import unittest
import os
import sys

sys.path.append(os.path.join(os.getcwd(), '..'))
from client import make_presence


class TestClient(unittest.TestCase):

    def test_make_presence_correct(self):
        presence = make_presence()
        presence['time'] = 10
        test_msg = {
            'action': 'presence',
            'time': 10,
            'user': {'account_name': 'C0deMaver1ck',
                     'status': 'Yep, I am here!'}
        }
        self.assertEqual(test_msg, presence)


if __name__ == '__main__':
    unittest.main()
