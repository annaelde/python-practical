""" Email Parsing

This Python 3 module contains class Email, which can read and parse an email,
and store the parsed fields.
"""
import re
import sys
import os


class Email:
    fields = [{'key': 'To',
               'regex': [r'(?:^To: )([\S\s]*?)\n[^\t]'],
               'value': []},
              {'key': 'From',
               'regex': [r'(?:^From: )([\S\s]*?)\n[^\t]'],
               'value': []},
              {'key': 'Date',
               'regex': [r'(?:^Date: )([\S\s]*?)\n[^\t]'],
               'value': []},
              {'key': 'Contents',
               'regex': [r'(?:^Content-Transfer-Encoding: quoted-printable\n)([\S\s]*?)\n(?:^------=_Part_[0-9\_\.]*?--$|--[0-9a-fA-F]*?--$)'],
               'value': []}]
    text = ''
    path = ''

    def __init__(self, path: str):
        self.path = path

    def add_field(self, key: str, regex: list):
        """Add email field to be parsed."""
        fields.append({'key': key, 'regex': regex, 'value': []})

    def remove_field(self, key: str):
        """Remove email field from fields to be parsed."""
        for index, field in self.fields:
            if field['key'] == key:
                self.fields.remove(index)

    def open_email(self):
        """Read text file and save as string."""
        try:
            with open(self.path, 'r') as email_file:
                self.text = email_file.read()
        except:
            raise Exception

    def parse_email(self):
        """Parse email fields using assigned regular expressions."""
        for field in self.fields:
            for regex in field['regex']:
                matches = re.findall(regex, self.text, re.MULTILINE)
                for match in matches:
                    match = self.clean_match(match)
                    field['value'].append(match)

    def save_email(self, path):
        """Save parsed and formatted email to file path."""
        with open(path, 'w') as email_file:
            for field in self.fields:
                line = '{0}: {1}\n\n'.format(
                    field['key'], '\n'.join(field['value']))
                email_file.write(line)

    def clean_match(self, match):
        """Remove tabs or any other extraneous formatting from the matches. 
        Returns cleaned match.
        """
        clean_match = match.replace('\t', '')
        return clean_match


if __name__ == "__main__":
    INPUT_MESSAGE = 'Enter the filepath of the email (.txt) to parse: '
    SAVE_MESSAGE = 'Enter where you want to save the parsed email: '

    def open_email(email):
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

    def save_email(email, location):
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
        answer=input('Parse another email? (Y / N): ')
        if answer.lower() != 'y':
            parse_my_emails=False
