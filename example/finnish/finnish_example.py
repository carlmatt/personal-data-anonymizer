import datetime
import pandas as pd
from personal_data_anonymizer import PersonalDataAnonymizer


app = PersonalDataAnonymizer()

# Replace the test_file with your file of choice
test_file = 'tuntematon_sotilas_100000_rows.xlsx'

test_text = pd.read_excel(f'example/finnish/test_sets/{test_file}',
                          header=None).iloc[:, 0].to_list()

word_count = 0
for i in range(len(test_text)): word_count = word_count + len(test_text[i].split())

start_time = datetime.datetime.now()
test_text_anonymized = app.anonymize_everything(test_text, case_sensitive=False)
end_time = datetime.datetime.now()

print(f'Anonymized {word_count} words of text in {end_time - start_time}.')
