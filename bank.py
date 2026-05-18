import sqlite3
import hashlib


def hash_pin(pin:str)->str:
    return hashlib.sha256(pin.encode()).hexdigest()


def validate_pin(pin:str)->bool:
    return len(pin)==4 and pin.isdigit() and pin not in ["0000","1111","1234"]


class Account:
    def __init__(self,acc_no:str,name:str,balance:int):
        self.acc_no=acc_no
        self.name=name
        self.balance=balance

    def deposit(self,amt:int):
        self.balance+=amt

    def withdraw(self,amt:int)->bool:
        if amt>self.balance:
            return False

        self.balance-=amt
        return True

    def transfer(self,other,amt:int)->bool:
        if self.withdraw(amt):
            other.deposit(amt)
            return True

        return False


class Bank:
    def __init__(self):
        self.conn=sqlite3.connect("bank.db")

        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS accounts(acc_no TEXT PRIMARY KEY,name TEXT,pin TEXT,balance INTEGER)"
        )

        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS transactions(id INTEGER PRIMARY KEY AUTOINCREMENT,acc_no TEXT,detail TEXT)"
        )

    def create_account(self,acc:str,name:str,pin:str):
        self.conn.execute(
            "INSERT INTO accounts VALUES(?,?,?,?)",
            (acc,name,hash_pin(pin),0)
        )

        self.conn.commit()

    def login(self,acc:str,pin:str):
        row=self.conn.execute(
            "SELECT * FROM accounts WHERE acc_no=? AND pin=?",
            (acc,hash_pin(pin))
        ).fetchone()

        if row:
            return Account(row[0],row[1],row[3])

        return None

    def get_account(self,acc:str):
        row=self.conn.execute(
            "SELECT * FROM accounts WHERE acc_no=?",
            (acc,)
        ).fetchone()

        if row:
            return Account(row[0],row[1],row[3])

        return None

    def save(self,account):
        self.conn.execute(
            "UPDATE accounts SET balance=? WHERE acc_no=?",
            (account.balance,account.acc_no)
        )

        self.conn.commit()

    def add_transaction(self,acc:str,msg:str):
        self.conn.execute(
            "INSERT INTO transactions(acc_no,detail) VALUES(?,?)",
            (acc,msg)
        )

        self.conn.commit()

    def deposit(self,account,amt:int):
        account.deposit(amt)

        self.save(account)

        self.add_transaction(
            account.acc_no,
            "+"+str(amt)
        )

    def withdraw(self,account,amt:int)->bool:
        ok=account.withdraw(amt)

        if ok:
            self.save(account)

            self.add_transaction(
                account.acc_no,
                "-"+str(amt)
            )

        return ok

    def transfer(self,sender,receiver,amt:int)->bool:
        ok=sender.transfer(receiver,amt)

        if ok:
            self.save(sender)
            self.save(receiver)

            self.add_transaction(
                sender.acc_no,
                "sent "+str(amt)
            )

            self.add_transaction(
                receiver.acc_no,
                "received "+str(amt)
            )

        return ok

    def get_balance(self,account)->int:
        return account.balance

    def get_transactions(self,acc:str):
        data=self.conn.execute(
            "SELECT detail FROM transactions WHERE acc_no=? ORDER BY id DESC LIMIT 5",
            (acc,)
        ).fetchall()

        return [i[0] for i in data]