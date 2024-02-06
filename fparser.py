"""Contains all the code needed to create and manage a Parser object.
A parser reads a file for code that should be documented. Children
of a parser include a PyParser and a RubyParser.
"""


import ast


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

        docstrings = {
            "module_doc": None,
            "class_docs": [],
            "function_docs": [],
        }

        tree = ast.parse(f_content, filename=fname)

        # check module-level docstring
        if tree and isinstance(tree, ast.Module): # if tree is a module
            if tree.body and isinstance(tree.body[0], ast.Expr): # if first element is an expression
                module_docstring = tree.body[0].value.s # get the expression val as a string
                docstrings["module_doc"] = module_docstring

        # walk through syntax tree looking for docstrings
        fn_docs = []
        cl_docs = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.body:
                # function docstring
                first_statement = node.body[0]
                if isinstance(first_statement, ast.Expr):
                    if isinstance(first_statement.value, ast.Constant):
                        fn_docs.append({node.name: first_statement.value.s})
            elif isinstance(node, ast.ClassDef) and node.body:
                # class docstring
                if isinstance(node.body[0], ast.Expr):
                    if isinstance(node.body[0].value, ast.Constant):
                        cl_docs.append({node.name: node.body[0].value.s})

        docstrings["class_docs"] = cl_docs
        docstrings["function_docs"] = fn_docs

        self.data[fname]["docstrings"] = docstrings


class RubyParser(Parser):
    """A ruby code parser object."""

    def __init__(self, files):
        super().__init__(files)
