import argparse
import re


class ValidateAddress(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        pattern = re.compile(r'^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$')
        if not re.fullmatch(pattern, values) and values != 'localhost':
            parser.error('Неверный формат IP-адреса')
        setattr(namespace, self.dest, values)


class ValidatePort(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if int(values) < 1024 or int(values) > 65535:
            parser.error('Номер порта должен быть в диапазоне от 1024 до 65535')
        setattr(namespace, self.dest, values)
