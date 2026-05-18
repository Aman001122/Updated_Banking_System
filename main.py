import sqlite3
from bank import Bank,validate_pin

bank=Bank()

while True:
    print("\n1.Create")
    print("2.Login")
    print("3.Exit")

    ch=input("Enter: ")

    if ch=="1":
        acc=input("Account: ")
        name=input("Name: ")
        pin=input("PIN: ")

        if not validate_pin(pin):
            print("Weak pin")
            continue

        try:
            bank.create_account(acc,name,pin)
            print("Account created")

        except sqlite3.IntegrityError:
            print("Account exists")

    elif ch=="2":
        acc=input("Account: ")
        pin=input("PIN: ")

        user=bank.login(acc,pin)

        if not user:
            print("Wrong details")
            continue

        while True:
            print("\n1.Balance")
            print("2.Deposit")
            print("3.Withdraw")
            print("4.Transfer")
            print("5.Statement")
            print("6.Logout")

            op=input("Choose: ")

            if op=="1":
                print(bank.get_balance(user))

            elif op=="2":
                try:
                    amt=int(input("Amount: "))
                    bank.deposit(user,amt)

                except ValueError:
                    print("Numbers only")

            elif op=="3":
                try:
                    amt=int(input("Amount: "))

                    if not bank.withdraw(user,amt):
                        print("Not enough balance")

                except  ValueError:
                    print("Numbers only")
            elif op=="4":
                try:
                    to=input("Receiver: ")
                    amt=int(input("Amount: "))

                    receiver=bank.get_account(to)

                    if not receiver:
                        print("Account not found")

                    elif not bank.transfer(user,receiver,amt):
                        print("Not enough balance")

                except ValueError:
                    print("Numbers only")

            elif op=="5":
                data=bank.get_transactions(user.acc_no)

                for i in data:
                    print(i)

            elif op=="6":
                break

    elif ch=="3":
        break