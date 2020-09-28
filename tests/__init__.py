import unittest
from personal_data_anonymizer import PersonalDataAnonymizer


class TestPersonalDataAnonymizer(unittest.TestCase):
    def test_anonymize_social_security_number(self):
        text = 'Nimeni on Matti Seppälä ja henkilötunnukseni on 010101-123P.'
        app = PersonalDataAnonymizer()
        actual = app.anonymize_social_security_number(text)
        expected = ['Nimeni on Matti Seppälä ja henkilötunnukseni on [redacted].']
        self.assertEqual(actual, expected)

    def test_anonymize_social_security_number_new_format(self):
        text = 'Henkilötunnukseni on 311214A123P.'
        app = PersonalDataAnonymizer()
        actual = app.anonymize_social_security_number(text)
        expected = ['Henkilötunnukseni on [redacted].']
        self.assertEqual(actual, expected)

    def test_anonymize_first_name(self):
        text = ['Nimeni on Matti Seppälä ja henkilötunnukseni on 010101-123P.']
        app = PersonalDataAnonymizer()
        actual = app.anonymize_name(text, names='first_names_finland')
        expected = ['Nimeni on [redacted] Seppälä ja henkilötunnukseni on 010101-123P.']
        self.assertEqual(actual, expected)

    def test_anonymize_last_name(self):
        text = ['Nimeni on Matti Seppälä ja henkilötunnukseni on 010101-123P.']
        app = PersonalDataAnonymizer()
        actual = app.anonymize_name(text, names='last_names_finland')
        expected = ['Nimeni on Matti [redacted] ja henkilötunnukseni on 010101-123P.']
        self.assertEqual(actual, expected)

    def test_anonymize_phone_number(self):
        text = 'Puhelinnumeroni on 0401234567'
        app = PersonalDataAnonymizer()
        actual = app.anonymize_phone_number(text)
        expected = ['Puhelinnumeroni on [redacted]']
        self.assertEqual(actual, expected)

    def test_anonymize_everything(self):
        text = ['Nimeni on Matti Seppälä. Henkilötunnukseni on 010101-123P ja puhelinnumeroni on 0501234567.',
                'olen riikka toivola hetuni on 090909-0000 ja puhelinnumeroni 0441212312']
        app = PersonalDataAnonymizer()
        actual = app.anonymize_everything(text)
        expected = ['Nimeni on [redacted] [redacted]. Henkilötunnukseni on [redacted] ja puhelinnumeroni on [redacted].',
                    'olen [redacted] [redacted] hetuni on [redacted] ja puhelinnumeroni [redacted]']
        self.assertEqual(actual, expected)
