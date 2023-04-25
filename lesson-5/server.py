import argparse
import json
import logging
import socket

from common.utils import parse_message, prepare_dispatch
from common.validators import ValidateAddress, ValidatePort
from log import server_log_config


server_logger = logging.getLogger('server')


def get_args():
    parser = argparse.ArgumentParser(description='Запуск сервера')
    parser.add_argument('-a', type=str, default='', dest='addr',
                        action=ValidateAddress,
                        help='IP-адрес, который будет прослушиваться')
    parser.add_argument('-p', type=int, default=7777, dest='host',
                        action=ValidatePort,
                        help='Номер порта, на котором запустится сервер')
    args = parser.parse_args()
    return args.addr, args.host


def make_response(parsed_msg: dict):
    if parsed_msg.get('action') == 'presence':
        return {'response': 200}
    return {
        'response': 400,
        'error': 'Bad request'
    }


def main():
    host, port = get_args()
    server_logger.info(f'Старт сервера на порту {port}')

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()

    while True:
        client, addr = server_socket.accept()
        server_logger.info(f'Подключен клиент с адреса f{addr}')

        try:
            client_msg = client.recv(1024)
            server_logger.info('Получено сообщение от клиента')

            parsed_message = parse_message(client_msg)
            server_logger.info(f'Распознано сообщение клиента: {parsed_message}')

            response = make_response(parsed_message)
            server_logger.info(f'Сформирован ответ клиенту: {response}')

            client.send(prepare_dispatch(response))
            server_logger.info('Ответ клиенту отправлен')

            client.close()
            server_logger.info('Соединение с клиентом закрыто')

        except json.JSONDecodeError as e:
            server_logger.error(f'Не удалось декодировать JSON')
            client.close()
            server_logger.info('Соединение с клиентом закрыто')


if __name__ == '__main__':
    main()
