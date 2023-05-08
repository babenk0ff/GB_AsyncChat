import argparse
import json
import logging
import socket
from select import select
from collections import deque

from common.validators import ValidateAddress, ValidatePort
from log import server_log_config
from log.log_decorator import log
from jim import JIM, InvalidJIM
from typing import Deque, List

server_logger = logging.getLogger('server')


class Server:
    def __init__(self, host: str, port: int):
        self.host: str = host
        self.port: int = port
        self.socket: socket = self.set_socket(self.host, self.port)
        self.inputs: List[socket] = [self.socket]
        self.outputs: List = []
        self.messages: Deque[JIM] = deque()

    @staticmethod
    @log
    def set_socket(host, port):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, port))
        return server_socket

    @staticmethod
    @log
    def send_message(sock, message):
        try:
            sock.send(message.encode('utf-8'))
        except ConnectionError:
            server_logger.error(f'Клиент {sock.getpeername()} отключился '
                                f'в процессе отправки ему сообщения')

    @log
    def handle_incoming_connect(self, client_sock):
        try:
            raw_data = client_sock.recv(1024)
            if not raw_data:
                server_logger.info(
                    f'Клиент {client_sock.getpeername()} отключился')
                self.inputs.remove(client_sock)
                if client_sock in self.outputs:
                    self.outputs.remove(client_sock)
                return
            server_logger.info('Получены данные от клиента')
            json_string = raw_data.decode('utf-8')

            jim_obj = JIM(json_string)
            if jim_obj.is_message:
                self.messages.append(jim_obj)
            elif jim_obj.is_presence:
                self.send_message(client_sock, JIM.get_ok())

        except (ConnectionError, ConnectionResetError, OSError):
            server_logger.error(
                f'Клиент {client_sock.getpeername()} внезапно отключился ')
            self.inputs.remove(client_sock)
        except InvalidJIM:
            server_logger.error(f'Получен неверный формат JIM-объекта')
            self.send_message(client_sock, JIM.get_bad_request())

    @log
    def start(self):
        print(f'Старт сервера на порту {self.port}')
        server_logger.info(f'Старт сервера на порту {self.port}')
        self.socket.listen(5)
        while True:
            to_read, to_write, _ = select(self.inputs, self.outputs, [])
            for sock in to_read:
                if sock == self.socket:
                    client_socket, client_address = self.socket.accept()
                    self.inputs.append(client_socket)
                    self.outputs.append(client_socket)
                    server_logger.info(f'Подключен клиент с адреса: '
                                       f'{client_address}')
                else:
                    self.handle_incoming_connect(sock)

            if self.messages and to_write:
                message = self.messages.popleft().to_json()
                for sock in to_write:
                    self.send_message(sock, message)


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
