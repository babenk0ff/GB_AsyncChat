import argparse
import socket
import time

from common.utils import parse_message, prepare_dispatch
from common.validators import ValidateAddress, ValidatePort


def get_args():
    parser = argparse.ArgumentParser(description='Запуск клиента')
    parser.add_argument('host', type=str, action=ValidateAddress,
                        help='IP-адрес сервера')
    parser.add_argument('port', nargs='?', type=int, default=7777,
                        action=ValidatePort, help='Номер порта сервера')
    args = parser.parse_args()
    return args.host, args.port


def make_presence():
    msg = {
        'action': 'presence',
        'time': time.time(),
        'user': {
            'account_name': 'C0deMaver1ck',
            'status': 'Yep, I am here!'
        }
    }
    return msg


def main():
    host, port = get_args()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))
        sock.send(prepare_dispatch(make_presence()))

        server_response = sock.recv(1024)
        parsed_message = parse_message(server_response)
        print(parsed_message)

    except ConnectionRefusedError:
        print('Ошибка подключения к серверу')


if __name__ == '__main__':
    main()
