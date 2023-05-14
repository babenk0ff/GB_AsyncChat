"""Написать функцию host_ping(), в которой с помощью утилиты ping будет
проверяться доступность сетевых узлов. Аргументом функции является список,
в котором каждый сетевой узел должен быть представлен именем хоста или
ip-адресом. В функции необходимо перебирать ip-адреса и проверять их
доступность с выводом соответствующего сообщения («Узел доступен»,
«Узел недоступен»). При этом ip-адрес сетевого узла должен создаваться с
помощью функции ip_address()."""

import ipaddress
import os
import subprocess


def host_ping(host_list):
    results = {
        'Reachable': [],
        'Unreachable': [],
    }

    for host in host_list:
        try:
            ip = ipaddress.ip_address(host)
        except ValueError:
            ip = host

        if os.name == 'nt':
            command = ['ping', '-n', '1', '-w', '200', str(ip)]
        else:
            command = ['ping', '-c', '1', '-i', '0.2', str(ip)]

        ping_result = subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        if ping_result.returncode == 0:
            results['Reachable'].append(ip)
            print(f'{ip} - Узел доступен')
        else:
            results['Unreachable'].append(ip)
            print(f'{ip} - Узел недоступен')

    return results


if __name__ == '__main__':
    hosts = [
        '127.0.0.1',
        '8.8.8.8',
        'google.com',
        'wrong.addr',
    ]

    host_ping(hosts)
