import random
from sys import exit
import sqlite3


def tax(user_income):
    tax_dict = {15528: 15, 42708: 25, 132407: 28}
    tax_percent = 0
    if user_income >= 15528:
        tax_percent = tax_dict[15528]
        if user_income >= 42708:
            tax_percent = tax_dict[42708]
            if user_income >= 132407:
                tax_percent = tax_dict[132407]
    return tax_percent


def calculate_tax():
    print('please write your income: ')
    income = int(input())
    percent = tax(income)
    calculated_tax = (income * percent)/100
    print(f'The tax for {income} is {percent}%. That is {round(calculated_tax)} dollars!')


def get_user_pin_from_table(user_card):
    command = f"""SELECT
    number,
    pin
    FROM
        card
    WHERE
        number = {user_card}
        ; """
    cur.execute(command)
    return cur.fetchall()[0][1]


def card_num_generator():
    return str(random.randint(000000000, 999999999)).zfill(9)


def add_income(income_amount, original_income, user_card):
    new_income = income_amount + original_income
    cur.execute(f"UPDATE card SET balance = {new_income} WHERE number = {user_card};")
    conn.commit()
    print('Income was added!')


# def check_card_num(user_card):
#     cur.fetchall()
#


def delete_account(user_card):
    user_card


class Cards:
    # info = dict()

    def __init__(self):
        pass

    def generate_pin(self):
        return f'{random.randrange(1, 10**3):04}'

    def luhan(self, card_pre):
        return "0"


    def new_account(self):
        card_pre = "400000" + card_num_generator()
        card_num = int(append(card_pre)) # self.luhan(card_pre)
        # self.info.update({card_num: {"pin": self.generate_pin(), "balance": 0}})
        new_pin = self.generate_pin()
        self.write_to_table(card_num, new_pin)
        print('Your card has been created')
        print('Your card number:')
        print(card_num)
        print(f'Your card PIN:')
        print(new_pin +'\n')


    def log_in(self):
        user_card = input('\nEnter your card number:\n')
        input_pin = input('Enter your PIN:')
        try:
            if get_user_pin_from_table(user_card) == input_pin and verify(user_card):
                print("You have successfully logged in!")
                self.logged_in_options(user_card)
            else:
                print("\nWrong card number or PIN!\n")
        except:
            print("\nWrong card number or PIN!\n")
    # def exit___():
    #     exit()

    def logged_in_options(self, user_card):
        logged_in_menu = {1: 'balance', 2: "Add income", 3: "Do transfer", 4: "Close account", 5: 'Log out', 0: 'Exit___'}
        logged_in_msg = """1. Balance \n2. Add income \n3. Do transfer \n4. Close account \n5. Log out \n0. Exit"""
        while True:
            print(logged_in_msg)
            user_choice_in_log_in = logged_in_menu[int(input())]
            if user_choice_in_log_in == 'balance':
                cur.execute(f"SELECT number, balance FROM card WHERE number = {user_card};")
                print('Balance: ', cur.fetchall()[0][1])
            elif user_choice_in_log_in == "Add income":
                cur.execute(f"SELECT number, balance FROM card WHERE number = {user_card};")
                print('Enter income:')
                add_income(int(input()), int(cur.fetchall()[0][1]), user_card)
            elif user_choice_in_log_in == 'Do transfer':
                print('Transfer')
                print('Enter card number:')
                card_num_for_transfer = input()
                if verify(str(card_num_for_transfer)):
                    cur.execute(f"SELECT number, balance FROM card WHERE number = {card_num_for_transfer};")
                    if cur.fetchall():
                        cur.execute(f"SELECT number, balance FROM card WHERE number = {user_card};")
                        current_balance = cur.fetchall()[0][1]
                        print('Enter how much money you want to transfer:')
                        transfer_amount = int(input())
                        if transfer_amount > current_balance:
                            print('Not enough money!')
                        else:
                            cur.execute(f'UPDATE card SET balance = balance + {transfer_amount} WHERE number = {card_num_for_transfer}')
                            cur.execute(f'UPDATE card SET balance = balance - {transfer_amount} WHERE number = {user_card}')
                            conn.commit()
                            print('Success!\n')
                    else:
                        print('Such a card does not exist.')
                else:
                    print("\nProbably you made mistake in card number. Please try again!\n")

            elif user_choice_in_log_in == 'Close account':
                cur.execute(f'DELETE FROM card WHERE number = {user_card}')
                conn.commit()
                print('The account has been closed!\n')
                break
            elif user_choice_in_log_in == 'Log out':
                print("You have successfully logged out!")
                break
            elif user_choice_in_log_in == 'Exit___':
                global user_choice
                user_choice = 'exit___'
                break

    # def luhn(self, pre_luhan):
    #
    #     c = 0
    #     summ = 0
    #     second = False
    #     length = len(pre_luhan);
    #     for i in range(length - 1, -1, -1):
    #         c = int(pre_luhan[i])
    #         if second == True:
    #             c = c * 2
    #         summ = summ + c / 10
    #         summ = summ + c % 10
    #         second = not second
    #     if summ % 10 == 0:
    #         return True
    #     return False
    def write_to_table(self, card_num, pin):
        cur.execute(f"INSERT into card (number, pin) VALUES({card_num}, '{pin}')")
        conn.commit()



