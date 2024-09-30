menu = """

[d] Deposit
[w] Withdraw
[e] Extract
[q] Quit program

=> """

balance = 0
limit = 500
extract = ""
number_withdraw = 0
LIMIT_WITHDRAW = 3

while True:

    option = input(menu).lower()

    if option == "d":
        valor = float(input("Enter an amount for the deposit: "))
        
        if valor > 0:
            balance += valor
            extract += f"Deposit: R$ {valor:.2f}\n"
        
        else:
            print("The value entered is invalid")
    
    elif option == "w":
        valor = float(input("Enter an amount for the withdraw: "))

        exceeded_balance = valor > balance

        exceeded_limit = valor > limit

        exceeded_withdraw = number_withdraw >= LIMIT_WITHDRAW

        if exceeded_balance:
            print("Unable to withdraw money due to lack of funds")
        
        elif exceeded_limit:
            print("Withdrawal amount exceeds limit")
        
        elif exceeded_withdraw:
            print("Number of withdrawals exceed")
        
        elif valor > 0:
            balance -= valor
            extract += f"Withdraw: R$ {valor:.2f}\n"
            number_withdraw += 1
        
        else:
            print("Operation failed! The value entered is invalid")

    elif option == "e":
        print("\n********** Extract **********")
        print("There was no transaction" if not extract else extract)
        print(f"\n Balance: R$ {balance:.2f}")
        print("********************")

    elif option == "q":
       break

    else:
        print("Wrong option, please select again a valid operation.")