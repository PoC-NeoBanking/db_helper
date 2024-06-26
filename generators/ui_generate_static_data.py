import random

import names

from database.ui_orm_query import (
    get_all_ids,
    add_user,
    new_transaction,
    get_all_ipns
)


def generate_random_users(Session, n, min_balance, max_balance):
    """
    Для генерації юзерів

    :param Session: сесія потрібна для роботи з бд
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
        add_user(Session=Session, ipn=ipn, first_name=first_name, last_name=last_name, account_balance=balance)
    print('Generation of users DONE')


def generate_random_transaction(Session, n, user=None, user_ipn=None):
    """
    Для генерації транзакцій(з допомогою консолі) для рандомних людей
    І такод для генерації транзакцій для якоїсь окремої людини по його id чи ipn, якщо воно є, інакше рандомні для всіх
    Якщо є і ipn і id, то працюватиме по ipn

    :param Session: сесія потрібна для роботи з бд
    :param n: к-сть генерацій
    :param user: його id в бд або нічого не передавайте(OPTIONAL)
    :param user_ipn:
    :return: None
    """
    list_of_all_ids = get_all_ids(Session)
    list_of_all_ipns = get_all_ipns(Session)

    is_ipn = False
    is_none = False
    if user is None and user_ipn is None:
        is_none = True
        user = [random.choice(list_of_all_ids) for _ in range(n)]
    elif user:
        user = [user]
    else:
        is_ipn = True
        user = [user_ipn]

    random_lst = list_of_all_ids if is_ipn is False else list_of_all_ipns
    for i in range(n):
        first_user = user[0]
        if is_none:
            first_user = user[i]
        random_number = random.randint(0, 1)
        second_user = random.choice(random_lst)

        if first_user == second_user:
            second_user = random.choice(random_lst)

        if random_number == 1:
            first_user, second_user = second_user, first_user
        new_transaction(Session, first_user, second_user, is_ipn=True)

    print('Generation of transaction DONE')