def checksum(string):
    """
    Compute the Luhn checksum for the provided string of digits. Note this
    assumes the check digit is in place.
    """
    digits = list(map(int, string))
    odd_sum = sum(digits[-1::-2])
    even_sum = sum([sum(divmod(2 * d, 10)) for d in digits[-2::-2]])
    return (odd_sum + even_sum) % 10


def verify(string):
    """
    Check if the provided string of digits satisfies the Luhn checksum.
    >>> verify('356938035643809')
    True
    >>> verify('534618613411236')
    False
    """
    return (checksum(string) == 0)


def generate(string):
    """
    Generate the Luhn check digit to append to the provided string.
    >>> generate('35693803564380')
    9
    >>> generate('53461861341123')
    4
    """
    cksum = checksum(string + '0')
    return (10 - cksum) % 10


def append(string):
    """
    Append Luhn check digit to the end of the provided string.
    >>> append('53461861341123')
    '534618613411234'
    """
    return string + str(generate(string))


def bank():
    #stage_three() # initializing the sqlite table
    global user_choice
    break_all = 0
    cards = Cards()
    menu = {1: 'new_account', 2: 'log_in', 0: 'exit___'}
    while True:
        welcome_msg = """1. Create an account \n2. Log into account \n0. Exit"""
        print(welcome_msg)
        user_choice = menu[int(input())]
        # user_input = input("""
        # 1. Create an account
        # 2. Log into account
        # 0. Exit
        # """)
        if user_choice == 'new_account':
            cards.new_account()
        elif user_choice == 'log_in':
            cards.log_in()
        if user_choice == 'exit___':
            print("Bye!")
            exit()


def  create_card_table(cur, conn):
    create_card_table = f"""CREATE TABLE IF NOT EXISTS card (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    number TEXT,
    pin TEXT,
    balance INTEGER DEFAULT 0
    );"""
    cur.execute(create_card_table)

    # cur.execute("UPDATE card SET balance = 0 WHERE id = 1")
    conn.commit()


def clean_slate(cur, conn):
    try:
        cur.execute("DELETE FROM card")
        cur.execute(f"INSERT into card (number, pin, balance) VALUES(NULL, NULL, 0)")
        conn.commit()
    finally:
        pass
        # print('the table is now CLEAN!')


def initialize_record_system():
    # establishing the sql file and connection to it
    global conn
    global cur
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()

    try:
        create_card_table(cur, conn) # creating the card table
        # print('the table has been created !')
    except sqlite3.OperationalError:
        pass
        # print('the table exists!') # if the table exists allready

    clean_slate(cur, conn) # cleaning the table

    # sql options:
        # cur.execute('SOME SQL QUERY')
    # cur.fetchone()  # Returns the first row from the response
    # cur.fetchall()  # Returns all rows from the response
    # cur.execute('SOME SELECT QUERY')

if __name__ == "__main__":
    global cur
    global conn
    initialize_record_system()
    bank()
