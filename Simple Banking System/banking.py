import random
import sqlite3

conn = sqlite3.connect('card.s3db')

cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS card;')
cur.execute('CREATE TABLE card(id INTEGER PRIMARY KEY, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);')
conn.commit()

issued_cards = {}
iin_code = '400000'


def select_option_to_start():
    print('1. Create an account')
    print('2. Log into account')
    print('0. Exit')
    select = int(input())
    if select == 1:
        generate_card_details()
    elif select == 2:
        login_into_account()
    elif select == 0:
        print('Bye!')
        exit()
    else:
        print("Error of selection the first option")


def generate_bin_number(iin):
    number = random.randint(100000000, 999999999)
    card_number = iin + str(number)
    return card_number


def generate_checksum_number(bin_number):
    global next_multiple_ten_num
    card_number_list = list()
    temp_bin_num = bin_number
    for i in bin_number:
        element = int(temp_bin_num) % 10
        temp_bin_num = temp_bin_num[:-1]
        card_number_list.append(element)
    card_number_list.reverse()
    card_number_list[0] = card_number_list[0] * 2
    card_number_list[2] = card_number_list[2] * 2
    card_number_list[4] = card_number_list[4] * 2
    card_number_list[6] = card_number_list[6] * 2
    card_number_list[8] = card_number_list[8] * 2
    card_number_list[10] = card_number_list[10] * 2
    card_number_list[12] = card_number_list[12] * 2
    card_number_list[14] = card_number_list[14] * 2
    for i in range(0, len(card_number_list)):
        if card_number_list[i] > 9:
            card_number_list[i] -= 9
    checksum = sum(card_number_list)
    if (checksum % 10) > 0:
        next_multiple_ten_num = checksum + (10 - checksum % 10)
    elif (checksum % 10) == 0:
        next_multiple_ten_num = checksum
    else:
        print('Smth goes wrong with checksum')
    last_digit = next_multiple_ten_num - checksum
    return last_digit


def generate_card_details():
    bin_number = generate_bin_number(iin_code)
    checksum_number = generate_checksum_number(bin_number)
    card_number = bin_number + str(checksum_number)
    pin_code = random.randint(1000, 9999)
    print()
    print('Your card has been created')
    print('Your card number:')
    print(card_number)
    print('Your card PIN:')
    print(pin_code)
    print()
    issued_cards[card_number] = pin_code
    cur.execute('INSERT INTO card(number, pin) VALUES(?, ?)', (card_number, pin_code))
    conn.commit()


def login_into_account():
    print()
    print('Enter your card number:')
    enter_card_number = input()
    print('Enter your PIN:')
    enter_pin = int(input())
    if enter_card_number in issued_cards and enter_pin == issued_cards[enter_card_number]:
        print()
        print('You have successfully logged in!')
        print()
        access_balance(enter_card_number)
    else:
        print('Wrong card number or PIN!')
        print()


def access_balance(card_number):
    print('''1. Balance
    2. Add income
    3. Do transfer
    4. Close account
    5. Log out
    0. Exit''')
    select = int(input())
    if select == 1:
        check_balance(card_number)
    elif select == 2:
        add_income(card_number)
    elif select == 3:
        do_transfer_check(card_number)
    elif select == 4:
        close_account(card_number)
    elif select == 5:
        print('You have successfully logged out!')
        select_option_to_start()
    elif select == 0:
        print('Bye!')
        exit()
    else:
        print("error in selecting a balance option")


def add_income(card_number):
    print()
    print('Enter income:')
    income = int(input())
    current_balance = cur.execute('SELECT balance FROM card WHERE number = ?', (card_number,)).fetchone()
    new_balance = income + int(current_balance[0])
    cur.execute('UPDATE card SET balance = ? WHERE number = ?', (new_balance, card_number))
    conn.commit()
    print('Income was added!')
    print()
    access_balance(card_number)


