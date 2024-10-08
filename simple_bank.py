from datetime import datetime

menu = """
[d] Deposit
[w] Withdraw
[e] Extract
[q] Quit program

=> """

balance = 0
limit = 500
extract = ""
number_transactions = 0
LIMIT_TRANSACTION = 10
daily_transactions = []

while True:
    option = input(menu).lower()

    if option == "d" or option == "w":
        if number_transactions >= LIMIT_TRANSACTION:
            print("You have reached the limit of transactions for the day.")
            continue

    if option == "d":
        valor = float(input("Enter an amount for the deposit: "))

        if valor > 0:
            balance += valor
            data = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            extract += f"{data} - Deposit: R$ {valor:.2f}\n"
            number_transactions += 1
            daily_transactions.append('d')

        else:
            print("The value entered is invalid")

    elif option == "w":
        valor = float(input("Enter an amount for the withdraw: "))

        exceeded_balance = valor > balance
        exceeded_limit = valor > limit

        if exceeded_balance:
            print("Unable to withdraw money due to lack of funds")

        elif exceeded_limit:
            print("Withdrawal amount exceeds limit")

        elif valor > 0:
            balance -= valor
            data = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            extract += f"{data} - Withdraw: R$ {valor:.2f}\n"
            number_transactions += 1
            daily_transactions.append('w')

        else:
            print("Operation failed! The value entered is invalid")

    elif option == "e":
        print("\n********** Extract **********")
        print("There was no transaction" if not extract else extract)
        print(f"\nBalance: R$ {balance:.2f}")
        print(f"Number of transactions today: {number_transactions}/{LIMIT_TRANSACTION}")
        print("********************")

    elif option == "q":
        break

    else:
        print("Wrong option, please select again a valid operation.")