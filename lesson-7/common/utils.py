import json
import os
import sys

sys.path.append(os.path.join(os.getcwd(), '..'))
from log.log_decorator import log


@log
def parse_message(message):
    decoded_message = message.decode()
    deserialized_message = json.loads(decoded_message)
    return deserialized_message


@log
def prepare_dispatch(msg):
    json_string = json.dumps(msg)
    return json_string.encode()
