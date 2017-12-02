""" Email Parsing

This Python 3 module contains functions for opening a text file and parsing an email.
It can also be run as a script on the command line.
"""
import re
import sys
import os


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
               'regex': r'(?:^Content-Transfer-Encoding: quoted-printable\n)([\S\s]*?)\n(?:^------=_Part_[0-9\_\.]*?--$|--[0-9a-fA-F]*?--$)',
               'value': []}]
    text = ''
    path = ''

    def __init__(self, path):
        self.path = path

    def open_email(self):
        """ Read text file and save as string.
        """
        try:
            with open(self.path, 'r') as email_file:
                self.text = email_file.read()
        except:
            raise Exception

    def parse_email(self):
        """ Parse email fields using assigned
        regular expressions.
        """
        for field in self.fields:
            matches = re.findall(field['regex'], self.text, re.MULTILINE)
            for match in matches:
                match = self.clean_match(match)
                field['value'].append(match)
                break

    def save_email(self, path):
        """ Save parsed and formatted email to
        file path.
        """
        with open(path, 'w') as email_file:
            for field in self.fields:
                line = '{0}: {1}\n\n'.format(
                    field['key'], '\n'.join(field['value']))
                email_file.write(line)

    def clean_match(self, match):
        """ Remove tabs or any other extraneous formatting
        from the matches.
        """
        clean_match = match.replace('\t', '')
        return clean_match


if __name__ == "__main__":
    def open_email(email):
        try:
            email.open_email()
        except:
            print('Could not open the specified file.')
            choice = input('Try a new file (1) or exit (2): ')
            if choice == '1':
                email.path = input(
                    'Enter the filepath of the email (.txt) to parse: ')
                email.open_email()
            else:
                sys.exit()

        email.parse_email()

    def save_email(email, location):
        try:
            email.save_email(location)
        except:
            print('Could not save email to that location.')
            choice = input('Try a new filepath (1) or exit (2): ')
            if choice == '1':
                email.path = input(
                    'Enter where you want to save the parsed email: ')
                email.open_email()
            else:
                sys.exit()

    # email = Email(input(
    #     'Enter the filepath of the email (.txt) to parse: '))
    # email.save_email(input('Enter where you want to save the parsed email: '))

    parse_my_emails = True
    while parse_my_emails:
        email = Email(r'A:')
        open_email(email)
        save_email(email, r'A:\parse_msg.txt')
        answer = input('Parse another email? (Y / N): ')
        if answer.lower() != 'y':
            parse_my_emails = False
