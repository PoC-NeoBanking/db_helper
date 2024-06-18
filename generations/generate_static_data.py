import random
import names

from database.tables import list_categories
from database.orm_query import get_all_ids
from database.orm_query import (
    add_user,
    add_transaction,
)

def generate_random_users(n, min_balance, max_balance):
    for i in range(n):
        print(f'user_{i}')
        ipn = random.randint(10000000, 99999999)
        balance = round(random.uniform(min_balance, max_balance), 2)
        first_name = names.get_first_name()
        last_name = names.get_last_name()
        add_user(ipn=ipn, first_name=first_name, last_name=last_name, account_balance=balance)


def generate_random_transaction(n, min_balance, max_balance):
    list_of_all_ids = get_all_ids()
    for i in range(n):
        print(f'transaction_{i}')
        sender = random.choice(list_of_all_ids)
        receiver = random.choice(list_of_all_ids)
        if sender == receiver:
            sender = random.choice(list_of_all_ids)
        sum_of_transaction = round(random.uniform(min_balance, max_balance), 2)
        category = random.choice(list_categories)
        add_transaction(sender, receiver, transaction_amount=sum_of_transaction, transaction_category=category)
