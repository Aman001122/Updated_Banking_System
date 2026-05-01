from bank import Bank, OverdraftError, InvalidAmountError, validate_pin

bank = Bank()


def create_account():
    acc = input("account number: ")
    name = input("name: ")
    pin = input("4-digit pin: ")

    if not validate_pin(pin):
        print("weak or invalid pin")
        return

    try:
        bank.create_account(acc, name, pin)
        print("account created")
    except:
        print("account may already exist")


def reset_pin():
    acc = input("account number: ")
    name = input("name: ")
    new_pin = input("new pin: ")

    if not validate_pin(new_pin):
        print("weak pin")
        return

    if bank.reset_pin(acc, name, new_pin):
        print("pin reset successful")
    else:
        print("verification failed")


def login():
    attempts = 3

    while attempts > 0:
        acc = input("account number: ")
        pin = input("pin: ")

        if bank.login(acc, pin):
            return acc

        attempts -= 1
        print(f"invalid login, attempts left: {attempts}")

    print("account temporarily locked")

    choice = input("forgot pin? (yes/no): ").lower()

    if choice == "yes":
        reset_pin()

    return None


def atm_menu(acc):
    while True:
        print("\n1 deposit")
        print("2 withdraw")
        print("3 transfer")
        print("4 balance")
        print("5 mini statement")
        print("6 logout")

        ch = input("choose: ")

        try:
            if ch == "1":
                amt = int(input("amount: "))
                bank.deposit(acc, amt)
                print("done")

            elif ch == "2":
                amt = int(input("amount: "))
                bank.withdraw(acc, amt)
                print("done")

            elif ch == "3":
                to = input("receiver: ")
                amt = int(input("amount: "))
                bank.transfer(acc, to, amt)
                print("transfer successful")

            elif ch == "4":
                print("balance:", bank.get_balance(acc))

            elif ch == "5":
                for t in bank.get_transactions(acc):
                    print(t)

            elif ch == "6":
                break

        except (InvalidAmountError, OverdraftError, Exception, ValueError) as e:
            print(e)


while True:
    print("\n1 login")
    print("2 create account")
    print("3 exit")

    ch = input("choose: ")

    if ch == "1":
        acc = login()
        if acc:
            atm_menu(acc)

    elif ch == "2":
        create_account()

    elif ch == "3":
        break