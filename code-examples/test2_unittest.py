import unittest

def my_spell_checker(file_or_text):
    dictionary_path = '/etc/dictionaries-common/words'
    dictionary_words = open(dictionary_path).read().decode('utf-8').splitlines()
    try:
        text = file_or_text.read().decode('utf-8')
    except AttributeError:
        text = file_or_text
    for word in text.split():
        if word not in dictionary_words:
            return False
    return True


class TestMyDataRow(unittest.TestCase):
    dictionary_path = '/etc/dictionaries-common/words'

    def setUp(self):
        self.file = open('/tmp/test_file.tmp', 'w+')
        self.file.write('evil monkey')
        self.file.seek(0)

    def test_spell_checker_with_text(self):
        text = 'cat'
        result = my_spell_checker(text)
        self.assertTrue(result)

    def test_spell_checker_with_file(self):

        result = my_spell_checker(self.file)
        self.assertTrue(result)
