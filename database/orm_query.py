import json
import os
import random
from datetime import datetime, date
from decimal import Decimal

import yaml
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database.engine import Session
from database.tables import User, Transaction, list_categories


def get_user_by_ipn_manual(ipn):
    """
    Get user by its ipn

    :return: user: type(User)
    """

    with Session() as session:
        user = session.query(User).filter_by(ipn=ipn).first()

    if not user:
        print(f"User with IPN {ipn} not found.")
        return None
    print(user.id, user.first_name)
    return user


def delete_user_by_ipn_manual(ipn):
    """
    Delete user by its ipn
    """

    with Session() as session:
        try:
            user_to_delete = session.query(User).filter(User.ipn == ipn).first()
            if user_to_delete:
                session.delete(user_to_delete)
                session.commit()
                print(f"User with IPN {ipn} deleted successfully.")
            else:
                print(f"User with IPN {ipn} not found.")
        except Exception as e:
            session.rollback()
            print(f"Error deleting user: {e}")


def delete_transaction_by_id_manual(transaction_id):
    """
    Delete transaction by its id
    """

    with Session() as session:
        try:
            transaction_to_delete = session.query(Transaction).filter_by(id=transaction_id).first()
            if transaction_to_delete:
                session.delete(transaction_to_delete)
                session.commit()
                print(f"Transaction with ID {transaction_id} deleted successfully.")
            else:
                print(f"Transaction with ID {transaction_id} not found.")
        except Exception as e:
            session.rollback()
            print(f"Error deleting transaction: {e}")


def get_all_ipns_manual():
    """
    Get all ipn's of available users

    :return: List of all ipn's
    """

    with Session() as session:
        try:
            ipns = session.query(User.ipn).all()
            all_ipns = [ipn for (ipn,) in ipns]
            return all_ipns
        except Exception as e:
            session.rollback()
            print(f'Error retrieving IPNs: {e}')
            return []


def get_all_ids_manual():
    """
    Get all id's of available users

    :return: List of all id's
    """

    with Session() as session:
        try:
            ids = session.query(User.id).all()
            all_ids = [id_ for (id_,) in ids]
            return all_ids
        except Exception as e:
            session.rollback()
            print(f'Error retrieving IPNs: {e}')
            return []


def add_user_manual(ipn, first_name, last_name, account_balance):
    """
    Add user
    """

    user = User(ipn=ipn, first_name=first_name, last_name=last_name, account_balance=account_balance)
    try:
        with Session.begin() as session:
            session.add(user)
    except Exception as e:
        session.rollback()
        print(f'Error adding user: {e}')
        return e


def add_transaction_manual(sender_identificator, receiver_identificator, transaction_amount, transaction_category,
                           transaction_date=None, is_ipn=False):
    """
    Add transaction

    Changed: максимальною суму переводу грошей з аккаунту задається наявна к-сть грошей на рахунку відправника
    І потім міняється баланс у відправника і отримувача, відносно радомною суми відправки
    Те саме з датою
    """

    try:
        with Session.begin() as session:
            if is_ipn:
                sender = session.query(User).filter_by(ipn=sender_identificator).first()
                sender_identificator = sender.id
                receiver = session.query(User).filter_by(ipn=receiver_identificator).first()
                receiver_identificator = receiver.id
            else:
                sender = session.query(User).filter_by(id=sender_identificator).first()
                receiver = session.query(User).filter_by(id=receiver_identificator).first()

            if sender and receiver:
                sender.account_balance = float(sender.account_balance) - transaction_amount
                receiver.account_balance = float(receiver.account_balance) + transaction_amount

                if not transaction_date:
                    transaction = Transaction(
                        sender_id=sender_identificator,
                        receiver_id=receiver_identificator,
                        transaction_amount=transaction_amount,
                        transaction_category=transaction_category
                    )
                else:
                    transaction = Transaction(
                        sender_id=sender_identificator,
                        receiver_id=receiver_identificator,
                        transaction_amount=transaction_amount,
                        transaction_category=transaction_category,
                        transaction_date=transaction_date
                    )
                session.add(transaction)
            else:
                print("Sender or Receiver not found.")
    except Exception as e:
        session.rollback()
        print(f'Error adding transaction: {e}')


