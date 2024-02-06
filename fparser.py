"""Contains all the code needed to create and manage a Parser object.
A parser reads a file for code that should be documented. Children
of a parser include a PyParser and a RubyParser.
"""


class Parser:
    """A base class representing a code parser object."""

    def __init__(self, files):
        self.files = files

    def load_files(self):
        """Lazily load files into memory to be parsed one at a time."""

        # TODO: implement generator to yield file strings one at a time

        pass


class PyParser(Parser):
    """A python code parser object."""

    def __init__(self, files):
        super().__init__(files)

        print(self.files)


class RubyParser(Parser):
    """A ruby code parser object."""

    def __init__(self, files):
        super().__init__(files)

        print(self.files)
