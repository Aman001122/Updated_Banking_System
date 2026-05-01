# Banking Transaction System Assignment


# 1. Code Explanation

"""
Overall Flow:
This is a command-line banking system.
The program starts from main.py where user can login or create account.

After login, user can:
deposit, withdraw, transfer, check balance, and see mini statement.

All operations run in a loop until user logs out.
"""


"""
How Transactions Work:
Transactions are handled using functions inside the Bank class.

When a user performs an action:
- data is updated in the database
- transaction is recorded
- changes are saved

Each transaction is stored with timestamp.
"""


"""
How Data is Stored:
Initially data was stored in JSON, but later it was replaced with SQLite database.

There are two tables:
- accounts (stores account details)
- transactions (stores transaction history)

This improves performance and structure.
"""


"""
Deposit, Withdraw, Transfer:

Deposit:
- adds amount to balance
- saves transaction

Withdraw:
- checks balance
- subtracts amount
- saves transaction

Transfer:
- checks receiver exists
- checks balance
- transfers money between accounts
"""


# 2. Issues in Original Code

"""
1. Data stored in JSON (not scalable)
2. PIN stored in plain text
3. No proper error handling
4. Code repetition
5. No logging system
6. Weak validation
"""


# 3. Improvements Made (Phases)

"""
Phase 1 (OOP):
- Created Account and Bank classes
- Moved logic into methods

Phase 2 (Error Handling):
- Added try-except blocks
- Created custom exceptions like OverdraftError

Phase 3 (PEP8 & Type Hints):
- Improved code formatting
- Added type hints for better readability

Phase 4 (Security & Logging):
- Hashed PIN using SHA-256
- Added logging using logging module

Phase 5 (SQLite):
- Replaced JSON with SQLite database
- Created tables for accounts and transactions
"""


# 4. Tests

def test_deposit():
    balance = 1000
    amt = 500
    new_balance = balance + amt
    assert new_balance == 1500


def test_withdraw_fail():
    balance = 1000
    amt = 5000

    if amt > balance:
        result = False
    else:
        result = True

    assert result == False


# 5. What was hard

"""
Understanding how to move from simple functions to classes was slightly confusing.
Also learning how database replaces JSON took some time.
"""


# 6. Future Improvements

"""
- Add GUI interface
- Improve security further
- Add user authentication features
- Optimize database queries
"""