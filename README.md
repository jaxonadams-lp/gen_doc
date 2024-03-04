...***SAMPLE GENERATED MARKDOWN FILE***...


DocuGen
=======

Contents
========

* [Python Code](#python-code)
	* [`directory.py`](#directorypy)
	* [`docwriter.py`](#docwriterpy)
	* [`fparser.py`](#fparserpy)
	* [`main.py`](#mainpy)
	* [`pythondoc.py`](#pythondocpy)
	* [`rubydoc.py`](#rubydocpy)

# Python Code

## `directory.py`


Contains all the code needed to create and manage a Directory object.
A Directory holds a list of files and folders (also implemented as
directories). Each file is either a python file or a ruby file.

### Imported Libraries

|Module|Name|Alias|
| :---: | :---: | :---: |
||os||

### Class Definitions

- Directory
    - A directory containing python and ruby files.

### Function Definitions

- \_\_init\_\_
    *Docstring not defined.*
    - Arguments:
        - self
        - directory
- locate\_files
    - Find all python and ruby files in the current directory.
    - Arguments:
        - self
- files\_present
    - Check if a python or ruby file is stored in the current
        directory.
        
    - Arguments:
        - self
- files\_by\_ext
    - Return a list of all files, including those in
        subdirectories. Files are filtered by the provided
        extension.
        
    - Arguments:
        - self
        - extension
- pprint
    - Print all files and subdirectories stored.
    - Arguments:
        - self
        - indent
  
  
---
## `docwriter.py`


Contains all code needed to create and manage DocumentationWriter
objects. A DocumentationWriter will write all python and ruby
documentation collected to a new file in the desired format.

### Imported Libraries

|Module|Name|Alias|
| :---: | :---: | :---: |
|mdutils.mdutils|MdUtils||

### Class Definitions

- DocumentationWriter
    - Manages new documentation files.

### Function Definitions

- \_\_init\_\_
    *Docstring not defined.*
    - Arguments:
        - self
        - filename
        - p_name
        - p_desc
        - pydocs
        - rubydocs
- write\_file
    - Delegate the writing of a new file to the proper method
        based on the selected format.
        
    - Arguments:
        - self
- write\_md
    - Write a new documentation file in Markdown format.
    - Arguments:
        - self
  
  
---
## `fparser.py`


Contains all the code needed to create and manage a Parser object.
A parser reads a file for code that should be documented. Children
of a parser include a PyParser and a RubyParser.

### Imported Libraries

|Module|Name|Alias|
| :---: | :---: | :---: |
||ast||
||re||
|pythondoc|PyDoc||
|rubydoc|RubyDoc||

### Class Definitions

- Parser
    - A base class representing a code parser object.
- PyParser
    - A python code parser object.
- RubyParser
    - A ruby code parser object.

### Function Definitions

- \_\_init\_\_
    *Docstring not defined.*
    - Arguments:
        - self
        - files
- load\_files
    - Lazily load files into memory to be parsed one at a time.
    - Arguments:
        - self
- \_\_init\_\_
    *Docstring not defined.*
    - Arguments:
        - self
        - files
- load\_data
    - Call member functions to populate pydocs with PyDoc instances
        containing documentable file content.
        
    - Arguments:
        - self
- parse\_imports
    - Parse a given AST node for import data and add it to the PyDoc.
    - Arguments:
        - self
        - node
        - pydoc
- parse\_functions
    - Parse a given AST node for function data and add it to the PyDoc.
    - Arguments:
        - self
        - node
        - pydoc
- parse\_classes
    - Parse a given AST node for class data and add it to the PyDoc.
    - Arguments:
        - self
        - node
        - pydoc
- parse\_file
    - Find the given pydoc by name and update its data.
    - Arguments:
        - self
        - fname
        - f_content
- \_\_init\_\_
    *Docstring not defined.*
    - Arguments:
        - self
        - files
- load\_data
    - Call member functions to populate rubydocs with RubyDoc instances
        containing documentable file content.
        
    - Arguments:
        - self
- parse\_actions
    - Parse the given string for a list of custom actions.
    - Arguments:
        - self
        - rubydoc
        - action_str
- parse\_triggers
    - Parse the given string for a list of custom triggers.
    - Arguments:
        - self
        - rubydoc
        - trigger_str
- parse\_methods
    - Parse the given string for a list of custom methods.
    - Arguments:
        - self
        - rubydoc
        - method_str
- parse\_file
    - Find the given rubydoc by name and update its data.
    - Arguments:
        - self
        - fname
        - title
        - actions
        - triggers
        - methods
  
  
---
## `main.py`


Generate documentation for all python and ruby files in the given
directory. Expects ruby files to follow the Workato SDK template format.
The documentation generated is intended for internal use within the
Integrations team.

### Imported Libraries

|Module|Name|Alias|
| :---: | :---: | :---: |
||os||
||sys||
|pathlib|Path||
|directory|Directory||
|fparser|PyParser||
|fparser|RubyParser||
|docwriter|DocumentationWriter||

### Class Definitions


*No classes defined.*
### Function Definitions

- get\_path
    - Get a file path from the user.
    - Arguments:
        - message
- main
    - Get a file path from the user and generate code documentation.
    - Arguments:
  
  
---
## `pythondoc.py`


Contains all code needed to create and manage a Python Document object.
A python document stores all information on a python file that should be
documented. The following information is stored:

 - File name
 - Imported libraries
 - Module Docstring
 - Function names
 - Function docstrings
 - Function parameters
 - Class names
 - Class docstrings

### Imported Libraries

|Module|Name|Alias|
| :---: | :---: | :---: |
|collections|namedtuple||

### Class Definitions

- PyDoc
    - A collection of documentation on a python file.

### Function Definitions

- \_\_init\_\_
    *Docstring not defined.*
    - Arguments:
        - self
        - filename
- add\_import
    - Add a new ImportInfo namedtuple to self.imported_libraries.
    - Arguments:
        - self
        - module
        - name
        - alias
- add\_function\_info
    - Add a new FunctionInfo namedtuple to self.functions.
    - Arguments:
        - self
        - func_name
        - doc
        - args
- add\_class\_info
    - Add a new ClassInfo namedtuple to self.classes.
    - Arguments:
        - self
        - cl_name
        - doc
- pprint
    - Pretty-print class data to the console.
    - Arguments:
        - self
  
  
---
## `rubydoc.py`


Contains all code needed to create and manage a Ruby Document object.
A ruby document stores all information on a ruby file that should be
documented. Only ruby files following Workato's connector format are parsed.
The following information is stored:

 - File name
 - Connector name
 - Custom actions
 - Custom triggers
 - Custom methods

### Imported Libraries


*No external libraries used.*
### Class Definitions

- RubyDoc
    - A collection of documentation on a ruby connector file.

### Function Definitions

- \_\_init\_\_
    *Docstring not defined.*
    - Arguments:
        - self
        - filename
  
  
---
