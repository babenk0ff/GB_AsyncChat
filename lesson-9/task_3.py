"""Написать функцию host_range_ping_tab(), возможности которой основаны на
функции из примера 2. Но в данном случае результат должен быть итоговым по
всем ip-адресам, представленным в табличном формате (использовать модуль
tabulate). Таблица должна состоять из двух колонок"""

from tabulate import tabulate
from task_2 import host_range_ping


def host_range_ping_tab(start, end):
    result = host_range_ping(start, end)
    print('\n', tabulate(result, headers='keys', stralign='center'))


if __name__ == '__main__':
    host_range_ping_tab('192.168.1.1', '192.168.1.4')
