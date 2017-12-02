""" Email Parsing

This Python 3 module contains functions for opening a text file and parsing an email.
It can also be run as a script on the command line.
"""
import re


class Email:
    fields = [{'key': 'To',
               'regex': r'(?:^To: )([\S\s]*?)\n[^\t]',
               'value': []},
              {'key': 'From',
               'regex': r'',
               'value': []},
              {'key': 'Date',
               'regex': r'',
               'value': []},
              {'key': 'Contents',
               'regex': r'',
               'value': []}]
    text = ''
    path = ''

    def __init__(self, path):
        self.path = path

    def open_email(self):
        """ Read text file and save as string.
        """
        with open(self.path, 'r') as email_file:
            self.text = email_file.read()

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
                line = '{0}: {1}\n\n'.format(field['key'], '\n'.join(field['value']))
                email_file.write(line)

    def clean_match(self, match):
        """ Remove tabs or any other extraneous formatting
        from the matches.
        """
        clean_match = match.replace('\t', '')
        return clean_match


if __name__ == "__main__":
    # email = Email(input(
    #     'Enter the filepath of the email (.txt) to parse: '))
    # email.save_email(input('Enter where you want to save the parsed email: '))
    email = Email(r'A:\original_msg.txt')
    email.open_email()
    email.parse_email()
    email.save_email(r'A:\parse_msg.txt')
