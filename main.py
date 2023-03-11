class Customer:
    def __init__(self, pin, name, balance):
        self.pin = pin
        self.name = name
        self.balance = balance


class ATM:
    def __init__(self):
        self.customers = []
        self.out_of_service = False
        self.card_validated = False
        self.withdrawal_approved = False
        self.available_funds = 1000
        self.active_customer = None
        self.get_customers()

    def get_customer_pin(self):
        while not self.card_validated:
            pin = input("Please enter your PIN: ")
            for customer in self.customers:
                if pin == customer.pin:
                    self.active_customer = customer
                    self.card_validated = True
            if self.active_customer:
                print(f"Hello {self.active_customer.name}")
            else:
                print(f"Invalid pin, please try again")

    def get_service(self):
        srv = None
        while srv != "1" or srv != "2" or srv != "3":
            srv = input("Please choose a service from the following options:"
                        "\n1:\tDisplay balance\n2:\tWithdraw Cash\n3:\tCancel, eject card\n")
            if srv == "1":
                self.display_balance()
            elif srv == "2":
                self.withdraw_cash()
                break
            elif srv == "3":
                self.eject_card()
                print("Please take your card. Goodbye!")
                break
            else:
                print("Please enter 1 or 2 to continue or 3 to eject your card")

    def display_balance(self):
        balance = self.active_customer.balance
        print(f"Your balance is: €{balance:,.2f} ")

    def withdraw_cash(self):
        while not self.withdrawal_approved:
            amount = 0
            amount = input("Enter the amount you want to withdraw: ")
            try:
                amount = int(amount)
                if amount == 0:
                    # this is added to avoid the ATM considering 0 to be a valid amount to dispense
                    raise Exception
                # check if the ATM has the funds
                if amount > self.available_funds:
                    print("Unable to dispense this amount. Please try a smaller amount")
                # check if the customer has funds in their account
                elif amount > self.active_customer.balance:
                    print("Insufficient funds in your account. Please try a smaller amount")
                # check if the input is a valid denomination - this ATM only contains 10 euros notes
                elif not self.is_valid_denomiation(amount):
                    print("Unable to dispense this amount. Please enter a multiple of 10")
                else:
                    # if we reach this point, dispense the cash
                    self.withdrawal_approved = True
                    print("Withdrawal approved. Please take your card and wait for your cash")
                    # once the cash is dispensed the ATM available cash is reduced by the amount
                    self.available_funds = self.available_funds - amount
                    if self.available_funds == 0:
                        # The ATM must go out of service when it has no more cash to dispense
                        self.out_of_service = True
                    # The customer balance is also reduced by the amount
                    self.active_customer.balance = self.active_customer.balance - amount
                    # The ATM must now be set to be ready for the next customer
                    self.eject_card()
                    break
            except:
                print(f"{amount} is not a valid amount.")

    def eject_card(self):
        # Return the ATM to the default state i.e. no active customer, no cash withdrawal approval
        # and no validated card
        self.active_customer = None
        self.withdrawal_approved = False
        self.card_validated = False

    def is_valid_denomiation(self, amount):
        return amount % 10 == 0

    def get_customers(self):
        c1 = Customer("1234", "Bob", 1435.62)
        self.customers.append(c1)
        c2 = Customer("2345", "Adam", 325)
        self.customers.append(c2)
        c3 = Customer("3456", "Molly", 1000)
        self.customers.append(c3)


def atm_runner():
    atm = ATM()
    while not atm.card_validated and not atm.out_of_service:
        atm.get_customer_pin()
        atm.get_service()

    if atm.out_of_service:
        print("Out of Service")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    atm_runner()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
