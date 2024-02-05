"""Contains all the code needed to create and manage a Directory object.
A Directory holds a list of files and folders (also implemented as
directories). Each file is either a python file or a ruby file.
"""

class Directory:
    """A directory containing python and ruby files."""

    def __init__(self, directory):
        self.directory = directory

    def locate_files(self):
        """Find all python and ruby files in the current directory."""

        print("Heyooo")
