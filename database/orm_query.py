from database.tables import User, Transaction


def add_user(ipn, first_name, last_name, account_balance, Session):
    user = User(ipn=ipn, first_name=first_name, last_name=last_name, account_balance=account_balance)
    try:
        with Session.begin() as session:
            session.add(user)
    except Exception as e:
        session.rollback()
        print(f'Error adding user: {e}')
        return e


def add_transaction(sender_id, receiver_id, transaction_amount, transaction_category, Session):
    transaction = Transaction(sender_id=sender_id, receiver_id=receiver_id, transaction_amount=transaction_amount,
                              transaction_category=transaction_category)
    try:
        with Session.begin() as session:
            session.add(transaction)
    except Exception as e:
        session.rollback()
        print(f'Error adding transaction: {e}')
        return e


def get_all_users_with_transactions(Session):
    with Session() as session:
        users = session.query(User).all()
        for number, user in enumerate(users):
            print(f"{number + 1}. User_{user.id}: {user.first_name} {user.last_name}, IPN: {user.ipn}")

            transactions = session.query(Transaction).filter(
                (Transaction.sender_id == user.id) | (Transaction.receiver_id == user.id)).all()

            for index, transaction in enumerate(transactions):
                sender = session.query(User).filter_by(id=transaction.sender_id).first()
                receiver = session.query(User).filter_by(id=transaction.receiver_id).first()

                print(f"    {index + 1}) Transaction ID: {transaction.id}, Amount: {transaction.transaction_amount}")
                print(f"    Sender: {sender.first_name} {sender.last_name}, "
                      f"Receiver: {receiver.first_name} {receiver.last_name}")
            print()


def get_user_by_ipn(ipn, Session):
    with Session() as session:
        user = session.query(User).filter_by(ipn=ipn).first()

    if not user:
        print(f"User with IPN {ipn} not found.")
        return None
    print(user.id, user.first_name)
    return user


def delete_user_by_ipn(ipn, Session):
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
    with Session() as session:
        try:
            ids = session.query(User.id).all()
            all_ids = [id for (id,) in ids]  # Повертаємо список інтегрованих значень ipn
            # print(all_ipns)
            return all_ids
        except Exception as e:
            session.rollback()
            print(f'Error retrieving IPNs: {e}')
            return []
