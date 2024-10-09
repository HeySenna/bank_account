from datetime import datetime
import textwrap

def deposit(balance, valor, extract, /):
    if valor > 0:
        saldo += valor
        extract += f"Deposit: \tR$ {valor:.2f}\n"
    else:
        print("\n Operation failed! the value entered is invalid")

    return balance, extract

def withdrawl(*, balance, valor, extract, limit, number_transactions, limit_transactions):
    exceeded_balance = valor > balance
    exceeded_limit = valor > limit
    exceeded_withdrawls = number_transactions >= limit_transactions

    if exceeded_balance:
        print("Unable to withdraw money due to lack of funds.")

    elif exceeded_limit:
        print("Withdrawal amount exceeds limit.")
    
    elif exceeded_withdrawls:
        print("Max amount of withdraw exceeds limit.")

    elif valor > 0:
        balance -= valor
        extract += f"Withdraw:\t\t R$ {valor:.2f}\n"
        number_transactions += 1
        print("\n Withdrawl successfully carried out ")

    else:
        print("Operation failed! The value entered is invalid")
    
    return balance, extract

def create_users(users):
    cpf = input("Inform your CPF (only numbers): ")
    user = filter_user(cpf, users)

    if user:
        print("\n Already exist a user with this CPF.")
        return
    
    name = input("Informe your full name: ")
    birth_date = input("Inform your birth date (dd-mm-aaaa): ")
    address = input("Inform your address (logradouro, nro - Neighborhood - City/Acronym state): ")

    users.append({"name": name, "birth_date": birth_date, "cpf": cpf, "address": address })

    print("User created with success!")

def filter_user(cpf, users):
    users_filtered = [user for user in users if user["cpf"] == cpf]
    return users_filtered[0] if users_filtered else None

def create_account(agency, number_account, users):
    cpf = input("Inform user CPF: ")
    user = filter_user(cpf, users)

    if user:
        print("\n Account created with success!")
        return {"agency": agency, "number_account": number_account, "user": user }
    
def list_accounts(accounts):
    for account in accounts:
        line = f"""\
            Agency:\t{account['agency']}
            C/C:\t\t{account['number_account']}
            Responsible:\t\t{account['user']['name']}
            """
        print("=" * 100)
        print(textwrap.dedent(line))

def show_extract(balance, /, *, extract):
    print("\n ============ Extract  ============")
    print("There were no changes." if not extract else extract)
    print(f"\n Balance: \t\t R${balance:.2f}")
    print("\n ==================================")

def menu():
    menu = """\n
    =======Menu=======
    [d]\tDeposit
    [w]\tWithdrawl
    [e]\tExtract
    [nc]\tNew account
    [lc]\tList accounts
    [nu]\tNew user
    [q]\tQuit program
    => """
    return input(textwrap.dedent(menu).lower())

def main():
    LIMIT_TRANSACTIONS = 3
    AGENCY = "0001"

    balance = 0
    limit = 500
    extract = ""
    number_transactions = 0
    users = []
    accounts= []

    while True:
        option = menu()

        if option == "d":
            valor = float(input("Enter an amount for the deposit: "))

            balance, extract = deposit(balance, valor, extract)

        elif option == "w":
            valor = float(input("Enter an amount for the withdrawl: "))

            balance, extract = withdrawl(
                balance = balance,
                valor = valor,
                extract = extract,
                limit = limit,
                number_transactions = number_transactions,
                limit_transactions = LIMIT_TRANSACTIONS,
            )
        elif option == "e":
            show_extract(balance, extract = extract)
        
        elif option == "nu":
            create_users(users)

        elif option == "nc":
            number_account = len(accounts) + 1
            account = create_account(AGENCY, number_account, users)

            if account:
                accounts.append(account)

        elif option == "lc":
            list_accounts(accounts)

        elif option == "q":
            break

        else:
            print("Wrong option, please select again a valid operation.")

main()