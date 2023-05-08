import unittest
import os
import sys

sys.path.append(os.path.join(os.getcwd(), '..'))
from server import make_response


class TestServer(unittest.TestCase):
    error_response = {
        'response': 400,
        'error': 'Bad request',
    }
    success_response = {
        'response': 200,
    }

    def test_make_response_correct(self):
        test_msg = {
            'action': 'presence',
            'time': 10,
            'user': {'account_name': 'C0deMaver1ck',
                     'status': 'Yep, I am here!'}
        }
        self.assertEqual(make_response(test_msg), self.success_response)

    def test_make_response_no_action(self):
        test_msg = {
            'time': 10,
            'user': {'account_name': 'C0deMaver1ck',
                     'status': 'Yep, I am here!'}
        }
        self.assertEqual(make_response(test_msg), self.error_response)

    def test_make_response_not_correct_action(self):
        test_msg = {
            'action': 'NOT_CORRECT',
            'time': 10,
            'user': {'account_name': 'C0deMaver1ck',
                     'status': 'Yep, I am here!'}
        }
        self.assertEqual(make_response(test_msg), self.error_response)


if __name__ == '__main__':
    unittest.main()
