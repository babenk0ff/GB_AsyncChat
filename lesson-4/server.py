import argparse
import socket

from common.utils import parse_message, prepare_dispatch
from common.validators import ValidateAddress, ValidatePort


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

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()

    while True:
        client, addr = server_socket.accept()

        client_msg = client.recv(1024)
        parsed_message = parse_message(client_msg)
        print(parsed_message)

        response = make_response(parsed_message)
        client.send(prepare_dispatch(response))

        client.close()


if __name__ == '__main__':
    main()
