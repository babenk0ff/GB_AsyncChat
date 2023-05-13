import json
import time

from .exeptions import InvalidJIM

ACTIONS = (
    'authenticate',
    'presence',
    'msg',
    'quit',
    'join',
    'leave',
    'probe',
)


class JIM:
    is_presence = False
    is_response = False
    is_message = False
    is_quit = False

    def __init__(self, json_string):
        try:
            deserialized = json.loads(json_string)
            if self.is_schema_valid(deserialized):
                for attr, value in deserialized.items():
                    setattr(self, attr, value)

                if hasattr(self, 'action'):
                    if self.action == 'presence':
                        self.is_presence = True
                    elif self.action == 'msg':
                        self.is_message = True
                    elif self.action == 'quit':
                        self.is_quit = True
                if hasattr(self, 'response'):
                    self.is_response = True

            else:
                raise InvalidJIM
        except TypeError as e:
            print(e)

    @classmethod
    def is_schema_valid(cls, data):
        if not isinstance(data, dict):
            return False

        if 'response' in data:
            return True

        if not all(key in data for key in ('action', 'time')) or \
                data['action'] not in ACTIONS:
            return False

        if data['action'] == 'presence' and 'user' in data and \
                isinstance(data['user'], dict) and \
                len(data['user'].get('account_name', '')) <= 25:
            return True

        if data['action'] == 'msg' and all(
                key in data for key in ('sender', 'message')
        ) and isinstance(data['sender'], str) \
                and len(data['sender']) <= 25 \
                and isinstance(data['message'], str) \
                and len(data['message']) <= 500:
            return True

        return False

    def to_json(self):
        filtered_attrs = {
            key: value for key, value in vars(self).items()
            if not key.startswith('is_')
        }
        return json.dumps(filtered_attrs)

    @staticmethod
    def get_message(sender, message, receiver=''):
        schema = {
            'action': 'msg',
            'time': time.time(),
            'sender': sender,
            'receiver': receiver,
            'message': message,
        }
        return json.dumps(schema)

    @staticmethod
    def get_presence(username):
        schema = {
            'action': 'presence',
            'time': time.time(),
            'user': {'account_name': username},
        }
        return json.dumps(schema)

    @staticmethod
    def get_quit():
        response = {'action': 'quit',
                    'time': time.time()}
        return json.dumps(response)

    @staticmethod
    def get_400_bad_request():
        response = {'response': 400,
                    'error': 'Bad request'}
        return json.dumps(response)

    @staticmethod
    def get_200_ok():
        response = {'response': 200}
        return json.dumps(response)

    @staticmethod
    def get_409_conflict():
        response = {'response': 409,
                    'error': 'Уже имеется подключение с указанным именем'}
        return json.dumps(response)

    @staticmethod
    def get_404_not_found():
        response = {'response': 404,
                    'error': 'Пользователь отсутствует на сервере'}
        return json.dumps(response)
