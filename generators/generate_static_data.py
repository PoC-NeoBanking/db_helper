import random

import names

from database.orm_query import (
    get_all_ids_manual,
    add_user_manual,
    new_transaction_manual
)


def generate_random_users_manual(n, min_balance, max_balance):
    """
    Для ручної генерації юзерів(з допомогою консолі)

    :param n: к-сть генерацій
    :param min_balance: мінімальна сума балансу
    :param max_balance: максимальна сума балансу
    :return: None
    """
    for i in range(n):
        # print(f'user_{i}')
        ipn = random.randint(10000000, 99999999)
        balance = round(random.uniform(min_balance, max_balance), 2)
        first_name = names.get_first_name()
        last_name = names.get_last_name()
        add_user_manual(ipn=ipn, first_name=first_name, last_name=last_name, account_balance=balance)
    print('Generation of users DONE')


def generate_random_transaction_manual(n, user_id=None):
    """
    Для ручної генерації транзакцій(з допомогою консолі) для рандомних людей
    І такод для ручної генерації транзакцій для якоїсь окремої людини по його id, якщо воно є, інакше рандомні для всіх

    :param n: к-сть генерацій
    :param user_id: його id в бд або нічого не передавайте(OPTIONAL)
    :return: None
    """
    list_of_all_ids = get_all_ids_manual()

    is_none = False
    if user_id is None:
        is_none = True
        user_id = [random.choice(list_of_all_ids) for _ in range(n)]
    else:
        user_id = [user_id]

    for i in range(n):
        first_user_id = user_id[0]
        if is_none:
            first_user_id = user_id[i]
        random_number = random.randint(0, 1)
        second_user_id = random.choice(list_of_all_ids)

        if first_user_id == second_user_id:
            second_user_id = random.choice(list_of_all_ids)

        if random_number == 1:
            first_user_id, second_user_id = second_user_id, first_user_id

        new_transaction_manual(first_user_id, second_user_id)

    print('Generation of transaction DONE')
