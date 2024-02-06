"""Contains all the code needed to create and manage a Directory object.
A Directory holds a list of files and folders (also implemented as
directories). Each file is either a python file or a ruby file.
"""

import os

class Directory:
    """A directory containing python and ruby files."""

    def __init__(self, directory):
        self.directory = directory
        self.name = directory.split("\\")[-1]

        self.files = []
        self.subdirectories = []

        self.locate_files()

    def locate_files(self):
        """Find all python and ruby files in the current directory."""

        subdirs = []
        files = []

        for entry in os.listdir(self.directory):
            if os.path.isfile(f"{self.directory}\\{entry}"):
                if entry.endswith(".py") or entry.endswith(".rb"):
                    files.append(entry)
            elif os.path.isdir(f"{self.directory}\\{entry}"):
                subdirs.append(entry)

        self.files = files
        for dir_name in subdirs:
            new_dir = Directory(
                os.path.normpath(os.path.join(self.directory, dir_name))
            )
            self.subdirectories.append(new_dir)

    def files_present(self):
        """Check if a python or ruby file is stored in the current
        directory.
        """

        if len(self.files):
            return True
        
        for subdir in self.subdirectories:
            if subdir.files_present():
                return True
            
        return False

    def pprint(self, indent=""):
        """Print all files and subdirectories stored."""

        if indent == "":
            print(f"PRINTING TREE FOR {self.name}")

        for filename in self.files:
            print(f"{indent} |-- {filename}")
        for dirname in self.subdirectories:
            if dirname.files_present():
                print(f"{indent} +-- {dirname.name}")
                dirname.pprint(indent + "    ")
