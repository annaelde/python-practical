# Email Parser Coding Practical
I've implemented an Email class, which contains methods for: 

- reading an email from a file
- parsing the file's contents into a list of fields using regular expressions
- adding and removing fields (useful when instantiating the class elsewhere)
- saving the parsed email to a file
- cleaning the email fields

Most of these methods have some sort of basic validation.

There's logic inside the EmailParser module for running it as a script from the command line. I also included a unit test and some sample documents that work with the test.

## Commands
### Running the Script

`python EmailParser.py`

### Running the Test

`python -m unittest`

## Next Steps
There are *a lot* more content types that I would need to add to my regular expressions for the content field to cover everything I found while researching different types of emails.

Expanding the `clean_match()` method would definitely be next--I noticed some odd characters occurring in the email text file I downloaded (e.g., '=C2=A0') that have something to do with UTF-8 characters not rendered properly in MIME-encoded text.

I would also have to figure out how to handle HTML in emails. You can't parse HTML with regex, so I don't think extracting the inner HTML would work with my current parsing method.

I would also look into optimizing the way the fields are stored, because I'm not sure if nesting dictionaries in a list is the most efficient for lookups.

## Conclusion
Thanks for taking the time to review my work. I would appreciate any constructive criticism you have about my code 😊