def do_transfer_check(card_number_from):
    print('Enter card number:')
    card_number_to = input()
    if cards_from_to_equal(card_number_from, card_number_to) is True and luhn_check_card_to(card_number_to) is True and card_to_exist(card_number_to) is True:
        print("Enter how much money you want to transfer:")
        amount_to_transfer = input()
        if enough_balance_check(card_number_from, amount_to_transfer) is True:
            make_transfer(card_number_from, card_number_to, amount_to_transfer)
        else:
            access_balance(card_number_from)
    else:
        access_balance(card_number_from)


def make_transfer(card_number_from, card_number_to, amount_to_transfer):
    balance_from = cur.execute('SELECT balance FROM card WHERE number = ?', (card_number_from,)).fetchone()
    balance_to = cur.execute('SELECT balance FROM card WHERE number = ?', (card_number_to,)).fetchone()
    new_balance_from = int(balance_from[0]) - int(amount_to_transfer)
    new_balance_to = int(balance_to[0]) + int(amount_to_transfer)
    cur.execute('UPDATE card SET balance = ? WHERE number = ?', (new_balance_from, card_number_from))
    conn.commit()
    cur.execute('UPDATE card SET balance = ? WHERE number = ?', (new_balance_to, card_number_to))
    conn.commit()


def close_account(card_number_to_close):
    print()
    print('The account has been closed!')
    cur.execute('DELETE FROM card where number = ?', (card_number_to_close,))
    conn.commit()


def cards_from_to_equal(card_number_from, card_number_to):
    if card_number_to == card_number_from:
        print("You can't transfer money to the same account!")
        return False
    else:
        return True


def card_to_exist(card_number_to):
    card_available_in_database = cur.execute('SELECT number FROM card WHERE number = ?', (card_number_to,)).fetchone()
    if card_available_in_database is None or card_number_to != card_available_in_database[0]:
        print("Such a card does not exist.")
        return False
    else:
        return True


# def luhn_check_card_to(card_number_to):
#     card_number_list = list()
#     for i in card_number_to:
#         element = int(card_number_to) % 10
#         card_number_to = card_number_to[:-1]
#         card_number_list.append(element)
#     card_number_list.reverse()
#     temp_card_number_list = card_number_list[:-1]
#     temp_card_number_list[0] = temp_card_number_list[0] * 2
#     temp_card_number_list[2] = temp_card_number_list[2] * 2
    # temp_card_number_list[4] = temp_card_number_list[4] * 2
    # temp_card_number_list[6] = temp_card_number_list[6] * 2
    # temp_card_number_list[8] = temp_card_number_list[8] * 2
    # temp_card_number_list[10] = temp_card_number_list[10] * 2
    # temp_card_number_list[12] = temp_card_number_list[12] * 2
    # temp_card_number_list[14] = temp_card_number_list[14] * 2
    # for i in range(0, len(temp_card_number_list)):
    #     if temp_card_number_list[i] > 9:
    #         temp_card_number_list[i] -= 9
    # checksum = sum(temp_card_number_list)
    # if checksum
    #
    # print("Probably you made a mistake in the card number. Please try again!")

def luhn_check_card_to(card_number_to):
    bin_number = card_number_to[:-1]
    last_element = card_number_to[-1]
    if generate_checksum_number(bin_number) == int(last_element):
        return True
    elif generate_checksum_number(bin_number) != int(last_element):
        print("Probably you made a mistake in the card number. Please try again!")
        return False
    else:
        print("Error")


def enough_balance_check(card_number_from, amount_transfer):
    from_balance = cur.execute('SELECT balance FROM card WHERE number = ?', (card_number_from,)).fetchone()
    if int(amount_transfer) <= int(from_balance[0]):
        return True
    else:
        print("Not enough money!")
        return False


def check_balance(card_number_to_check):
    from_balance = cur.execute('SELECT balance FROM card WHERE number = ?', card_number_to_check)
    print('Balance: ')


while True:
    select_option_to_start()
