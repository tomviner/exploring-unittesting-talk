import re
import os
import pytest

INPUT_FN = '../talk-draft.md'
os.chdir('./code-examples/')


def get_text(fn=INPUT_FN):
    return open(INPUT_FN).read()


def filter_console_snippets(text):
    return re.findall(r'    \$ (.*)', text)


def get_console_snippets():
    text = get_text()
    return filter_console_snippets(text)

@pytest.mark.parametrize('snippet', get_console_snippets())
def test_console_snippets(snippet):
    exit_code = os.system(snippet)
    assert exit_code == 0