def new_transaction_manual(sender, receiver, sum_of_transaction=None):
    """
    Add new transaction from sender to reciever

    :param sender: sender id
    :param receiver: receiver id
    :param sum_of_transaction: sum of transaction
    """

    with Session() as session:
        user = session.query(User).filter_by(id=sender).first()
        max_balance = user.account_balance
    if not user:
        return
    if sum_of_transaction is None:
        sum_of_transaction = round(random.uniform(0, int(max_balance)), 2)
    category = random.choice(list_categories)
    add_transaction_manual(sender, receiver, transaction_amount=sum_of_transaction, transaction_category=category)


def get_all_users_with_transactions_manual(limit=-1):
    """
    Get all user and its transactions

    :param: limit - к-сть юзерів, які мають вивестися, дефолтне значення = усі
    """
    if limit == -1:
        limit = len(get_all_ids_manual())
    with Session() as session:
        users = session.query(User).limit(limit).all()
        for number, user in enumerate(users):
            print(
                f"{number + 1}. User_{user.id}: {user.first_name} {user.last_name}, IPN: {user.ipn}, "
                f"Balance: {user.account_balance}")

            transactions = session.query(Transaction).filter(
                (Transaction.sender_id == user.id) | (Transaction.receiver_id == user.id)).all()

            print(len(transactions))


def get_user_with_transactions_by_ipn_manual(ipn):
    """
    Get all transactions of one user by its IPN

    :param: ipn -  код IPN
    """

    with Session() as session:
        user = session.query(User).filter_by(ipn=ipn).first()
    print(
        f"User_{user.id}: {user.first_name} {user.last_name}, IPN: {user.ipn}, "
        f"Balance: {user.account_balance}")

    transactions = session.query(Transaction).filter(
        (Transaction.sender_id == user.id) | (Transaction.receiver_id == user.id)).all()

    for index, transaction in enumerate(transactions):
        sender = session.query(User).filter_by(id=transaction.sender_id).first()
        receiver = session.query(User).filter_by(id=transaction.receiver_id).first()

        print(f"    {index + 1}) Transaction ID: {transaction.id}, Amount: {transaction.transaction_amount}")
        print(f"    Sender: {sender.first_name} {sender.last_name}, "
              f"Receiver: {receiver.first_name} {receiver.last_name}, "
              f"Category: {transaction.transaction_category}")
    print(f'Count of all transactions: {len(transactions)}')


def counts_of_users_manual():
    """
    Count of all users(only number)

    :return: number of all users
    """

    with Session() as session:
        user_count = session.query(User).count()
        print(user_count)
        return user_count


def counts_of_transactions_manual():
    """
    Count of all transactions(only number)

    :return: number of all transactions
    """

    with Session() as session:
        transaction_count = session.query(Transaction).count()
        print(transaction_count)
        return transaction_count


def save_to_yaml_together_manual():
    """
    Save all users in one yaml file
    Save these files in 'data' folder in separated folders as 'users' and 'transactions'

    :return: None
    """
    os.makedirs('data/users', exist_ok=True)
    os.makedirs('data/transactions', exist_ok=True)

    with Session() as session:
        users = session.execute(select(User)).scalars().all()
        users_data = [user.__dict__ for user in users]
        for user in users_data:
            user.pop('_sa_instance_state', None)

        with open('data/users/users.yaml', 'w') as file:
            yaml.dump(users_data, file, default_flow_style=False, allow_unicode=True)

        transactions = session.execute(select(Transaction)).scalars().all()
        transactions_data = [transaction.__dict__ for transaction in transactions]
        for transaction in transactions_data:
            transaction.pop('_sa_instance_state', None)

        with open('data/transactions/transactions.yaml', 'w') as file:
            yaml.dump(transactions_data, file, default_flow_style=False, allow_unicode=True)

    print("SUCCESS, saved all data in yaml TOGETHER")


