import random
from datetime import datetime, timedelta

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


def generate_random_date(start=None, end=None):
    """
    Генерує випадкову дату у заданому проміжку

    :param start: Початок проміжку (нижче у змінній start - є потрібний вхідний формат дати)
    :param end: Кінець проміжку (нижче у змінній end - є потрібний вхідний формат дати)
    :return: Згенерована дата, у потрібному форматі
    """
    if not start:
        start = "2023-01-01T00:00:00.000000"
        end = "2024-01-01T00:00:00.000000"

    start_date = datetime.strptime(start, '%Y-%m-%dT%H:%M:%S.%f')
    end_date = datetime.strptime(end, '%Y-%m-%dT%H:%M:%S.%f')

    random_seconds = random.uniform(0, (end_date - start_date).total_seconds())
    random_date = start_date + timedelta(seconds=random_seconds)

    return random_date.isoformat()


def generate_random_transaction(Session, n, from_date=None, to_date=None,user=None, user_ipn=None):
    """
    Для генерації транзакцій(з допомогою консолі) для рандомних людей
    І такод для генерації транзакцій для якоїсь окремої людини по його id чи ipn, якщо воно є, інакше рандомні для всіх
    Якщо є і ipn і id, то працюватиме по ipn

    :param Session: сесія потрібна для роботи з бд
    :param n: к-сть генерацій
    :param from_date: початок проміжку дати
    :param to_date: кінець проміжку дати
    :param user: id юзера в бд або нічого не передавайте(OPTIONAL)
    :param user_ipn: ipn юзера
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

        generated_date = generate_random_date(start=from_date, end=to_date)
        new_transaction(Session, first_user, second_user, transaction_date=generated_date, is_ipn=is_ipn)
