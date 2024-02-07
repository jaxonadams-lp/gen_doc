"""Contains all code needed to create and manage a Python Document object.
A python document stores all information on a python file that should be
documented. The following information is stored:

 - File name
 - Imported libraries
 - Module Docstring
 - Function names
 - Function docstrings
 - Function parameters
 - Function return values
 - Class names
 - Class docstrings
"""


from collections import namedtuple


class PyDoc:
    """A collection of documentation on a python file."""

    ImportInfo = namedtuple("ImportInfo", "module name alias")
    ClassInfo = namedtuple("ClassInfo", "name docstring")
    FunctionInfo = namedtuple("FunctionInfo", "name docstring args")

    def __init__(self, filename):
        self.filename = filename
        self.module_docstring = None

        self.imported_libraries = []

        # lists of ClassInfo and FunctionInfo named tuples
        self.classes = []
        self.functions = []

    def add_import(self, module, name, alias):
        """Add a new ImportInfo namedtuple to self.imported_libraries."""

        new_import = self.ImportInfo(module, name, alias)
        self.imported_libraries.append(new_import)

    def add_function_info(self, func_name, doc, args):
        """Add a new FunctionInfo namedtuple to self.functions."""

        new_func = self.FunctionInfo(func_name, doc, args)
        self.functions.append(new_func)

    def add_class_info(self, cl_name, doc):
        """Add a new ClassInfo namedtuple to self.classes."""

        new_cl = self.ClassInfo(cl_name, doc)
        self.classes.append(new_cl)

    def pprint(self):
        """Pretty-print class data to the console."""

        print(f"COLLECTED INFO FOR FILE " + self.filename.split("\\")[-1])
        print("------------------------" + "-" * len(self.filename.split("\\")[-1]))

        print("Module docstring:")
        print(self.module_docstring)
        print("\n")

        print("Imported libraries:")
        if not len(self.imported_libraries):
            print("    None")
            print("\n")
        for im in self.imported_libraries:
            print(f"    Module: {'.'.join(im.module)}")
            print(f"      Name: {'.'.join(im.name)}")
            print(f"     Alias: {im.alias}")
            print("\n")

        print("Classes:")
        if not len(self.classes):
            print("    None")
            print("\n")
        for cl in self.classes:
            print("    CLASS " + cl.name)
            print("    " + "Docstring:")
            print("    " * 2 + cl.docstring)
            print("\n")

        print("Functions:")
        if not len(self.functions):
            print("    None")
            print("\n")
        for fn in self.functions:
            print("    FUNCTION " + fn.name)
            print("    " + "Docstring:")
            print("    " * 2 + fn.docstring.replace("    ", "    " * 2))
            print("    " + "Arguments:")
            print("    " * 2 + ", ".join(fn.args) if len(fn.args) else "    " * 2 + "None")
            print("\n")

        print("\n")
