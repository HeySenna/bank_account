import textwrap
from abc import ABC, abstractmethod
from datetime import datetime
class Client:
    def __init__(self, address):
        self.address = address
        self.accounts = []

    def perform_transaction(self, account, transaction):
        transaction.register(account)

    def add_account(self, account):
        self.accounts.append(account)


class PhysicalPerson(Client):
    def __init__(self, name, birth_date, cpf, address):
        super().__init__(address)
        self.name = name
        self.birth_date = birth_date
        self.cpf = cpf


class Account:
    def __init__(self, number, client):
        self.balance = 0
        self.number = number
        self._agency = "0001"
        self._cliente = client
        self._history = History()

    @classmethod
    def new_account(cls, client, number):
        return cls(number, client)

    @property
    def balance(self):
        return self._balance
    @property
    def number(self):
        return self._number

    @property
    def agency(self):
        return self._agency

    @property
    def client(self):
        return self._client

    @property
    def history(self):
        return self._history

    def Withdrawl(self, value):
        balance = self.balance
        exceed_balance = value > balance

        if exceed_balance:
            print("\n@@@  Operation failed! You don't have enough balance.@@@")

        elif value > 0:
            self._balance -= value
            print("\n===  Loot carried out successfully! ===")
            return True

        else:
            print("\n@@@ OOperation failed! The value entered is invalid.  @@@")

        return False

    def deposit(self, value):
        if value > 0:
            self._balance += value
            print("\n=== Deposit successfully made! ===")
        else:
            print("\n@@@ Operation failed! The value entered is invalid. @@@")
            return False

        return True


class CurrentAccount(Account):
    def __init__(self, number, cliennt, limit=500, limit_withdrawl=3):
        super().__init__(number, cliennt)
        self._limit = limit
        self.limit_withdrawl = limit_withdrawl

    def withdrawl(self, value):
        withdrawl_number = len(
            [transaction for transaction in self.history._transactions if transaction["tipo"] == Withdrawl.__name__]
        )

        exceed_limit = value > self._limite
        excedeu_withdrawl = withdrawl_number >= self._exceed_limit

        if exceed_limit:
            print("\n@@@ Operation failed! The withdrawal amount exceeds the limit. @@@")

        elif excedeu_withdrawl:
            print("\n@@@ Operation failed! Maximum number of withdrawals exceeded. @@@")

        else:
            return super().withdrawl(value)

        return False

    def __str__(self):
        return f"""\
            Agency:\t{self.agency}
            C/C:\t\t{self.number}
            Titular:\t{self.client.name}
        """


class History:
    def __init__(self):
        self._transactions = []

    @property
    def _transactions(self):
        return self._transactions

    def add_transactions(self, transaction):
        self.transactions.append(
            {
                "type": transaction.__class__.__name__,
                "value": transaction.value,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
            }
        )


class Transaction(ABC):
    @property
    @abstractmethod
    def value(self):
        pass

    @abstractmethod
    def register(self, account):
        pass


class Withdrawl(Transaction):
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    def register(self, account):
        sucess_transaction = account.withdrawl(self.value)

        if sucess_transaction:
            account.history.add_transactions(self)


class Deposit(Transaction):
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    def register(self, account):
        sucess_transaction = account.deposit(self.value)

        if sucess_transaction:
            account.history.add_transactions(self)


def menu():
    menu = """\n
    ================ MENU ================
    [d]\Deposit
    [s]\Withdrawl
    [e]\tExtract
    [nc]\tNew account
    [lc]\tList accounts
    [nu]\tNew user
    [q]\tExit
    => """
    return input(textwrap.dedent(menu))


def filter_client(cpf, clients):
    filtered_clients = [client for client in clients if client["cpf"] == cpf]
    return filtered_clients[0] if filtered_clients else None



def recover_client_account(client):
    if not client.accounts:
        print("\n@@@ Cliente doesn't have a account! @@@")
        return

    # FIXME: não permite cliente escolher a conta
    return client.account[0]


def deposit(clients):
    cpf = input("Informe CPF client: ")
    client = filter_client(cpf, clients)

    if not client:
        print("\n@@@ Cliente not found! @@@")
        return

    value = float(input("Informe value of deposit: "))
    transaction = Deposit(value)

    account = recover_client_account(clients)
    if not account:
        return

    client.perform_transaction(account, transaction)


def withdrawl(clients):
    cpf = input("Informe CPF client: ")
    client = filter_client(cpf, clients)

    if not client:
        print("\n@@@ Cliente not found! @@@")
        return

    value = float(input("Informe value of withdrawl: "))
    transaction = Withdrawl(value)

    account = recover_client_account(client)
    if not account:
        return

    client.perform_transaction(account, transaction)


def show_extract(clients):
    cpf = input("Informe o CPF do cliente: ")
    client = filter_client(cpf, clients)

    if not client:
        print("\n@@@ Client not found! @@@")
        return

    account = recover_client_account(client)
    if not account:
        return

    print("\n================ EXTRATO ================")
    transactions = account.history.transactions

    extract = ""
    if not transactions:
        extract = "Não foram realizadas movimentações."
    else:
        for transaction in transactions:
            extract += f"\n{transaction['type']}:\n\tR$ {transaction['value']:.2f}"

    print(extract)
    print(f"\Balance:\n\tR$ {account.balance:.2f}")
    print("==========================================")


def create_clients(clients):
    cpf = input("Inform CPF (only numbers): ")
    client = filter_client(cpf, clients)

    if client:
        print("\n@@@ Already exist a user with this CPF! @@@")
        return

    name = input("Inform your full name: ")
    birth_date = input("Inform your birth date (dd-mm-yyyy): ")
    address = input("Enter the address (logradouro, nro - neighborhood - city/acronym state): ")

    client = PhysicalPerson(name = name, birth_date = birth_date, cpf=cpf, address = address)

    clients.append(client)

    print("=== User created with sucess ===")

def create_account(number_account, clients, accounts):
    cpf = input("Inform user CPF: ")
    client = filter_client(cpf, clients)

    if not client:
        print("\n=== User not found, account creation flow closed! ===")
        return
    
    account = CurrentAccount.new_account(client = client, number = number_account)
    accounts.append(account)
    client.accounts.append(account)

def list_accounts(accounts):
    for account in accounts:
        print("=" * 100)
        print(textwrap.dedent(str(account)))


def main():
    clients = []
    accounts = []

    while True:
        option = menu()

        if option == "d":
            deposit(clients)

        elif option == "s":
            withdrawl(clients)

        elif option == "e":
            show_extract(clients)

        elif option == "nu":
            create_clients(clients)

        elif option == "nc":
            account_number = len(accounts) + 1
            create_account(account_number, clients, accounts)

        elif option == "lc":
            list_accounts(accounts)

        elif option == "q":
            break

        else:
            print("\n@@@ Invalid operation, please select new desired operation @@@")


main()