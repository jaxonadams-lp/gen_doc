"""Contains all the code needed to create and manage a Parser object.
A parser reads a file for code that should be documented. Children
of a parser include a PyParser and a RubyParser.
"""


import ast
import re

from pythondoc import PyDoc


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
                args = [a.arg for a in node.args.args]
                docstr = "Docstring not defined."
                # docstring
                first_statement = node.body[0]
                if isinstance(first_statement, ast.Expr):
                    if isinstance(first_statement.value, ast.Constant):
                        docstr = first_statement.value.s
                pydoc.add_function_info(node.name, docstr, args)
            # class definition
            elif isinstance(node, ast.ClassDef) and node.body:
                # class docstring
                docstr = "Docstring not defined."
                if isinstance(node.body[0], ast.Expr):
                    if isinstance(node.body[0].value, ast.Constant):
                        docstr =  node.body[0].value.s
                pydoc.add_class_info(node.name, docstr)


class RubyParser(Parser):
    """A ruby code parser object."""

    # regex matches the following pattern:
    # {
    #     title: "<some string>",
    #     connection: {<some_object_def>},
    #     actions: {<some_object_def},
    #     triggers: {<some_object_def},
    #     methods: {<some_object_def},
    #     object_definitions: {<some_object_def},
    #     pick_lists: {<some_object_def>}
    # }
    # the following fields are captured:
    # title, actions, triggers, methods
    connector_pattern = r'\{[\s\n]*(title:\s*"[^"]*"),[\s\n]*' \
                        r'connection:\s*\{[\w\W]*\},[\w\W]*' \
                        r'(actions:\s*\{[\w\W]*\}),[\w\W]*' \
                        r'(triggers:\s*\{[\w\W}]*\}),[\n\s]*' \
                        r'(methods:\s*\{[\w\W]*\}),[\n\s]*' \
                        r'object_definitions:\s*\{[\w\W]*\},[\n\s]*' \
                        r'pick_lists:\s*\{[\w\W]*\}[\n\s]*\}'

    def __init__(self, files):
        super().__init__(files)

        for fname, f_content in self.load_files():
            print(fname)

            match = re.search(self.connector_pattern, f_content)
            if match is not None:
                print([g for g in match.groups()])
