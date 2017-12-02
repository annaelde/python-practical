import os
import unittest

from EmailParser import Email


class TestEmail(unittest.TestCase):
    def setUp(self):
        self.email = Email()
        self.key = 'Subject'
        self.regex = r'(?:^Subject: )([\S\s]*?)\n[^\t]'

    def test_open_email(self):
        """Test if opening a blank path will fail."""
        with self.assertRaises(IOError):
            self.email.open_email()

    def test_parse_email(self):
        """Test if the parsing matches our expected output."""
        self.email.open_path = './original_email.txt'
        self.email.open_email()
        self.email.parse_email()
        sample_email = open('./parsed_email.txt', 'r')
        parsed_email = sample_email.read()
        sample_email.close()
        self.assertMultiLineEqual(parsed_email, self.email.parsed_email)

    def test_save_email(self):
        """Test if saving the parsed email to a file works."""
        with self.assertRaises(IOError):
            self.email.save_email('')

        self.email.save_email('./saved_email.txt')
        os.remove('./saved_email.txt')

    def test_mutate_field(self):
        """Test if adding/removing fields behaves as expected."""
        # Test adding a field
        with self.assertRaises(ValueError):
            self.email.add_field('', '')

        self.email.add_field(self.key, self.regex)

        found_key = False
        found_regex = r''
        for field in self.email.fields:
            if field['key'] == self.key:
                found_key = True
                found_regex = field['regex']

        self.assertTrue(found_key)
        self.assertEqual(found_regex, self.regex)

        # Test removing a field
        with self.assertRaises(LookupError):
            self.email.remove_field('')

        self.email.remove_field(self.key)

        found_key = False
        found_regex = r''
        for field in self.email.fields:
            if field['key'] == self.key:
                found_key = True
                found_regex = field['regex']

        self.assertFalse(found_key)
        self.assertNotEqual(found_regex, self.regex)


if __name__ == '__main__':
    unittest.main()
