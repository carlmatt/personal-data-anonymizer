import csv
import re
from typing import Callable, Union

from personal_data_anonymizer.utils.finnish import cases as cases_finnish
from personal_data_anonymizer.utils.finnish import conjugate as conjugation_finnish


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

    @staticmethod
    def conjugate_names(names: list, conjugation_func: Callable[[str, str], str], cases: dict) -> list:
        """ Tool for conjugating names into different cases

        :param names: Names to conjugate
        :param conjugation_func: Conjugation function to use
        :param cases: Cases to use in conjugation
        :return: Conjugated names
        """
        names = set(names)
        names_conjugated = set()
        for name in names:
            names_conjugated.update({conjugation_func(name, case[0]) for case in cases})

        names.update(names_conjugated)
        return list(names)

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
            names = self.conjugate_names(names, conjugation_finnish, cases_finnish)
        elif names == 'last_names_finland':
            names = self.last_names_finland
            names = self.conjugate_names(names, conjugation_finnish, cases_finnish)
        elif not isinstance(names, (list, str)):
            raise TypeError("'names' must be either a string or a list of strings")

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

    def anonmyize_email_address(self, text_corpus: Union[list, str], anonymized_text: str = '[redacted]') -> list:
        """ Anonymize email address

        :param text_corpus: Text to be anonymized
        :param anonymized_text: Text to replace the anonymized part with, defaults to '[redacted]'
        :return: Anonymized text
        """
        text_corpus = self.check_text_corpus(text_corpus)
        pattern = '[^@]+@[^@]+\.[^@]+'

        return [''.join([anonymized_text if re.match(pattern, word) else word for word in re.split(r'(\s)', text)])
                for text in text_corpus]

    def anonymize_everything(self, text_corpus: Union[list, str], case_sensitive: bool = False) -> list:
        """ Anonymize everything using the default values

        :param text_corpus: Text to be anonymized
        :param case_sensitive: Determines whether the anonymization is case sensitive, defaults to False
        :return: Anonymized text
        """
        text = self.check_text_corpus(text_corpus)
        text = self.anonymize_social_security_number(text)
        text = self.anonymize_name(text, names='first_names_finland', case_sensitive=case_sensitive)
        text = self.anonymize_name(text, names='last_names_finland', case_sensitive=case_sensitive)
        text = self.anonymize_phone_number(text)
        text = self.anonmyize_email_address(text)
        return text
