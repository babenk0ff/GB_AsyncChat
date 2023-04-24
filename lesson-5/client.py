import argparse
import logging
import socket
import time

from common.utils import parse_message, prepare_dispatch
from common.validators import ValidateAddress, ValidatePort
from log import client_log_config


client_logger = logging.getLogger('client')


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
        client_logger.info(
            f'Произведено подключение к серверу по адресу: {host}:{port}'
        )

        sock.send(prepare_dispatch(make_presence()))
        client_logger.info('Отправлено сообщение о присутствии')

        server_response = sock.recv(1024)
        client_logger.info('Получен ответ сервера')

        parsed_message = parse_message(server_response)
        client_logger.info(f'Ответ сервера распознан: {parsed_message}')

    except ConnectionRefusedError:
        client_logger.critical(
            f'Не удалось подключение к серверу по адресу: {host}:{port}'
        )


if __name__ == '__main__':
    main()
