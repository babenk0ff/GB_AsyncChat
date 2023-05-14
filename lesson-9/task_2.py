"""Написать функцию host_range_ping() для перебора ip-адресов из заданного
диапазона. Меняться должен только последний октет каждого адреса. По
результатам проверки должно выводиться соответствующее сообщение."""

from ipaddress import ip_address

from task_1 import host_ping


def host_range_ping(start, end):
    try:
        start_ip = ip_address(start)
        end_ip = ip_address(end)
    except ValueError as e:
        print('Неверный формат IP-адреса: {}'.format(str(e).split(sep=" ")[0]))
        return

    start_s, start_ip_oct = start.rsplit('.', maxsplit=1)
    end_s, end_ip_oct = end.rsplit('.', maxsplit=1)

    if start_s != end_s:
        print(f'IP-адреса {start_ip} и {end_ip} отличаются '
              f'не только последним октетом')
        return
    elif end_ip_oct < start_ip_oct:
        print(f'Обратная последовательность адресов')
        return

    hosts = map(str, [start_ip + i for i
                      in range(int(end_ip_oct) - int(start_ip_oct) + 1)])

    return host_ping(hosts)


if __name__ == '__main__':
    host_range_ping('192.168.1.1', '192.168.1.15')
