import os
import re
from textwrap import dedent

import markdown
import pytest
from pyquery import PyQuery

INPUT_FN = '../talk-draft.md'
os.chdir('./code-examples/')


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
    return [snip for snip in snips if not re.match(r'\$ ', snip)]


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

@pytest.mark.parametrize('snippet', get_python_snippets())
def test_python_snippets(snippet):
    import unittest, nose, nose2, pytest
    exec(snippet, {
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
        })