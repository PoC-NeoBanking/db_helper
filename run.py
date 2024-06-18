from database.engine import create_db, drop_db
from database.orm_query import (
    add_user,
    add_transaction,
    get_user_by_ipn,
    get_all_users_with_transactions,
    delete_user_by_ipn,
    delete_transaction_by_id,

)

from database.tables import User, Transaction

def main():
    create_db()

    # drop_db()

    # add_user(ipn=11111111, first_name='John', last_name='Doe', account_balance=1500.00)
    # add_user(ipn=22222222, first_name='Alice', last_name='Johnson', account_balance=2500.00)
    # add_user(ipn=33333333, first_name='Bob', last_name='Brown', account_balance=1800.00)
    # add_user(ipn=44444444, first_name='Eve', last_name='White', account_balance=900.00)
    # add_user(ipn=55555555, first_name='Chris', last_name='Lee', account_balance=1200.00)
    # add_user(ipn=66666666, first_name='Emma', last_name='Davis', account_balance=2100.00)
    # add_user(ipn=77777777, first_name='Michael', last_name='Miller', account_balance=1750.00)
    # add_user(ipn=88888888, first_name='Sarah', last_name='Wilson', account_balance=1900.00)
    # add_user(ipn=99999999, first_name='Serj', last_name='Dii', account_balance=300.00)
    # add_user(ipn=10101010, first_name='Sophia', last_name='Moore', account_balance=2200.00)
    # add_user(ipn=12121212, first_name='David', last_name='Martinez', account_balance=1600.00)
    # add_user(ipn=13131313, first_name='Lily', last_name='Garcia', account_balance=1350.00)
    # add_user(ipn=14141414, first_name='Andrew', last_name='Lopez', account_balance=1950.00)
    # add_user(ipn=15151515, first_name='Olivia', last_name='Hernandez', account_balance=1400.00)
    # add_user(ipn=16161616, first_name='James', last_name='Gonzalez', account_balance=1650.00)
    # add_user(ipn=17171717, first_name='Mia', last_name='Perez', account_balance=2000.00)
    # add_user(ipn=18181818, first_name='Benjamin', last_name='Rodriguez', account_balance=2300.00)
    # add_user(ipn=19191919, first_name='Charlotte', last_name='Sanchez', account_balance=1250.00)
    # add_user(ipn=20202020, first_name='Logan', last_name='Ramirez', account_balance=2400.00)
    # add_user(ipn=21212121, first_name='Amelia', last_name='Torres', account_balance=1700.00)
    #
    # add_transaction(3, 7, transaction_amount=1500.00)
    # add_transaction(10, 15, transaction_amount=2200.00)
    # add_transaction(12, 18, transaction_amount=1600.00)
    # add_transaction(5, 9, transaction_amount=1200.00)
    # add_transaction(14, 19, transaction_amount=1400.00)
    # add_transaction(11, 17, transaction_amount=1950.00)
    # add_transaction(6, 13, transaction_amount=2100.00)
    # add_transaction(16, 20, transaction_amount=2000.00)
    # add_transaction(4, 8, transaction_amount=900.00)
    # add_transaction(1, 2, transaction_amount=2500.00)
    # add_transaction(10, 12, transaction_amount=1350.00)
    # add_transaction(15, 18, transaction_amount=1650.00)
    # add_transaction(7, 11, transaction_amount=1750.00)
    # add_transaction(3, 16, transaction_amount=2300.00)
    # add_transaction(9, 20, transaction_amount=1250.00)
    # add_transaction(13, 17, transaction_amount=2400.00)
    # add_transaction(5, 14, transaction_amount=1950.00)
    # add_transaction(8, 19, transaction_amount=1700.00)
    # add_transaction(2, 6, transaction_amount=1350.00)
    # add_transaction(4, 15, transaction_amount=1600.00)

    # get_user_by_ipn(17171717)
    # add_transaction(19, 22, transaction_amount=90000.00)
    # delete_user_by_ipn(11111111)
    # delete_transaction_by_id(1)
    get_all_users_with_transactions()


if __name__ == '__main__':
    main()
