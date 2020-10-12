import unittest
from personal_data_anonymizer import PersonalDataAnonymizer


class TestPersonalDataAnonymizer(unittest.TestCase):
    def test_anonymize_social_security_number(self):
        text = 'Nimeni on Matti Seppälä ja henkilötunnukseni on 010101-123P.'
        app = PersonalDataAnonymizer()
        actual = app.anonymize_social_security_number(text)
        expected = ['Nimeni on Matti Seppälä ja henkilötunnukseni on [redacted].']
        self.assertEqual(actual, expected)

    def test_anonymize_social_security_number_21st_century(self):
        text = 'Henkilötunnukseni on 311214A123P.'
        app = PersonalDataAnonymizer()
        actual = app.anonymize_social_security_number(text)
        expected = ['Henkilötunnukseni on [redacted].']
        self.assertEqual(actual, expected)

    def test_anonymize_social_security_number_19th_century(self):
        text = 'Henkilötunnukseni on 311299+0010.'
        app = PersonalDataAnonymizer()
        actual = app.anonymize_social_security_number(text)
        expected = ['Henkilötunnukseni on [redacted].']
        self.assertEqual(actual, expected)

    def test_anonymize_first_name(self):
        text = ['Nimeni on matti seppälä, ja henkilötunnukseni on "010101-123P".']
        app = PersonalDataAnonymizer()
        actual = app.anonymize_name(text, names='first_names_finland')
        expected = ['Nimeni on [redacted] seppälä, ja henkilötunnukseni on "010101-123P".']
        self.assertEqual(actual, expected)

    def test_anonymize_first_name_conjugated(self):
        text = ['Matilla on koira. Sarilla on kissa.']
        app = PersonalDataAnonymizer()
        actual = app.anonymize_name(text, names='first_names_finland')
        expected = ['[redacted] on koira. [redacted] on kissa.']
        self.assertEqual(actual, expected)

    def test_anonymize_last_name(self):
        text = ['Nimeni on matti seppälä, ja henkilötunnukseni on 010101-123P.']
        app = PersonalDataAnonymizer()
        actual = app.anonymize_name(text, names='last_names_finland')
        expected = ['Nimeni on matti [redacted], ja henkilötunnukseni on 010101-123P.']
        self.assertEqual(actual, expected)

    def test_anonymize_last_name_conjugated(self):
        text = ['Menemme Virtaselle. Tulemme Perältä.']
        app = PersonalDataAnonymizer()
        actual = app.anonymize_name(text, names='last_names_finland')
        expected = ['Menemme [redacted]. Tulemme [redacted].']
        self.assertEqual(actual, expected)

    def test_anonymize_first_name_case_sensitive(self):
        text = ['Nimeni on Pekka Haapa-aho ja henkilötunnukseni on 010101-123P.']
        app = PersonalDataAnonymizer()
        actual = app.anonymize_name(text, names='first_names_finland', case_sensitive=True)
        expected = ['Nimeni on [redacted] Haapa-aho ja henkilötunnukseni on 010101-123P.']
        self.assertEqual(actual, expected)

    def test_anonymize_last_name_case_sensitive(self):
        text = ['Nimeni on Pekka Haapa-aho ja henkilötunnukseni on 010101-123P.']
        app = PersonalDataAnonymizer()
        actual = app.anonymize_name(text, names='last_names_finland', case_sensitive=True)
        expected = ['Nimeni on Pekka [redacted] ja henkilötunnukseni on 010101-123P.']
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
                    '[redacted] [redacted] [redacted] hetuni on [redacted] ja puhelinnumeroni [redacted]']
        self.assertEqual(actual, expected)

    def test_anonymize_everything_case_sensitive(self):
        text = ['Nimeni on Matti Seppälä. Henkilötunnukseni on 010101-123P ja puhelinnumeroni on 0501234567.',
                'olen riikka toivola hetuni on 090909-0000 ja puhelinnumeroni 0441212312']
        app = PersonalDataAnonymizer()
        actual = app.anonymize_everything(text, case_sensitive=True)
        expected = ['Nimeni on [redacted] [redacted]. Henkilötunnukseni on [redacted] ja puhelinnumeroni on [redacted].',
                    'olen riikka toivola hetuni on [redacted] ja puhelinnumeroni [redacted]']
        self.assertEqual(actual, expected)
