import sqlite3
import hashlib
from datetime import datetime

def hash_pin(pin):
    return hashlib.sha256(pin.encode()).hexdigest()

def validate_pin(pin):
    if len(pin)!=4 or not pin.isdigit():
        return False
    if pin in ["0000","1111","1234"]:
        return False
    return True


class Account:
    def __init__(self, acc_no, balance):
        self.acc_no = acc_no
        self.balance = balance

    def deposit(self, amt):
        if amt>0:
            self.balance += amt

    def withdraw(self, amt):
        if amt<=self.balance:
            self.balance -= amt
            return True
        return False


class Bank:
    def __init__(self):
        self.conn = sqlite3.connect("bank.db")
        self.conn.execute("CREATE TABLE IF NOT EXISTS accounts(acc_no TEXT PRIMARY KEY,name TEXT,pin TEXT,balance INTEGER)")
        self.conn.execute("CREATE TABLE IF NOT EXISTS transactions(id INTEGER PRIMARY KEY AUTOINCREMENT,acc_no TEXT,detail TEXT)")

    def create_account(self,acc,name,pin):
        self.conn.execute("INSERT INTO accounts VALUES(?,?,?,?)",(acc,name,hash_pin(pin),0))
        self.conn.commit()

    def login(self,acc,pin):
        cur = self.conn.execute("SELECT * FROM accounts WHERE acc_no=? AND pin=?",(acc,hash_pin(pin)))
        return cur.fetchone()

    def get_account(self,acc):
        cur = self.conn.execute("SELECT balance FROM accounts WHERE acc_no=?",(acc,))
        row = cur.fetchone()
        if row:
            return Account(acc,row[0])
        return None

    def update_balance(self,account):
        self.conn.execute("UPDATE accounts SET balance=? WHERE acc_no=?",(account.balance,account.acc_no))
        self.conn.commit()

    def add_transaction(self,acc,detail):
        self.conn.execute("INSERT INTO transactions(acc_no,detail) VALUES(?,?)",(acc,detail))
        self.conn.commit()

    def get_transactions(self,acc):
        cur = self.conn.execute("SELECT detail FROM transactions WHERE acc_no=? ORDER BY id DESC LIMIT 5",(acc,))
        return [i[0] for i in cur.fetchall()]