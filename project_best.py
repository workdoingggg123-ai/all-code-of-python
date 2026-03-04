import os
from datetime import datetime

class Bank:

    FILE_NAME = "bank_server.txt"
    TRANSACTION_FILE = "transactions.txt"

    # ---------------- CREATE ACCOUNT ----------------
    def making_account(self):
        name = input("ENTER NAME: ")
        acc = input("ENTER ACCOUNT NUMBER: ")

        # Check duplicate account
        if os.path.exists(self.FILE_NAME):
            with open(self.FILE_NAME, "r") as file:
                for line in file:
                    old_acc, _, _ = line.strip().split(',')
                    if old_acc == acc:
                        print("❌ ACCOUNT NUMBER ALREADY EXISTS!")
                        return

        money = int(input("ENTER INITIAL DEPOSIT: "))

        with open(self.FILE_NAME, "a") as file:
            file.write(f"{acc},{name},{money}\n")

        # Save first transaction as deposit
        with open(self.TRANSACTION_FILE, "a") as tfile:
            tfile.write(f"{acc},DEPOSIT,{money},{money},{datetime.now()}\n")

        print("✅ ACCOUNT CREATED SUCCESSFULLY!")

    # ---------------- CHECK BALANCE ----------------
    def check_balance(self):
        acc_no = input("ENTER ACCOUNT NUMBER: ")

        try:
            with open(self.FILE_NAME, "r") as file:
                for line in file:
                    acc, name, money = line.strip().split(',')
                    if acc == acc_no:
                        print(f"\nACCOUNT HOLDER: {name}")
                        print(f"BALANCE: {money}")
                        return
            print("❌ ACCOUNT NOT FOUND!")
        except FileNotFoundError:
            print("NO DATA FOUND!")

    # ---------------- DEPOSIT MONEY ----------------
    def add_money(self):
        acc_no = input("ENTER ACCOUNT NUMBER: ")
        amount = int(input("ENTER AMOUNT TO DEPOSIT: "))

        updated_data = []
        found = False

        try:
            with open(self.FILE_NAME, "r") as file:
                for line in file:
                    acc, name, money = line.strip().split(',')

                    if acc == acc_no:
                        new_balance = int(money) + amount
                        money = str(new_balance)
                        found = True
                        print("✅ MONEY DEPOSITED SUCCESSFULLY")

                        # Save transaction
                        with open(self.TRANSACTION_FILE, "a") as tfile:
                            tfile.write(f"{acc},DEPOSIT,{amount},{new_balance},{datetime.now()}\n")

                    updated_data.append(f"{acc},{name},{money}\n")

            if found:
                with open(self.FILE_NAME, "w") as file:
                    file.writelines(updated_data)
            else:
                print("❌ ACCOUNT NOT FOUND!")

        except FileNotFoundError:
            print("NO DATA FOUND!")

    # ---------------- WITHDRAW MONEY ----------------
    def withdraw_money(self):
        acc_no = input("ENTER ACCOUNT NUMBER: ")
        amount = int(input("ENTER AMOUNT TO WITHDRAW: "))

        updated_data = []
        found = False

        try:
            with open(self.FILE_NAME, "r") as file:
                for line in file:
                    acc, name, money = line.strip().split(',')

                    if acc == acc_no:
                        if int(money) >= amount:
                            new_balance = int(money) - amount
                            money = str(new_balance)
                            found = True
                            print("✅ WITHDRAW SUCCESSFUL")

                            # Save transaction
                            with open(self.TRANSACTION_FILE, "a") as tfile:
                                tfile.write(f"{acc},WITHDRAW,{amount},{new_balance},{datetime.now()}\n")
                        else:
                            print("❌ INSUFFICIENT BALANCE")
                            return

                    updated_data.append(f"{acc},{name},{money}\n")

            if found:
                with open(self.FILE_NAME, "w") as file:
                    file.writelines(updated_data)
            else:
                print("❌ ACCOUNT NOT FOUND!")

        except FileNotFoundError:
            print("NO DATA FOUND!")

    # ---------------- VIEW ALL ACCOUNTS (ADMIN) ----------------
    def view_all_accounts(self):
        password = "17072007"
        verify = input("ENTER ADMIN PASSWORD: ")

        if verify != password:
            print("❌ INCORRECT PASSWORD")
            return

        try:
            with open(self.FILE_NAME, "r") as file:
                lines = file.readlines()

                if not lines:
                    print("NO ACCOUNTS FOUND!")
                    return

                print("\nTOTAL ACCOUNTS:", len(lines))
                print("-" * 40)

                for line in lines:
                    acc, name, money = line.strip().split(',')
                    print(f"ACCOUNT NUMBER: {acc}")
                    print(f"NAME: {name}")
                    print(f"BALANCE: {money}")
                    print("-" * 40)

        except FileNotFoundError:
            print("NO DATA FOUND!")

    # ---------------- TRANSACTION HISTORY ----------------
    def transaction_history(self):
        acc_no = input("ENTER ACCOUNT NUMBER: ")
        found = False

        try:
            with open(self.TRANSACTION_FILE, "r") as file:
                print("\n===== TRANSACTION HISTORY =====\n")

                for line in file:
                    acc, t_type, amount, balance, date = line.strip().split(',')

                    if acc == acc_no:
                        found = True
                        print(f"TYPE: {t_type}")
                        print(f"AMOUNT: {amount}")
                        print(f"BALANCE AFTER: {balance}")
                        print(f"DATE: {date}")
                        print("-" * 40)

                if not found:
                    print("NO TRANSACTIONS FOUND FOR THIS ACCOUNT.")

        except FileNotFoundError:
            print("NO TRANSACTION DATA FOUND!")


# ---------------- MAIN PROGRAM ----------------
bank = Bank()

while True:
    print("\n===== BANK MANAGEMENT SYSTEM =====")
    print("1. Create Account")
    print("2. Check Balance")
    print("3. Withdraw Money")
    print("4. Deposit Money")
    print("5. View All Accounts (Admin)")
    print("6. Transaction History")
    print("7. Exit")

    choice = input("ENTER YOUR CHOICE: ")

    if choice == "1":
        bank.making_account()
    elif choice == "2":
        bank.check_balance()
    elif choice == "3":
        bank.withdraw_money()
    elif choice == "4":
        bank.add_money()
    elif choice == "5":
        bank.view_all_accounts()
    elif choice == "6":
        bank.transaction_history()
    elif choice == "7":
        print("THANK YOU FOR USING BANK SYSTEM!")
        break
    else:
        print("INVALID CHOICE! TRY AGAIN.")