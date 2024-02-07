"""Contains all the code needed to create and manage a Parser object.
A parser reads a file for code that should be documented. Children
of a parser include a PyParser and a RubyParser.
"""


import ast

from pydoc import PyDoc


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

        self.pydocs = []
        self.load_data()

        for doc in self.pydocs:
            doc.pprint()

    def load_data(self):
        """Call member functions to populate the data attribute
        with code that should be documented.
        """

        for fname, f_content in self.load_files():
            self.pydocs.append(PyDoc(fname))

            self.parse_file(fname, f_content)

    def parse_file(self, fname, f_content):
        """Read the given file for all docstrings, adding them to self.data"""

        pydoc = [doc for doc in self.pydocs if doc.filename == fname][0]

        tree = ast.parse(f_content, filename=fname)

        # check module-level docstring
        if tree and isinstance(tree, ast.Module): # if tree is a module
            if tree.body and isinstance(tree.body[0], ast.Expr): # if first element is an expression
                module_docstring = tree.body[0].value.s # get the expression val as a string
                pydoc.module_docstring = module_docstring

        # walk through syntax tree looking for data
        for node in ast.walk(tree):
            # import
            if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                if isinstance(node, ast.Import):
                    module = []
                else:
                    module = node.module.split(".")
                for n in node.names:
                    pydoc.add_import(module, n.name.split("."), n.asname)
            
            # function definition
            elif isinstance(node, ast.FunctionDef) and node.body:
                # function docstring
                args = [a.arg for a in node.args.args]
                first_statement = node.body[0]
                if isinstance(first_statement, ast.Expr):
                    if isinstance(first_statement.value, ast.Constant):
                        pydoc.add_function_info(node.name, first_statement.value.s, args)
            # class definition
            elif isinstance(node, ast.ClassDef) and node.body:
                # class docstring
                if isinstance(node.body[0], ast.Expr):
                    if isinstance(node.body[0].value, ast.Constant):
                        pydoc.add_class_info(node.name, node.body[0].value.s)


class RubyParser(Parser):
    """A ruby code parser object."""

    def __init__(self, files):
        super().__init__(files)
