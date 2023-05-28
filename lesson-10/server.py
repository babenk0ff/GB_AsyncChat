import argparse
import dis
import logging
import sys
from collections import deque
from select import select
from socket import socket, AF_INET, SOCK_STREAM, SO_REUSEADDR, SOL_SOCKET
from typing import Deque, Dict, Tuple

from common.jim import JIM, InvalidJIM
from common.validators import ValidateAddress, ValidatePort
from log.log_decorator import log

logger = logging.getLogger('server')


class ServerVerifier(type):
    def __init__(cls, name, bases, attrs):
        for attr_name, attr_value in attrs.items():
            if hasattr(attr_value, '__call__'):
                bytecode = dis.Bytecode(attr_value)
                for instr in bytecode:
                    if instr.opname == 'CALL_FUNCTION':
                        arg = instr.argval
                        if isinstance(arg, tuple) and 'connect' in arg:
                            raise TypeError(f'{attr_name} вызывает '
                                            f'недопустимый метод connect')
                if hasattr(attr_value, 'type') \
                        and attr_value.type != SOCK_STREAM:
                    print(attr_name)
                    raise TypeError(f'Неподдерживаемый тип сокета')
        super().__init__(name, bases, attrs)


class Port:
    def __init__(self, port=7777):
        self.default_port = port

    def __set_name__(self, owner, name):
        self.name = '_' + name

    def __get__(self, instance, owner):
        return getattr(instance, self.name, self.default_port)

    def __set__(self, instance, value):
        if not isinstance(value, int) or value < 0:
            logger.critical('Порт должен быть целым положительным числом')
            sys.exit(1)
        setattr(instance, self.name, value)


class Server(metaclass=ServerVerifier):
    port = Port()

    def __init__(self, host: str, port: int):
        self.host: str = host
        self.port: int = port
        self.socket: socket = self.set_socket(self.host, self.port)
        self.inputs: Dict[socket: Tuple[str, str]] = {
            self.socket: (self.host, self.port)}
        self.outputs: Dict[socket: Tuple[str, str]] = {}
        self.messages: Deque[JIM] = deque()
        self.registered_users: Dict[str: socket] = {}

    @staticmethod
    @log
    def set_socket(host: str, port: int) -> socket:
        server_socket = socket(AF_INET, SOCK_STREAM)
        server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        server_socket.bind((host, port))
        return server_socket

    @staticmethod
    @log
    def send_message(sock: socket, message: str) -> None:
        try:
            sock.send(message.encode('utf-8'))
        except ConnectionError:
            raise

    @log
    def handle_mailing_list(self, to_write):
        for message in list(self.messages):
            receiver = message.receiver
            if receiver == '':
                for sock in to_write:
                    self.send_message(sock, message.to_json())
            elif receiver in self.registered_users.keys() \
                    and self.registered_users[receiver] in to_write \
                    and message.sender != receiver:
                sock = self.registered_users[receiver]
                self.send_message(sock, message.to_json())

            self.messages.pop()

    @log
    def handle_incoming_connect(self, client_sock: socket):
        try:
            raw_data = client_sock.recv(1024)
            if raw_data:
                logger.info('Получены данные от клиента')
                json_string = raw_data.decode('utf-8')

                jim_obj = JIM(json_string)

                if jim_obj.is_presence:
                    username = jim_obj.user['account_name']
                    if username in self.registered_users.keys():
                        self.send_message(client_sock, JIM.get_409_conflict())
                        self.kick_client(client_sock)
                    else:
                        self.registered_users[username] = client_sock
                        self.send_message(client_sock, JIM.get_200_ok())
                elif jim_obj.is_message:
                    if jim_obj.receiver in self.registered_users \
                            or jim_obj.receiver == '':
                        self.messages.append(jim_obj)
                    else:
                        self.send_message(client_sock, JIM.get_404_not_found())
                elif jim_obj.is_quit:
                    self.kick_client(client_sock)
                else:
                    self.send_message(client_sock, JIM.get_400_bad_request())

            else:
                raise ConnectionError

        except (ConnectionResetError, ConnectionError):
            logger.error(
                f'Клиент {self.inputs[client_sock]} отключился')
            self.kick_client(client_sock)

        except InvalidJIM:
            logger.error(f'Получен неверный формат JIM-объекта')
            self.send_message(client_sock, JIM.get_400_bad_request())

    @log
    def kick_client(self, client_sock: socket) -> None:
        del self.inputs[client_sock]
        if client_sock in self.outputs:
            del self.outputs[client_sock]
        for username, sock in list(self.registered_users.items()):
            if client_sock == sock:
                del self.registered_users[username]
        client_sock.close()

    @log
    def start(self) -> None:
        listening_addr = 'все' if not self.host else self.host
        print(f'Сервер запущен. Прослушиваемый адрес: {listening_addr}, '
              f'порт: {self.port} ')
        logger.info(f'Старт сервера ({self.port}, {listening_addr})')

        with self.socket:
            self.socket.listen(5)
            while True:
                try:
                    to_read, to_write, _ = select(
                        self.inputs, self.outputs, [], 1.0)

                    for sock in to_read:
                        if sock == self.socket:
                            client_sock, client_addr = self.socket.accept()
                            self.inputs[client_sock] = client_addr
                            self.outputs[client_sock] = client_addr
                            logger.info(f'Подключен клиент {client_addr}')
                        else:
                            self.handle_incoming_connect(sock)

                    if self.messages and to_write:
                        self.handle_mailing_list(to_write)
                except KeyboardInterrupt:
                    print('Сервер остановлен')
                    logger.info('Сервер остановлен')
                    sys.exit()


@log
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


if __name__ == '__main__':
    server_addr, server_port = get_args()

    server = Server(server_addr, server_port)
    server.start()