def save_to_yaml_separately_manual():
    """
    Save all users and all transactions in different yaml files separately
    Save these files in 'data' folder in separated folders as 'users' and 'transactions'

    :return: None
    """

    os.makedirs('data/users', exist_ok=True)
    os.makedirs('data/transactions', exist_ok=True)

    with Session() as session:
        users = session.execute(select(User).options(
            selectinload(User.transactions)
        )).scalars().all()

        for user in users:
            user_data = user.__dict__.copy()
            user_data.pop('_sa_instance_state', None)

            transactions_data = []
            for transaction in user.transactions:
                transaction_data = transaction.__dict__.copy()
                transaction_data.pop('_sa_instance_state', None)
                transactions_data.append(transaction_data)

                with open(f'data/transactions/transaction_{transaction.id}.yaml', 'w') as file:
                    yaml.dump(transaction_data, file, default_flow_style=False, allow_unicode=True)

            user_data['transactions'] = transactions_data

            with open(f'data/users/user_{user.id}.yaml', 'w') as file:
                yaml.dump(user_data, file, default_flow_style=False, allow_unicode=True)
    print("SUCCESS, saved all data in yaml SEPARATELY")


def serialize_data(obj):
    """
    Use to convert decimal int in float

    :return: needed type of obj
    """

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    elif isinstance(obj, Decimal):
        return float(obj)
    raise TypeError(f"Type {type(obj)} not serializable")


def save_to_json_together_manual():
    """
    Save all users in one json file
    Save these files in 'data' folder in separated folders as 'users' and 'transactions'

    :return: None
    """

    os.makedirs('data/users', exist_ok=True)
    os.makedirs('data/transactions', exist_ok=True)

    with Session() as session:
        users = session.execute(select(User)).scalars().all()
        users_data = [user.__dict__.copy() for user in users]
        for user in users_data:
            user.pop('_sa_instance_state', None)

        with open('data/users/users.json', 'w') as file:
            json.dump(users_data, file, ensure_ascii=False, indent=4, default=serialize_data)

        transactions = session.execute(select(Transaction)).scalars().all()
        transactions_data = [transaction.__dict__.copy() for transaction in transactions]
        for transaction in transactions_data:
            transaction.pop('_sa_instance_state', None)

        with open('data/transactions/transactions.json', 'w') as file:
            json.dump(transactions_data, file, ensure_ascii=False, indent=4, default=serialize_data)
    print("SUCCESS, saved all data in json TOGETHER")


def save_to_json_separately_manual():
    """
    Save all users and all transactions in different json files separately
    Save these files in 'data' folder in separated folders as 'users' and 'transactions'

    :return: None
    """
    os.makedirs('data/users', exist_ok=True)
    os.makedirs('data/transactions', exist_ok=True)

    with Session() as session:
        users = session.execute(select(User).options(
            selectinload(User.transactions)
        )).scalars().all()

        for user in users:
            user_data = user.__dict__.copy()
            user_data.pop('_sa_instance_state', None)

            transactions_data = []
            for transaction in user.transactions:
                transaction_data = transaction.__dict__.copy()
                transaction_data.pop('_sa_instance_state', None)
                transactions_data.append(transaction_data)

                with open(f'data/transactions/transaction_{transaction.id}.json', 'w') as file:
                    json.dump(transaction_data, file, ensure_ascii=False, indent=4, default=serialize_data)

            user_data['transactions'] = transactions_data

            with open(f'data/users/user_{user.id}.json', 'w') as file:
                json.dump(user_data, file, ensure_ascii=False, indent=4, default=serialize_data)
    print("SUCCESS, saved all data in json SEPARATELY")
