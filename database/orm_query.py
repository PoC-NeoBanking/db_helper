from database.tables import User, Transaction


def add_user(ipn, first_name, last_name, account_balance, Session):
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


def add_transaction(sender_id, receiver_id, transaction_amount, transaction_category, Session):
    """
    Add transaction

    Changed: максимальною суму переводу грошей з аккаунту задається наявна к-сть грошей на рахунку відправника
    І потім міняється баланс у відправника і отримувача, відносно радомною суми відправки
    """

    try:
        with Session.begin() as session:
            sender = session.query(User).filter_by(id=sender_id).first()
            receiver = session.query(User).filter_by(id=receiver_id).first()

            if sender and receiver:
                sender_account_balance = float(sender.account_balance) - transaction_amount
                receiver_account_balance = float(receiver.account_balance) + transaction_amount

                sender.account_balance = sender_account_balance
                receiver.account_balance = receiver_account_balance

                transaction = Transaction(
                    sender_id=sender_id,
                    receiver_id=receiver_id,
                    transaction_amount=transaction_amount,
                    transaction_category=transaction_category
                )
                session.add(transaction)

                # print(f"Transaction added: Sender {sender.first_name} {sender.last_name} "
                #       f"sent {transaction_amount} to Receiver {receiver.first_name} {receiver.last_name}")

            else:
                print("Sender or Receiver not found.")
    except Exception as e:
        session.rollback()
        print(f'Error adding transaction: {e}')


def get_user_by_ipn(ipn, Session):
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


def delete_user_by_ipn(ipn, Session):
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


def delete_transaction_by_id(transaction_id, Session):
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


def get_all_ipns(Session):
    """
    Get all ipn's of available users

    :return: List of all ipn's
    """

    with Session() as session:
        try:
            ipns = session.query(User.ipn).all()
            all_ipns = [ipn for (ipn,) in ipns]  # Повертаємо список інтегрованих значень ipn
            # print(all_ipns)
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
            all_ids = [id for (id,) in ids]
            return all_ids
        except Exception as e:
            session.rollback()
            print(f'Error retrieving IPNs: {e}')
            return []


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


def get_user_with_transactions(Session, ipn):
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
