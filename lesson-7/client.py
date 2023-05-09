import argparse
import logging
import socket
import sys

from common.validators import ValidateAddress, ValidatePort
from jim import JIM, InvalidJIM
from log import client_log_config
from log.log_decorator import log

client_logger = logging.getLogger('client')


class Client:
    def __init__(self, host, port, mode):
        self.server_host = host
        self.server_port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mode = mode
        self.username = None

    @log
    def connect(self):
        self.socket.connect((self.server_host, self.server_port))
        self.send_message(JIM.as_presence(self.username))

    @log
    def make_message(self):
        user_input = str(input('Введите сообщение: '))
        return JIM.as_message(self.username, user_input)

    @log
    def handle_incoming_msg(self):
        try:
            raw_data = self.socket.recv(1024)
            json_string = raw_data.decode('utf-8')
            jim_obj = JIM(json_string)
            if jim_obj.is_message:
                self.printer(jim_obj)
        except InvalidJIM:
            client_logger.error('Получен неверный формат JIM-объекта')

    @log
    def send_message(self, message):
        self.socket.send(message.encode('utf-8'))

    @staticmethod
    @log
    def printer(jim_obj):
        print(f'Отправитель: {jim_obj.sender}\n'
              f'  Сообщение: {jim_obj.message}\n')

    @log
    def start(self):
        with self.socket:
            try:
                self.username = str(input('Введите имя пользователя: '))
                self.connect()
                client_logger.info(
                    f'Успешное подключение к серверу '
                    f'по адресу {self.server_host}:{self.server_port}. '
                    f'Режим работы: {self.mode}')

                while True:
                    if self.mode == 'send':
                        try:
                            self.send_message(self.make_message())
                        except (ConnectionResetError,
                                ConnectionError,
                                ConnectionAbortedError):
                            client_logger.error(f'Связь с сервером потеряна')
                            sys.exit(1)

                    if self.mode == 'listen':
                        try:
                            self.handle_incoming_msg()
                        except (ConnectionResetError,
                                ConnectionError,
                                ConnectionAbortedError):
                            client_logger.error(f'Связь с сервером потеряна')
                            sys.exit(1)
            except ConnectionRefusedError:
                client_logger.critical(
                    f'Не удалось подключение к серверу '
                    f'по адресу: {self.server_host}:{self.server_port}')
                sys.exit(1)


@log
def get_args():
    parser = argparse.ArgumentParser(description='Запуск клиента')
    parser.add_argument('host', type=str, action=ValidateAddress,
                        help='IP-адрес сервера')
    parser.add_argument('port', nargs='?', type=int, default=7777,
                        action=ValidatePort, help='Номер порта сервера')
    parser.add_argument('mode', type=str, choices=('listen', 'send'),
                        help='Режим работы клиента')
    args = parser.parse_args()
    return args.host, args.port, args.mode


if __name__ == '__main__':
    client_host, client_port, client_mode = get_args()

    client = Client(client_host, client_port, client_mode)
    client.start()
