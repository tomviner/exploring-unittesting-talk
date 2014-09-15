import os
import re
from textwrap import dedent

import markdown
import pytest
from pyquery import PyQuery

INPUT_FN = '../talk-draft.md'
try:
    os.chdir('./code-examples/')
except OSError:
    pass


def get_code_blocks(fn=INPUT_FN):
    text = open(fn or INPUT_FN).read().decode('utf-8')
    html = markdown.markdown(text)
    dom = PyQuery(html)
    code_blocks = dom('code')
    return [block.text.strip() for block in code_blocks
        if '\n' in block.text] # remove inline code

def get_console_snippets(fn=None):
    console_pattern = r'(?:^|\n)\s*\$ '
    snips = get_code_blocks(fn)
    for snip in snips:
        if not snip or not re.match(console_pattern, snip):
            continue
        for cmd in re.split(console_pattern, snip):
            if cmd:
                yield cmd

def get_python_snippets(fn=None):
    snips = get_code_blocks(fn)
    return [snip for snip in snips
        # exclude console commands
        if not re.match(r'\$ ', snip)
        # exclude test run results
            and not 'Error' in snip and '.py ' not in snip]


def test_get_console_snippets_simple():
    snips = get_console_snippets(fn='./test_example_simple.md')
    expected = ["unwanted, non-python, console line", "console more"]
    assert list(snips) == expected

def test_get_python_snippets_complex():
    snips = get_python_snippets(fn='./test_example_complex.md')
    expected = ["a", dedent("""
    import unittestz

    class TestAdd(unittest.TestCase):
        def test_add(self):
            self.assertEqual(add(1, 1), 2)""").strip(),
    dedent("""
    def add(a, b):
        return a + b""").strip(),
    dedent("""
    import unittest

    class TestAdd(unittest.TestCase):
        def test_add(self):
            self.assertEqual(add(1, 1), 2)""").strip()]
    assert snips == expected

def test_get_python_snippets_simple():
    snips = get_python_snippets(fn='./test_example_simple.md')
    expected = ["""1""",
    dedent("""
    2a

    2bi
        2bii""").strip(),
    dedent("""
    3a
    3b""").strip(), dedent("""
    4a

    4b""").strip()]
    assert snips == expected


@pytest.mark.parametrize('snippet', get_console_snippets())
def test_console_snippets(snippet):
    exit_code = os.system(snippet)
    assert exit_code == 0

import unittest, nose, nose2, pytest
GIVENS = {
    'unittest': unittest,
    'nose': nose,
    'nose2': nose2,
    'pytest': pytest,
    'result': 0,
    'result2': float('nan'),
    'expected': 0,
    'purl': '',
    # omg, I'm going to hell
    # here we make a self with the union of attrs
    'self': type('UnitNose', (unittest.TestCase,), vars(nose.tools))
}

@pytest.mark.parametrize('snippet', get_python_snippets())
def test_exec_python_snippets(snippet):
    exec(snippet, GIVENS)

# Still pretty hacky
def write_python_snippets():
    libs = 'unittest nose pytest'.split()
    def non_marked(lib, snip):
        if lib != 'pytest':
            return False
        pytest_words = ('test_', 'assert ')
        unmatched = not any(l in snip for l in libs)
        return unmatched and any(word in snip for word in pytest_words)
    snips = get_python_snippets()
    unmatched = list(snips)
    for lib in libs:
        with open('test_extracted_{}.py'.format(lib), 'w') as f:
            f.write('import {}\n'.format(lib))
            f.write('from extracted_sut import *\n\n')
            f.write("self = type('UnitNose', (__import__('unittest').TestCase,), vars(__import__('nose').tools))\n\n")
            f.write('result, expected = 0, 0\n\n')
            for snip in snips:
                if lib in snip or non_marked(lib, snip):
                    f.write(snip+'\n\n# ---\n\n')
                    unmatched.remove(snip)
    with open('extracted_sut.py', 'w') as f:
        if unmatched:
            for snip in unmatched:
                f.write(snip+'\n\n# ---\n\n')


if __name__ == '__main__':
    write_python_snippets()
