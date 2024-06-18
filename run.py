from database.engine import create_db, drop_db
from database.tables import User, Transaction

from database.orm_query import (
    add_user,
    add_transaction,
    get_user_by_ipn,
    get_all_users_with_transactions,
    delete_user_by_ipn,
    delete_transaction_by_id,
    get_user_with_transactions,
    counts_of_users,
    counts_of_transactions
)

from generations.generate_static_data import generate_random_users, generate_random_transaction


def main():
    # create_db()  # створити бд

    # drop_db()  # видалити бд

    # generate_random_users(10_000, 0, 50_000)  # згенерувати 10_000 юзерів
    # generate_random_transaction(10_000)  # згенерувати 10_000 транзакцій до рандомних юзерів

    # get_all_users_with_transactions(100)  # вивести усі n юзерів, якщо не задати параметр, то усі виведуться
    counts_of_users()  # вивести к-сть усіх наяних узерів(просто число)
    counts_of_transactions()  # вивести к-сть усіх наявних транзакцій(просто число)
    pass


if __name__ == '__main__':
    main()
