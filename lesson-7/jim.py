import json
import time


class InvalidJIM(Exception):
    pass


class JIM:
    ACTIONS = (
        'authenticate',
        'presence',
        'msg',
        'quit',
        'join',
        'leave',
        'probe',
    )
    is_presence = False
    is_response = False
    is_message = False

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
                data['action'] not in cls.ACTIONS:
            return False

        if data['action'] == 'presence' and 'user' in data and \
                isinstance(data['user'], dict) and \
                len(data['user'].get('account_name', '')) <= 25:
            return True

        if data['action'] == 'msg' and all(
                key in data for key in ('sender', 'message')) and \
                isinstance(data['sender'], str) and len(data['sender']) <= 25 \
                and isinstance(data['message'], str) \
                and len(data['message']) <= 500:
            return True

        return False

    def to_json(self):
        filtered_attrs = {
            key: value for key, value in vars(self).items()
            if not key.startswith('_')
        }
        return json.dumps(filtered_attrs)

    @classmethod
    def as_message(cls, username, message):
        schema = {
            'action': 'msg',
            'time': time.time(),
            'sender': username,
            'message': message,
        }
        return json.dumps(schema)

    @classmethod
    def as_presence(cls, username):
        schema = {
            'action': 'presence',
            'time': time.time(),
            'user': {'account_name': username},
        }
        return json.dumps(schema)

    @staticmethod
    def get_bad_request():
        response = {'response': 400,
                    'error': 'Bad request'}
        return json.dumps(response)

    @staticmethod
    def get_ok():
        response = {'response': 200}
        return json.dumps(response)
