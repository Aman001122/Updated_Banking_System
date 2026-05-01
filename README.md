# Banking Transaction System

This is a simple banking system project made using Python.

It allows users to:
- Create account
- Login using PIN
- Deposit money
- Withdraw money
- Transfer money
- View balance
- See mini statement

The project was first made using JSON, but later updated to use SQLite database for better data handling.

PINs are stored securely using hashing, so they are not visible directly.

There is also a logging system which stores all transactions in a log file.

A basic GUI is also added using Tkinter so the program runs in a popup window instead of terminal.

## Files

- bank.py → main backend logic and database handling
- main.py → CLI version (optional)
- gui.py → GUI version using Tkinter
- bank.db → database file (auto created)
- bank.log → log file (auto created)

## How to run

Run the GUI version:

python gui.py

## Features added

- OOP (classes used)
- Error handling
- SQLite database
- PIN hashing
- Logging
- Simple GUI

## Note

This is a basic project made for learning purposes.