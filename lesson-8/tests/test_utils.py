import json
import unittest
import os
import sys

sys.path.append(os.path.join(os.getcwd(), '..'))
from common.utils import parse_message, prepare_dispatch


class TestUtils(unittest.TestCase):
    test_msg = {
        'action': 'presence',
        'time': 10,
        'user': {'account_name': 'C0deMaver1ck',
                 'status': 'Yep, I am here!'}
    }
    encoded_test_msg = json.dumps(test_msg).encode()

    def test_prepare_dispatch(self):
        self.assertEqual(self.encoded_test_msg,
                         prepare_dispatch(self.test_msg))

    def test_parse_message(self):
        self.assertEqual(self.test_msg, parse_message(self.encoded_test_msg))


if __name__ == '__main__':
    unittest.main()
