import sys


class CoffeeMachine:

    def __init__(self):
        self.water = 400
        self.milk = 540
        self.coffee_beans = 120
        self.disposable_cups = 9
        self.money = 550

    def coffee_machine_remaining(self):
        print(f"""The coffee machine has:
        {self.water} of water
        {self.milk} of milk
        {self.coffee_beans} of coffee beans
        {self.disposable_cups} of disposable cups
        ${self.money} of money""")

    def choose_action(self):
        action = input("Write action (buy, fill, take, remaining, exit):")
        if action == "buy":
            self.select_coffee_type()
        elif action == 'fill':
            self.fill_supplies()
        elif action == "take":
            self.take_money()
        elif action == "remaining":
            self.coffee_machine_remaining()
        elif action == "exit":
            sys.exit()
        else:
            print("Error")

    def select_coffee_type(self):
        coffee_type = input(
            "What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - back to the previous menu:")
        if coffee_type == '1':
            self.make_espresso()
        elif coffee_type == '2':
            self.make_latte()
        elif coffee_type == '3':
            self.make_cappuccino()
        elif coffee_type == 'back':
            self.choose_action()
        else:
            print("Error")

    def fill_supplies(self):
        add_water = int(input("Write how many ml of water do you want to add:"))
        #        add_water = int(input())
        add_milk = int(input("Write how many ml of milk do you want to add:"))
        add_coffee_beans = int(input("Write how many grams of coffee beans do you want to add:"))
        add_disposable_cups = int(input("Write how many disposable cups of coffee do you want to add:"))
        self.water += add_water
        self.milk += add_milk
        self.coffee_beans += add_coffee_beans
        self.disposable_cups += add_disposable_cups

    def take_money(self):
        take_money = self.money
        print(f"I gave you ${take_money}")
        self.money = 0

    #        return take_money

    def make_espresso(self):
        if self.check_supplies(250, 0, 16) is True:
            # For one espresso, the coffee machine needs 250 ml of water and 16 g of coffee beans. It costs $4.
            self.water -= 250
            self.milk -= 0
            self.coffee_beans -= 16
            self.money += 4
            self.disposable_cups -= 1

    def make_latte(self):
        if self.check_supplies(350, 75, 20) is True:
            # For a latte, the coffee machine needs 350 ml of water, 75 ml of milk, and 20 g of coffee beans. It costs $7.
            self.water -= 350
            self.milk -= 75
            self.coffee_beans -= 20
            self.money += 7
            self.disposable_cups -= 1

    def make_cappuccino(self):
        # And for a cappuccino, the coffee machine needs 200 ml of water, 100 ml of milk, and 12 g of coffee. It costs $6.
        if self.check_supplies(200, 100, 12) is True:
            self.water -= 200
            self.milk -= 100
            self.coffee_beans -= 12
            self.money += 6
            self.disposable_cups -= 1

    def check_supplies(self, water_needed, milk_needed, coffee_beans_needed):
        if self.water < water_needed:
            print("Sorry, not enough water!")
            return False

        if self.milk < milk_needed:
            print("Sorry, not enough milk!")
            return False

        if self.coffee_beans < coffee_beans_needed:
            print("Sorry, not enough coffee beans!")
            return False

        if self.disposable_cups < 0:
            print("Sorry, not enough disposable cups!")
            return False

        print("Yes, I can make that amount of coffee")
        return True


coffee_machine = CoffeeMachine()

while True:
    coffee_machine.choose_action()
    print()
