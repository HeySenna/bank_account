import textwrap


def menu():
    menu = """\n
    ================ MENU ================
    [d]\Deposit
    [s]\Withdrawl
    [e]\Extract
    [nc]\tNew account
    [lc]\tList accounts
    [nu]\tNew user
    [q]\tExit
    => """
    return input(textwrap.dedent(menu))


def deposit(balance, valor, extract, /):
    if valor > 0:
        balance += valor
        extract += f"Deposit:\tR$ {valor:.2f}\n"
        print("\n=== Deposit successfully made!! ===")
    else:
        print("\n@@@ Operation failed! The value entered is invalid. @@@")

    return balance, extract


def withdrawl(*, balance, valor, extract, limit, number_withdrawl, limit_withdrawl):
    exceed_balance = valor > balance
    exceed_limit = valor > limit
    exceed_withdrawl = number_withdrawl >= limit_withdrawl

    if exceed_balance:
        print("\n@@@ Operation failed! You don't have enough balance. @@@")

    elif exceed_limit:
        print("\n@@@ Operation failed! The withdrawal amount exceeds the limit. @@@")

    elif exceed_withdrawl:
        print("\n@@@ Operation failed! Maximum number of withdrawals exceeded. @@@")

    elif valor > 0:
        balance -= valor
        extract += f"Withdrawl:\t\tR$ {valor:.2f}\n"
        number_withdrawl += 1
        print("\n=== Loot carried out successfully! ===")

    else:
        print("\n@@@ Operation failed! The value entered is invalid. @@@")

    return balance, extract


def show_extract(balance, /, *, extract):
    print("\n================ Extract ================")
    print("No moves were made." if not extract else extract)
    print(f"\Balance:\t\tR$ {balance:.2f}")
    print("==========================================")


def create_users(users):
    cpf = input("Inform CPF (only numbers): ")
    user = filter_users(cpf, users)

    if user:
        print("\n@@@ Already exist a user with this CPF! @@@")
        return

    name = input("Inform your full name: ")
    birth_date = input("Inform your birth date (dd-mm-yyyy): ")
    address = input("Enter the address (logradouro, nro - neighborhood - city/acronym state): ")

    users.append({"name": name, "birth_date": birth_date, "cpf": cpf, "address": address})

    print("=== User created with sucess ===")


def filter_users(cpf, users):
    filter_users = [user for user in users if user["cpf"] == cpf]
    return filter_users[0] if filter_users else None


def create_account(agency, number_account, users):
    cpf = input("Inform user CPF: ")
    user = filter_users(cpf, users)

    if user:
        print("\n=== Account successfully created! ===")
        return {"agency": agency, "number_account": number_account, "user": user}

    print("\n@@@ User not found, account creation flow closed! @@@")


def list_accounts(accounts):
    for account in accounts:
        line = f"""\
            Agency:\t{account['agencia']}
            C/C:\t\t{account['numero_conta']}
            Titular:\t{account['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(line))


def main():
    LIMIT_WITHDRAWL = 3
    AGENCY = "0001"

    balance = 0
    limit = 500
    extract = ""
    number_withdrawl = 0
    users = []
    accounts = []

    while True:
        option = menu()

        if option == "d":
            valor = float(input("inform value of withdrawl: "))

            balance, extract = deposit(balance, valor, extract)

        elif option == "s":
            valor = float(input("inform value of balance: "))

            balance, extract = withdrawl(
                balance=balance,
                valor=valor,
                extract=extract,
                limit=limit,
                number_withdrawl=number_withdrawl,
                limit_withdrawl=LIMIT_WITHDRAWL,
            )

        elif option == "e":
            show_extract(balance, extract=extract)

        elif option == "nu":
            create_users(users)

        elif option == "nc":
            number_account = len(accounts) + 1
            conta = create_account(AGENCY, number_account, users)

            if accounts:
                accounts.append(conta)

        elif option == "lc":
            list_accounts(accounts)

        elif option == "q":
            break

        else:
            print("Invalid operation, please select new desired operation")


main()