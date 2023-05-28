import argparse
import dis
import logging
import socket
import sys
import time
from threading import Thread

from common.jim import JIM, InvalidJIM
from common.validators import ValidateAddress, ValidatePort
from exeptions import APIError
from log.log_decorator import log

logger = logging.getLogger('client')


class ClientVerifier(type):
    def __init__(cls, name, bases, attrs):
        forbidden_methods = ['accept', 'listen', 'socket']
        for attr_name, attr_value in attrs.items():
            if hasattr(attr_value, '__call__'):
                bytecode = dis.Bytecode(attr_value)
                for instr in bytecode:
                    if instr.opname == 'LOAD_GLOBAL':
                        if instr.argval in forbidden_methods:
                            raise TypeError(f'{attr_name} вызывает '
                                            f'недопустимый метод connect')
        super().__init__(name, bases, attrs)


class Receiver(Thread, metaclass=ClientVerifier):
    def __init__(self, client):
        super().__init__()
        self.client = client
        self.daemon = True

    def run(self) -> None:
        while True:
            try:
                resp = self.client.get_server_response()
                if resp.is_message:
                    self.client.print_message(resp)
            except InvalidJIM as e:
                logger.error(e)
            except APIError as e:
                logger.error(e)
            except (OSError, ConnectionError, ConnectionAbortedError,
                    ConnectionResetError):
                logger.critical(
                    f'Потеряно соединение с сервером '
                    f'{self.client.server_host}:{self.client.server_port}')
                break


class Sender(Thread, metaclass=ClientVerifier):
    def __init__(self, client):
        super().__init__()
        self.client = client
        self.daemon = True

    def run(self) -> None:
        while True:
            try:
                receiver = self.client.get_username(receiver=True)
                message = self.client.make_message(receiver=receiver)
                self.client.send_message(message)
            except (OSError, ConnectionError, ConnectionAbortedError,
                    ConnectionResetError):
                logger.critical(
                    f'Потеряно соединение с сервером '
                    f'{self.client.server_host}:{self.client.server_port}')
                break
            except KeyboardInterrupt:
                self.client.send_message(JIM.get_quit())
                raise


class Client(metaclass=ClientVerifier):
    def __init__(self, sock: socket):
        self.socket = sock
        self.username = None
        print(self.socket.getsockname())
        print(self.socket.gethostbyname())
        print(self.socket.gethostbyaddr())
        print(self.socket.getservbyname())

    @log
    def get_username(self, receiver=False):
        while True:
            user = 'пользователя' if not receiver else 'получателя'
            username = str(input(f'Введите имя {user}: '))
            if len(username) > 25:
                print(f'Имя {user} не должно превышать 25 символов')
                continue
            else:
                return username

    @log
    def connect(self):
        self.send_message(JIM.get_presence(self.username))
        self.get_server_response()

    @log
    def make_message(self, receiver):
        while True:
            message = str(input('Введите сообщение: '))
            if len(message) > 500:
                print(f'Сообщение не должно превышать 500 символов')
                continue
            else:
                return JIM.get_message(self.username, message, receiver)

    @log
    def get_server_response(self) -> JIM:
        raw_data = self.socket.recv(1024)
        if raw_data:
            json_string = raw_data.decode('utf-8')
            resp = JIM(json_string)
            if resp.is_response and resp.response >= 400:
                raise APIError(resp.response, resp.error)
            return resp
        else:
            raise ConnectionError

    @log
    def send_message(self, message):
        self.socket.send(message.encode('utf-8'))

    @staticmethod
    @log
    def print_message(jim_obj: JIM) -> None:
        print(f'Отправитель: {jim_obj.sender}\n'
              f'  Сообщение: {jim_obj.message}\n')

    @log
    def start(self):
        with self.socket:
            try:
                self.username = self.get_username()
                self.connect()
            except KeyboardInterrupt:
                logger.info('Клиент был закрыт')
                self.send_message(JIM.get_quit())
                sys.exit()
            except (ConnectionRefusedError, ConnectionError):
                logger.critical(f'Не удалось подключиться к серверу ')
                sys.exit(1)
            except APIError as e:
                logger.error(e)
                sys.exit(1)
            except InvalidJIM as e:
                logger.error(e)
                sys.exit(1)

            else:
                receiver = Receiver(client=self)
                receiver.start()

                sender = Sender(client=self)
                sender.start()
                logger.debug('Потоки запущены')

                while True:
                    try:
                        time.sleep(1)
                        if receiver.is_alive() and sender.is_alive():
                            continue
                        break
                    except KeyboardInterrupt:
                        print('\nКлиент был остановлен')
                        logger.info('Клиент был закрыт')
                        sys.exit()


@log
def get_args():
    parser = argparse.ArgumentParser(description='Запуск клиента')
    parser.add_argument('host', type=str, action=ValidateAddress,
                        help='IP-адрес сервера')
    parser.add_argument('port', nargs='?', type=int, default=7777,
                        action=ValidatePort, help='Номер порта сервера')
    args = parser.parse_args()
    return args.host, args.port


@log
def init_socket(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
    except (ConnectionRefusedError, ConnectionError):
        logger.critical(f'Не удалось подключиться к серверу {host}:{port}')
        sys.exit(1)
    else:
        print('Установлено подключение к серверу')
        logger.info(f'Установлено подключение к серверу {host}:{port}')
        return sock


if __name__ == '__main__':
    client_host, client_port = get_args()
    client_socket = init_socket(client_host, client_port)

    client = Client(client_socket)
    client.start()
