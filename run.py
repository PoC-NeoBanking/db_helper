from database.engine import create_db, drop_db
from database.tables import User, Transaction

from database.orm_query import (
    add_user,
    add_transaction,
    get_user_by_ipn,
    get_all_users_with_transactions,
    delete_user_by_ipn,
    delete_transaction_by_id,
)

from generations.generate_static_data import generate_random_users, generate_random_transaction

def main():
    create_db()

    # drop_db()

    generate_random_users(100, 0, 50_000)
    generate_random_transaction(100, 0, 5_000)

    get_all_users_with_transactions()


if __name__ == '__main__':
    main()
