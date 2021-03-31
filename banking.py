import random
import sqlite3

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS card(
id INTEGER,
number TEXT,
pin TEXT,
balance INTEGER
);''')
conn.commit()

n_1 = None
n_2 = None
balance = 0
id = 0
card_number_db = None
PIN_number_db = None


def main_menu():
    """открытие главного меню"""
    global n_1
    print('''1. Create an account
2. Log into account
0. Exit''')
    n_1 = int(input())
    if n_1 == 1:
        create_an_account()
    elif n_1 == 2:
        log_into_account()
    elif n_1 == 0:
        exit()


def secondary_menu():
    global n_2
    '''открытие второстепенного меню'''
    print('''1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit''')
    n_2 = int(input())
    if n_2 == 1:
        check_balance()
    elif n_2 == 2:
        add_income()
    elif n_2 == 3:
        do_transfer()
    elif n_2 == 4:
        close_account()
    elif n_2 == 5:
        log_out()
    elif n_2 == 0:
        exit()


def add_income():
    """положить деньги на счет"""
    global balance
    income = int(input('Enter income:'))
    balance += income
    add_dengi = balance, card_number_db
    cur.execute('''UPDATE card SET balance = ? WHERE number = ?''', add_dengi)
    conn.commit()
    print('Income was added!')
    secondary_menu()


def do_transfer():
    """перевести деньги на другой счет"""
    card_transfer = input('Enter card number:')
    list_card_transfer = list(card_transfer)
    check_spisok = []
    b = 0
    for i in range(0, len(list_card_transfer), 2):
        a = int(list_card_transfer[i]) * 2
        if a > 9:
            a -= 9
        check_spisok.append(a)
    for i in range(1, len(list_card_transfer), 2):
        check_spisok.append(list_card_transfer[i])
    for i in check_spisok:
        b += int(i)
    if b % 10 != 0:
        print('Probably you made a mistake in the card number. Please try again!')
        secondary_menu()
    else:
        cur.execute('''SELECT balance FROM card WHERE number = ?''', [card_transfer])
        kolvo_deneg_na_carte_ktoto = cur.fetchone()
        if kolvo_deneg_na_carte_ktoto is None:
            print('Such a card does not exist.')
            secondary_menu()
        else:
            cur.execute('''SELECT balance FROM card WHERE number = ?''', [card_number_db])
            kolvo_deneg_na_carte = cur.fetchone()
            money_transfer = int(input('Enter how much money you want to transfer:'))
            if kolvo_deneg_na_carte < (money_transfer,):
                print('Not enough money!')
                secondary_menu()
            else:
                dengi_na_cartu = money_transfer, card_transfer
                dengi_s_carty = money_transfer, card_number_db
                cur.execute('''UPDATE card SET balance = balance + ? WHERE number = ?''', dengi_na_cartu)
                cur.execute('''UPDATE card SET balance = balance - ? WHERE number = ?''', dengi_s_carty)
                conn.commit()
                print('Success!')
                secondary_menu()


def close_account():
    """Удалить карту(закрыть счет)"""
    cur.execute('''DELETE FROM card WHERE number = ?;
    ''', [card_number_db])
    conn.commit()
    print('The account has been closed!')
    main_menu()


def create_an_account():
    """создание аккаунта и генерация номера карты и PIN кода"""
    global id
    id += 1
    account_number = str(random.randrange(100000000, 999999999))
    spisok = []
    b = 0
    for i in range(0, 9, 2):
        a = int(account_number[i]) * 2
        if a > 9:
            a -= 9
        spisok.append(a)
    for i in range(1, 9, 2):
        spisok.append(account_number[i])
    for i in spisok:
        b += int(i)
    check_number = 10 - ((b + 8) % 10)
    if check_number == 10:
        check_number = 0
    PIN_number = (random.randrange(1000, 9999))
    card_number = ("400000" + str(account_number) + str(check_number))
    user = (id, card_number, PIN_number, balance)
    cur.execute('''INSERT INTO card
    VALUES(?, ?, ?, ?);''', user)
    conn.commit()
    print('''Your card has been created
Your card number:
{}
Your card PIN:
{}'''.format(card_number, PIN_number))
    main_menu()


def log_into_account():
    """проверка данных и вход в аккаунт"""
    global n_2, card_number_db, PIN_number_db
    user_card_number = input('Enter your card number:')
    user_PIN_number = input('Enter your PIN:')
    user_input = user_card_number, user_PIN_number
    cur.execute('''SELECT number, pin FROM card WHERE number = ? AND pin = ?;''', user_input)
    user_input = cur.fetchone()
    if user_input != None:
        card_number_db, PIN_number_db = user_input
    if user_card_number == card_number_db and user_PIN_number == PIN_number_db:
        print('You have successfully logged in!')
        secondary_menu()
    else:
        print('Wrong card number or PIN!')
        main_menu()


def check_balance():
    """проверка баланса"""
    cur.execute('''SELECT balance FROM card WHERE number = ?''', [card_number_db])
    print(cur.fetchone())
    secondary_menu()


def log_out():
    """выход из аккаунта"""
    global card_number_db, PIN_number_db, balance
    print('You have successfully logged out!')
    card_number_db = None
    PIN_number_db = None
    balance = 0
    main_menu()


def exit():
    '''выход из системы'''
    print('Buy!')
    conn.close()


main_menu()

