import json
import os
import random
from datetime import datetime, date
from decimal import Decimal

import yaml
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database.tables import User, Transaction, list_categories


def get_all_ipns(Session):
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


def get_all_ids(Session):
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


def add_user(Session, ipn, first_name, last_name, account_balance):
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


def add_transaction(Session, sender_identificator, receiver_identificator, transaction_amount, transaction_category, is_ipn=False):
    """
    Add transaction

    Changed: максимальною суму переводу грошей з аккаунту задається наявна к-сть грошей на рахунку відправника
    І потім міняється баланс у відправника і отримувача, відносно радомною суми відправки
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

                transaction = Transaction(
                    sender_id=sender_identificator,
                    receiver_id=receiver_identificator,
                    transaction_amount=transaction_amount,
                    transaction_category=transaction_category
                )
                session.add(transaction)
            else:
                print("Sender or Receiver not found.")
    except Exception as e:
        session.rollback()
        print(f'Error adding transaction: {e}')


def new_transaction(Session, sender, receiver, sum_of_transaction=None, is_ipn=False):
    """
    Add new transaction from sender to reciever

    :param Session: session for db
    :param sender: sender id
    :param receiver: receiver id
    :param sum_of_transaction: sum of transaction
    :param is_ipn: False OPTIONAL - if it's ipn or not
    """
    # print(sender, receiver, is_ipn)
    with Session() as session:
        if is_ipn:
            user = session.query(User).filter_by(ipn=sender).first()
        else:
            user = session.query(User).filter_by(id=sender).first()
        max_balance = user.account_balance
    if not user:
        return
    if sum_of_transaction is None:
        sum_of_transaction = round(random.uniform(0, int(max_balance)), 2)
    category = random.choice(list_categories)
    add_transaction(Session, sender, receiver, transaction_amount=sum_of_transaction, transaction_category=category, is_ipn=is_ipn)


def get_user_by_ipn(Session, ipn):
    """
    Get user by its ipn

    :return: user: type(User)
    """

    with Session() as session:
        user = session.query(User).filter_by(ipn=ipn).first()

    if not user:
        print(f"User with IPN {ipn} not found.")
        return None
    # print(user.id, user.first_name)
    return user


def delete_user_by_ipn(Session, ipn):
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


def delete_transaction_by_id(Session, transaction_id):
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


def get_all_users_with_transactions(Session, limit=-1):
    """
    Get all user and its transactions

    :param: limit - к-сть юзерів, які мають вивестися, дефолтне значення = усі
    """

    if limit == -1:
        limit = len(get_all_ids(Session))
    with Session() as session:
        users = session.query(User).limit(limit).all()
        for number, user in enumerate(users):
            print(
                f"{number + 1}. User_{user.id}: {user.first_name} {user.last_name}, IPN: {user.ipn}, "
                f"Balance: {user.account_balance}")

            transactions = session.query(Transaction).filter(
                (Transaction.sender_id == user.id) | (Transaction.receiver_id == user.id)).all()

            print(len(transactions))
            # for index, transaction in enumerate(transactions):
            #     sender = session.query(User).filter_by(id=transaction.sender_id).first()
            #     receiver = session.query(User).filter_by(id=transaction.receiver_id).first()
            #
            #     print(f"    {index + 1}) Transaction ID: {transaction.id}, Amount: {transaction.transaction_amount}")
            #     print(f"    Sender: {sender.first_name} {sender.last_name}, "
            #           f"Receiver: {receiver.first_name} {receiver.last_name}, "
            #           f"Category: {transaction.transaction_category}")
            # print()


def get_user_with_transactions_by_ipn(Session, ipn):
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


def counts_of_users(Session):
    """
    Count of all users(only number)

    :return: number of all users
    """

    with Session() as session:
        user_count = session.query(User).count()
        print(user_count)
        return user_count


def counts_of_transactions(Session):
    """
    Count of all transactions(only number)

    :return: number of all transactions
    """

    with Session() as session:
        transaction_count = session.query(Transaction).count()
        print(transaction_count)
        return transaction_count


def save_to_yaml_together(Session):
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

    print("SUCCESS, saved all data in yalm TOGETHER")


def save_to_yaml_separately(Session):
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
    print("SUCCESS, saved all data in yalm SEPARATELY")


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


def save_to_json_together(Session):
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


def save_to_json_separately(Session):
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


def all_users(Session, limit=10):
    with Session() as session:
        users = session.query(User).all()
        data = []
        for user in users:
            user_data = f"ID: {user.id}, IPN: {user.ipn}, Name: {user.first_name} {user.last_name}, Balance: {float(user.account_balance)}"
            data.append(user_data)
    print("Showed successfully")
    return data


def all_transactions(Session):
    with Session() as session:
        transactions = session.execute(select(Transaction)).scalars().all()
        data = []
        for transaction in transactions:
            transaction_data = f"ID: {transaction.id}, Sender ID: {transaction.sender_id}, Receiver ID: {transaction.receiver_id}, Amount: {float(transaction.transaction_amount)}, Category: {transaction.transaction_category}"
            data.append(transaction_data)
    print("Showed successfully")
    return data


def show_user_with_transactions(Session, user_id, user_ipn):
    """
    Повертає детальну інфу користувача і всі його транзакції по ID i IPN
    Якщо є обоє, то по ID

    :param Session: - cecія
    :param user_id: - ID користувача OPTIONAL
    :param user_ipn: - код IPN користувача
    """
    if user_id == '' and user_ipn == '':
        return []
    elif user_id:
        with Session() as session:
            user = session.query(User).filter_by(id=user_id).first()
    elif user_ipn:
        with Session() as session:
            user = session.query(User).filter_by(ipn=user_ipn).first()

    all_data = []
    with Session() as session:
        all_data.append(f"User_{user.id}: {user.first_name} {user.last_name} {user.middle_name}, IPN: {user.ipn}, ")
        all_data.append(
            f'Account balance: {user.account_balance}, Last activity: {user.last_activity}, Fraudster: {user.detected_fraudster}')
        transactions = session.query(Transaction).filter(
            (Transaction.sender_id == user.id) | (Transaction.receiver_id == user.id)).all()
        all_data.append(f'TRANSACTIONS {len(transactions)}:')

    for index, transaction in enumerate(transactions):
        sender = session.query(User).filter_by(id=transaction.sender_id).first()
        receiver = session.query(User).filter_by(id=transaction.receiver_id).first()

        all_data.append(
            f"    {index + 1}. ID: {transaction.id}, Sum: {transaction.transaction_amount}, Date: {transaction.transaction_date}")
        all_data.append(
            f"    From_{transaction.sender_id}: {sender.first_name} {sender.last_name}, To_{transaction.receiver_id}: {receiver.first_name} {receiver.last_name}"
            f", Category: {transaction.transaction_category}")
    return all_data


def show_details_of_transaction(Session, transaction_id):
    """
    Повертає детальну інформацію про транзакцію по її ID

    :param Session: сесія
    :param transaction_id: ID транзакції
    """

    if transaction_id == '':
        return []

    all_data = []
    with Session() as session:
        transaction = session.query(Transaction).filter_by(id=transaction_id).first()

        sender = session.query(User).filter_by(id=transaction.sender_id).first()
        receiver = session.query(User).filter_by(id=transaction.receiver_id).first()

        all_data.append(f"Transaction_{transaction.id}: Sum: {transaction.transaction_amount}")
        all_data.append(
            f"From_{transaction.sender_id}: {sender.first_name} {sender.last_name}, To_{transaction.receiver_id}: {receiver.first_name} {receiver.last_name}")
        all_data.append(f"Category: {transaction.transaction_category}, Date: {transaction.transaction_date}")

    return all_data
