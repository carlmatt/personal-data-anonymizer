import csv
import re
from typing import Union


class PersonalDataAnonymizer:
    """ Tool for anonymizing personal data in text
    """

    def __init__(self):
        with open('personal_data_anonymizer/source_data/first_names_finland.csv') as file:
            reader = csv.reader(file)
            self.first_names_finland = [row[0] for row in reader]

        with open('personal_data_anonymizer/source_data/last_names_finland.csv') as file:
            reader = csv.reader(file)
            self.last_names_finland = [row[0] for row in reader]

    @staticmethod
    def check_text_corpus(text_corpus: Union[list, str]):
        """ Tool for verifying the 'text_corpus' input

        :param text_corpus: Variable to be checked
        :returns: text_corpus variable
        """
        if isinstance(text_corpus, str):
            return [text_corpus]
        elif isinstance(text_corpus, list):
            return text_corpus
        raise TypeError("'text_corpus' must be either a string or a list of strings")

    def anonymize_social_security_number(self, text_corpus: Union[list, str],
                                         pattern: re.Pattern = re.compile(r'\d{6}(-| |a|A|\+)\d{3}[a-zA-Z0-9]'),
                                         anonymized_text: str = '[redacted]') -> list:
        """ Anonymize social security number

        :param text_corpus: Text to be anonymized
        :param pattern: Social security pattern, defaults to Finnish social security pattern
        :param anonymized_text: Text to replace the anonymized part with, defaults to '[redacted]'
        :return: Anonymized text
        """
        text_corpus = self.check_text_corpus(text_corpus)
        return [re.sub(pattern, anonymized_text, text_corpus[i]) for i in range(len(text_corpus))]

    def anonymize_name(self, text_corpus: Union[list, str], names: Union[list, str], case_sensitive: bool = False,
                       anonymized_text: str = '[redacted]'):
        """ Anonymize name

        :param text_corpus: Text to be anonymized
        :param names: Names to anonymize. Can be either 'first_names_finland', 'last_names_finland' or a custom list
        :param case_sensitive: Determines whether the anonymization is case sensitive, defaults to False
        :param anonymized_text: Text to replace the anonymized part with, defaults to '[redacted]'
        :return: Anonymized text
        """
        text_corpus = self.check_text_corpus(text_corpus)

        if names == 'first_names_finland':
            names = self.first_names_finland
        elif names == 'last_names_finland':
            names = self.last_names_finland
        elif isinstance(names, list):
            pass
        elif not isinstance(names, (list, str)):
            raise TypeError("'names' must be either a string or a list of strings")
        else:
            raise ValueError("'names' must be either 'first_names_finland', 'last_names_finland' or a custom list")

        if not case_sensitive:
            names = {name.lower() for name in names}
            # The anonymization is run twice (first with '\s'), beacuse '\W' doesn't catch hyphenated names
            text_corpus = [''.join([anonymized_text if word.lower() in names else word for word in re.split(r'(\s)', text)])
                           for text in text_corpus]
            return [''.join([anonymized_text if word.lower() in names else word for word in re.split(r'(\W)', text)])
                    for text in text_corpus]

        names = set(names)  # Convert names list to a set for faster lookup
        text_corpus = [''.join([anonymized_text if word in names else word for word in re.split(r'(\s)', text)])
                       for text in text_corpus]
        return [''.join([anonymized_text if word in names else word for word in re.split(r'(\W)', text)])
                for text in text_corpus]

    def anonymize_phone_number(self, text_corpus: Union[list, str], pattern: re.Pattern = re.compile('(^0[0-9])|(^358)'),
                               anonymized_text: str = '[redacted]') -> list:
        """ Anonymize phone number

        :param text_corpus: Text to be anonymized
        :param pattern: Phone number pattern, defaults to zero followed by any number, or word starting with 358
        :param anonymized_text: Text to replace the anonymized part with, defaults to '[redacted]'
        :return: Anonymized text
        """
        text_corpus = self.check_text_corpus(text_corpus)

        return [''.join([anonymized_text if re.match(pattern, word) else word for word in re.split(r'(\W)', text)])
                for text in text_corpus]

    def anonymize_everything(self, text_corpus: Union[list, str]) -> list:
        """ Anonymize everything using the default values

        :param text_corpus: Text to be anonymized
        :return: Anonymized text
        """
        text = self.check_text_corpus(text_corpus)
        text = self.anonymize_social_security_number(text)
        text = self.anonymize_name(text, names='first_names_finland')
        text = self.anonymize_name(text, names='last_names_finland')
        text = self.anonymize_phone_number(text)
        return text
