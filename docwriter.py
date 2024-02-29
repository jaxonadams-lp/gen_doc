"""Contains all code needed to create and manage DocumentationWriter
objects. A DocumentationWriter will write all python and ruby
documentation collected to a new file in the desired format.
"""


from mdutils.mdutils import MdUtils


class DocumentationWriter:
    """Manages new documentation files."""

    def __init__(self, filename, pydocs=[], rubydocs=[]):

        self.filename = filename
        self.format = filename.split(".")[-1]
        self.pydocs = pydocs
        self.rubydocs = rubydocs

    def write_file(self):
        """Delegate the writing of a new file to the proper method
        based on the selected format.
        """

        if self.format == "md":
            return self.write_md()
        # more formats will be added later
    
    def write_md(self):
        """Write a new documentation file in Markdown format."""

        print(f"MOCK WRITE FILE {self.filename}")
