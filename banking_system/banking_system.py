from random import randint
import sqlite3

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
cur.execute(
    "CREATE TABLE IF NOT EXISTS card (id INTEGER PRIMARY KEY AUTOINCREMENT, number TEXT, pin TEXT, balance INTEGER "
    "DEFAULT 0)")


def start():
    global balance_logout
    balance_logout = 1
    while True:
        print("""1. Create an account
2. Log into account
0. Exit""")
        create_login = int(input())
        print('')

        if create_login == 1:
            create_account()
        elif create_login == 2:
            log_in()
        elif create_login == 0:
            break
        if balance_logout == 0:
            break


def check_luhn(num):
    check = int(str(num)[-1])
    num_list = [int(x) for x in str(num)[0:15]]
    for i in range(len(num_list)):
        if (i + 1) % 2 == 1:
            num_list[i] *= 2
        if num_list[i] > 9:
            num_list[i] -= 9
    luhn = (sum(num_list) + check)
    if luhn % 10 == 0:
        return True
    else:
        return False


def create_account():
    account = "400000"
    password = ""
    cumulative_num = 8
    for i in range(0, 9):
        random_num = randint(0, 9)
        account += str(random_num)
        if i % 2 == 0:
            if random_num > 4:
                cumulative_num += random_num * 2 - 9
            else:
                cumulative_num += random_num * 2
        else:
            cumulative_num += random_num
    account += str((10 - cumulative_num % 10) % 10)
    for i in range(0, 4):
        password += str(randint(0, 9))
    cur.execute("INSERT INTO card (number, pin) VALUES (?,?)", (account, password))
    conn.commit()
    print(f'''Your card has been created
Your card number:
{account}
Your card PIN:
{password}
''')


def log_in():
    print('Enter your card number:')
    log_account = input()
    print('Enter your PIN:')
    log_password = input()
    cur.execute("SELECT number, pin  FROM card WHERE number=?", (log_account,))
    records = cur.fetchall()
    print('')
    if not records:
        print('Wrong card number or PIN!\n')
    else:
        if log_account == records[0][0] and log_password == records[0][1]:
            print('You have successfully logged in!\n')
            account_management(log_account)
        else:
            print('Wrong card number or PIN!\n')


def account_management(log_account):
    while True:
        global balance_logout
        print('''1. Balance \n2. Add income \n3. Do transfer \n4. Close account \n5. Log out \n0. Exit''')
        balance_logout = int(input())
        print('')
        if balance_logout == 1:
            cur.execute("SELECT balance FROM card WHERE number=?", (log_account,))
            balance = (cur.fetchall())[0][0]
            print(f'Balance: {balance}\n')
        if balance_logout == 2:
            enter_income(log_account)
        if balance_logout == 3:
            do_transference(log_account)
        if balance_logout == 4:
            close_account(log_account)
            break
        if balance_logout == 5:
            print('\nYou have successfully logged out!\n')
            break
        if balance_logout == 0:
            break


def enter_income(log_account):
    print('Enter income:')
    income = int(input())
    cur.execute("SELECT balance FROM card WHERE number=?", (log_account,))
    new_balance = (cur.fetchall())[0][0] + income
    cur.execute("UPDATE card SET balance = ? WHERE number=?", (new_balance, log_account,))
    conn.commit()
    print('Income was added!')


def do_transference(log_account):
    print("\n Transfer")
    print("Enter card number:")
    transfer_account = input()
    cur.execute("SELECT balance FROM card WHERE number=?", (log_account,))
    balance = (cur.fetchall())[0][0]
    if log_account == transfer_account:
        print("You can't transfer money to the same account!")
    elif check_luhn(int(transfer_account)) is False:
        print("Probably you made mistake in the card number. Please try again!\n")
    else:
        cur.execute("SELECT number FROM card")
        accounts = (cur.fetchall())
        accounts = [i[0] for i in accounts]
        if transfer_account not in accounts:
            print("Such a card does not exist.")
        else:
            print("Enter how much money you want to transfer:")
            transfer_money = int(input())
            if (balance - transfer_money) <= 0:
                print('Not enough money!')
            else:
                new_balance = balance - transfer_money
                cur.execute("UPDATE card SET balance = ? WHERE number=?", (new_balance, log_account,))
                conn.commit()
                cur.execute("SELECT balance FROM card WHERE number=?", (transfer_account,))
                new_balance2 = (cur.fetchall())[0][0] + transfer_money
                cur.execute("UPDATE card SET balance = ? WHERE number=?", (new_balance2, transfer_account,))
                conn.commit()
                print('Success!\n')


def close_account(log_account):
    cur.execute("SELECT balance FROM card WHERE number=?", (log_account,))
    cur.execute("DELETE FROM card WHERE number=?", (log_account,))
    conn.commit()
    print('The account has been closed!\n')


start()

print('Bye!')