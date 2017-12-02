import unittest
import os
from EmailParser import Email


class TestEmail(unittest.TestCase):
    def setUp(self):
        self.email = Email('', './parsed_email_test.txt')

    def test_open_email(self):
        """Test if opening a blank path will fail."""
        with self.assertRaises(Exception):
            self.email.open_email()

    def test_parse_email(self):
        """Test if the parsing matches our expected output."""
        self.email.path = './original_email.txt'
        self.email.open_email()
        self.email.parse_email()
        parsed = open('./parsed_email.txt', 'r')
        self.assertMultiLineEqual(parsed.read(), self.email.parsed_email)
        parsed.close()


if __name__ == '__main__':
    unittest.main()