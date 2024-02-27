"""Contains all the code needed to create and manage a Parser object.
A parser reads a file for code that should be documented. Children
of a parser include a PyParser and a RubyParser.
"""


import ast
import re

from pythondoc import PyDoc
from rubydoc import RubyDoc


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
        """Call member functions to populate pydocs with PyDoc instances
        containing documentable file content.
        """

        for fname, f_content in self.load_files():
            self.pydocs.append(PyDoc(fname))

            self.parse_file(fname, f_content)

    def parse_imports(self, node, pydoc):
        """Parse a given AST node for import data and add it to the PyDoc."""

        if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
            if isinstance(node, ast.Import):
                module = []
            else:
                module = node.module.split(".")
            for n in node.names:
                pydoc.add_import(module, n.name.split("."), n.asname)

    def parse_functions(self, node, pydoc):
        """Parse a given AST node for function data and add it to the PyDoc."""

        if isinstance(node, ast.FunctionDef) and node.body:
            # arguments
            args = [a.arg for a in node.args.args]
            docstr = "Docstring not defined."
            # docstring
            first_statement = node.body[0]
            if isinstance(first_statement, ast.Expr):
                if isinstance(first_statement.value, ast.Constant):
                    docstr = first_statement.value.s
            pydoc.add_function_info(node.name, docstr, args)

    def parse_classes(self, node, pydoc):
        """Parse a given AST node for class data and add it to the PyDoc."""

        if isinstance(node, ast.ClassDef) and node.body:
            # class docstring
            docstr = "Docstring not defined."
            if isinstance(node.body[0], ast.Expr):
                if isinstance(node.body[0].value, ast.Constant):
                    docstr =  node.body[0].value.s
            pydoc.add_class_info(node.name, docstr)

    def parse_file(self, fname, f_content):
        """Find the given pydoc by name and update its data."""

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
            self.parse_imports(node, pydoc)
            
            # function data
            self.parse_functions(node, pydoc)

            # class data
            self.parse_classes(node, pydoc)


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

        self.rubydocs = []
        self.load_data()

    def load_data(self):
        """Call member functions to populate rubydocs with RubyDoc instances
        containing documentable file content.
        """

        for fname, f_content in self.load_files():
            match = re.search(self.connector_pattern, f_content)
            if match is not None:
                self.rubydocs.append(RubyDoc(fname))

                match_groups = match.groups()
                self.parse_file(fname, *match_groups)

    def parse_actions(self, rubydoc, action_str):
        """Parse the given string for a list of custom actions."""

        print("\nACTIONS")
        print(action_str)

    def parse_triggers(self, rubydoc, trigger_str):
        """Parse the given string for a list of custom triggers."""

        print("\nTRIGGERS")
        print(trigger_str)

    def parse_methods(self, rubydoc, method_str):
        """Parse the given string for a list of custom methods."""

        print("\nMETHODS")
        print(method_str)

    def parse_file(self, fname, title, actions, triggers, methods):
        """Find the given rubydoc by name and update its data."""

        rubydoc = [doc for doc in self.rubydocs if doc.filename == fname][0]

        # set connector name
        connector_name = title.split(":", 1)[1].strip()
        rubydoc.connector_name = connector_name

        print(f"Workato Connector: {rubydoc.connector_name}")

        # set custom actions
        self.parse_actions(rubydoc, actions)

        # set custom triggers
        self.parse_triggers(rubydoc, triggers)

        # set custom methods
        self.parse_methods(rubydoc, methods)
