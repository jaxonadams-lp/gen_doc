"""Contains all the code needed to create and manage a Parser object.
A parser reads a file for code that should be documented. Children
of a parser include a PyParser and a RubyParser.
"""


import re

from icecream import ic # TODO: REMOVE ME


class Parser:
    """A base class representing a code parser object."""

    def __init__(self, files):
        self.files = files

    def load_files(self):
        """Lazily load files into memory to be parsed one at a time."""

        for fname in self.files:
            with open(fname) as f:
                yield fname, f.read()

        pass


class PyParser(Parser):
    """A python code parser object."""

    def __init__(self, files):
        super().__init__(files)

        self.data = { fname: {} for fname in self.files }
        self.load_data()

        print(self.data)

    def load_data(self):
        """Call member functions to populate the data attribute
        with code that should be documented.
        """

        for fname, f_content in self.load_files():
            # TODO: call functions to populate self.data
            self.add_docstrings(fname, f_content)

    def add_docstrings(self, fname, f_content):
        """Read the given file for all docstrings, adding them to self.data"""

        # TODO: FIX ME -- exclude triple-quoted fstrings (f"""somestr""")
        ds_pattern = r'(\'\'\'(.*?)\'\'\'|\"\"\"(.*?)\"\"\")'
        ds_matches = re.finditer(ds_pattern, f_content, re.DOTALL)
        docstrings = [match[1] or match[2] for match in ds_matches]

        self.data[fname]["docstrings"] = docstrings


class RubyParser(Parser):
    """A ruby code parser object."""

    def __init__(self, files):
        super().__init__(files)
