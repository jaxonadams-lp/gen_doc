"""Generate documentation for all python and ruby files in the given
directory. Expects ruby files to follow the Workato SDK template format.
The documentation generated is intended for internal use within the
Integrations team.
"""


import os
import sys
from pathlib import Path

from directory import Directory
from fparser import PyParser, RubyParser


def get_path(message):
    """Get a file path from the user."""

    print(message)
    print(f"Current directory: {os.getcwd()}")
    path_in = input("  >> ")
    print("\n")

    project_path = f"{Path.home()}/{path_in}"

    print(f"Path: {path_in}")
    user_conf = input("Is this the correct path? [Y/n] >> ")

    if user_conf not in ["Y", "y", "yes", ""]:
        print("\n")
        return get_path(message)

    return project_path


def main():
    """Get a file path from the user and generate code documentation."""

    ascii_title = """
 _____                        _____              
|  __ \                      / ____|             
| |  | |  ___    ___  _   _ | |  __   ___  _ __  
| |  | | / _ \  / __|| | | || | |_ | / _ \| '_ \ 
| |__| || (_) || (__ | |_| || |__| ||  __/| | | |
|_____/  \___/  \___| \__,_| \_____| \___||_| |_|
                                                 
                                                 
    """

    os.chdir(Path.home())

    print(ascii_title)

    project_path = get_path("Please enter the path to the project you'd like documented.")

    try:
        os.chdir(project_path)
    except FileNotFoundError:
        print(f"Error: unable to locate directory from path '{project_path}'")
        sys.exit("\n")

    print(f"\nCurrent directory: {os.getcwd()}\n")

    directory = Directory(os.getcwd())
    directory.pprint()

    print("\n")

    pyparser = PyParser(directory.files_by_ext(".py"))
    # rbparser = RubyParser(directory.files_by_ext(".rb"))

    out_path = get_path("Please enter the full path (including a filename) to"
                        " which you'd like the documentation exported.")

    # for docdata in pyparser.pydocs:
    #     docdata.pprint()


# !---------------------------------------------------------------------------
if __name__ == "__main__":
    main()
