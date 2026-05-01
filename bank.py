import sqlite3
import hashlib
import logging
from datetime import datetime

logging.basicConfig(filename="bank.log", level=logging.INFO)


class OverdraftError(Exception):
    pass


class InvalidAmountError(Exception):
    pass


def hash_pin(pin):
    return hashlib.sha256(pin.encode()).hexdigest()


def validate_pin(pin):
    if not pin.isdigit() or len(pin) != 4:
        return False
    if pin in ["0000", "1111", "1234", "2222", "9999"]:
        return False
    return True


class Bank:
    def __init__(self):
        self.conn = sqlite3.connect("bank.db")
        self.create_tables()

    def create_tables(self):
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS accounts(
            acc_no TEXT PRIMARY KEY,
            name TEXT,
            pin TEXT,
            balance INTEGER
        )
        """)

        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS transactions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            acc_no TEXT,
            detail TEXT
        )
        """)

    def create_account(self, acc, name, pin):
        self.conn.execute(
            "INSERT INTO accounts VALUES (?, ?, ?, ?)",
            (acc, name, hash_pin(pin), 0)
        )
        self.conn.commit()

    def login(self, acc, pin):
        cur = self.conn.execute(
            "SELECT * FROM accounts WHERE acc_no=? AND pin=?",
            (acc, hash_pin(pin))
        )
        return cur.fetchone()

    def reset_pin(self, acc, name, new_pin):
        cur = self.conn.execute(
            "SELECT name FROM accounts WHERE acc_no=?",
            (acc,)
        )
        row = cur.fetchone()

        if not row or row[0] != name:
            return False

        self.conn.execute(
            "UPDATE accounts SET pin=? WHERE acc_no=?",
            (hash_pin(new_pin), acc)
        )
        self.conn.commit()
        return True

    def deposit(self, acc, amt):
        if amt <= 0:
            raise InvalidAmountError("invalid amount")

        self.conn.execute(
            "UPDATE accounts SET balance=balance+? WHERE acc_no=?",
            (amt, acc)
        )

        self.conn.execute(
            "INSERT INTO transactions(acc_no,detail) VALUES (?,?)",
            (acc, f"{datetime.now()} +{amt}")
        )

        self.conn.commit()

    def withdraw(self, acc, amt):
        balance = self.get_balance(acc)

        if amt <= 0:
            raise InvalidAmountError("invalid amount")

        if amt > balance:
            raise OverdraftError("insufficient balance")

        self.conn.execute(
            "UPDATE accounts SET balance=balance-? WHERE acc_no=?",
            (amt, acc)
        )

        self.conn.execute(
            "INSERT INTO transactions(acc_no,detail) VALUES (?,?)",
            (acc, f"{datetime.now()} -{amt}")
        )

        self.conn.commit()

    def transfer(self, acc, to, amt):
        if acc == to:
            raise Exception("cannot transfer to same account")

        balance = self.get_balance(acc)

        if amt <= 0:
            raise InvalidAmountError("invalid amount")

        if amt > balance:
            raise OverdraftError("insufficient balance")

        self.conn.execute(
            "UPDATE accounts SET balance=balance-? WHERE acc_no=?",
            (amt, acc)
        )

        self.conn.execute(
            "UPDATE accounts SET balance=balance+? WHERE acc_no=?",
            (amt, to)
        )

        self.conn.execute(
            "INSERT INTO transactions(acc_no,detail) VALUES (?,?)",
            (acc, f"{datetime.now()} sent {amt} to {to}")
        )

        self.conn.execute(
            "INSERT INTO transactions(acc_no,detail) VALUES (?,?)",
            (to, f"{datetime.now()} received {amt} from {acc}")
        )

        self.conn.commit()

    def get_balance(self, acc):
        cur = self.conn.execute(
            "SELECT balance FROM accounts WHERE acc_no=?",
            (acc,)
        )
        return cur.fetchone()[0]

    def get_transactions(self, acc):
        cur = self.conn.execute(
            "SELECT detail FROM transactions WHERE acc_no=? ORDER BY id DESC LIMIT 5",
            (acc,)
        )
        return [row[0] for row in cur.fetchall()]