""" Email Parsing

This Python 3 module contains class Email, which can read and parse an email,
and store the parsed fields.
"""
import os
import re
import sys


class Email:
    fields = [{'key': 'To',
               'regex': r'(?:^To: )([\S\s]*?)\n[^\t]',
               'value': []},
              {'key': 'From',
               'regex': r'(?:^From: )([\S\s]*?)\n[^\t]',
               'value': []},
              {'key': 'Date',
               'regex': r'(?:^Date: )([\S\s]*?)\n[^\t]',
               'value': []},
              {'key': 'Contents',
               'regex': r'(?:^Content-Transfer-Encoding: quoted-printable\n)([\S\s]*?)\n(?:^------=_Part_[0-9\_\.]*?--$|--[0-9a-fA-F]*?--$|^------=_Part_[0-9\_\.]*?$)',
               'value': []}]
    """List of email fields, each containing the following:
    Key: What the field will be labeled as in the formatted output.
    Regex: Used to find the field in the raw email input.
    Value: Result of the regex, stored as a list of matches.
    """
    raw_email = ''
    """Raw email input from an opened file."""
    parsed_email = ''
    """Parsed email output."""
    open_path = ''
    """Path that open_email() will use."""
    save_path = ''
    """Path that save_email() will use."""

    def __init__(self, open_path: str = '', save_path: str = ''):
        """ Open path and save path are both optional, can be assigned later.
        """
        self.open_path = open_path
        if save_path:
            self.save_path = save_path
        else:
            self.save_path = os.path.join(
                os.path.dirname(open_path), 'parsed_email.txt')

    def add_field(self, key: str, regex: str):
        """Add email field to be parsed."""
        if not key or not regex:
            raise ValueError('Field\'s key and regex cannot be empty.')
        self.fields.append({'key': key, 'regex': regex, 'value': []})

    def remove_field(self, key: str):
        """Remove email field from fields to be parsed."""
        field = self.get_field(key)
        self.fields.remove(field)

    def get_field(self, key: str):
        for field in self.fields:
            if field['key'] == key:
                return field
        raise LookupError('Field was not found.')

    def open_email(self):
        """Read text file and save as string."""
        with open(self.open_path, 'r') as email_file:
            self.raw_email = email_file.read()

    def parse_email(self):
        """Parse email fields using assigned regular expressions."""
        # Reset parsed email attribute
        self.parsed_email = ''
        # Iterate through fields and use regex to parse
        for field in self.fields:
            # Reset values
            if field['value'] != []:
                field['value'] = []
            # Parse email using field's assigned regular expression
            matches = re.findall(field['regex'], self.raw_email, re.MULTILINE)
            for match in matches:
                match = self.clean_match(match)
                field['value'].append(match)
            # Add values to parsed email attribute
            self.parsed_email += '{0}: {1}\n\n'.format(
                field['key'], '\n'.join(field['value']))

    def save_email(self, path: str = None):
        """Save parsed and formatted email to file path."""
        # Use save_path attribute if a path isn't passed
        if path is None:
            path = self.save_path
        with open(path, 'w') as email_file:
            email_file.write(self.parsed_email)

    def clean_match(self, match: str):
        """Remove tabs or any other extraneous formatting from the matches.
        Returns cleaned match.
        """
        clean_match = match.replace('\t', '')
        return clean_match


if __name__ == "__main__":
    INPUT_MESSAGE = 'Enter the filepath of the email (.txt) to parse: '
    SAVE_MESSAGE = 'Enter where you want to save the parsed email: '

    def open_email(email: str):
        try:
            email.open_email()
        except:
            choice = file_failure_prompt()
            if choice == '1':
                email.path = input(INPUT_MESSAGE)
                email.open_email()
            else:
                sys.exit()
        email.parse_email()

    def save_email(email: str, location: str):
        try:
            email.save_email(location)
        except:
            choice = file_failure_prompt()
            if choice == '1':
                email.path = input(SAVE_MESSAGE)
                email.open_email()
            else:
                sys.exit()

    def file_failure_prompt():
        print('Error opening that file path.')
        return input('Try a new filepath (1) or exit (2): ')

    parse_my_emails = True
    while parse_my_emails:
        email = Email(input(INPUT_MESSAGE))
        open_email(email)
        save_email(email, input(SAVE_MESSAGE))
        answer = input('Parse another email? (Y / N): ')
        if answer.lower() != 'y':
            parse_my_emails = False
