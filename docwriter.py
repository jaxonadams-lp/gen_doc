"""Contains all code needed to create and manage DocumentationWriter
objects. A DocumentationWriter will write all python and ruby
documentation collected to a new file in the desired format.
"""


from mdutils.mdutils import MdUtils


class DocumentationWriter:
    """Manages new documentation files."""

    def __init__(self, filename, p_name, p_desc=None, pydocs=[], rubydocs=[]):

        self.project_title = p_name
        self.project_description = p_desc
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

        # create file with title and description
        docfile = MdUtils(file_name=self.filename, title=self.project_title)
        if self.project_description is not None:
            docfile.new_header(1, "Description")
            docfile.new_paragraph(self.project_description)
            docfile.new_line("---")

        # add python info
        if len(self.pydocs):
            docfile.new_header(1, "Python Code")
            for pydoc in self.pydocs:
                # python filename header
                filename = pydoc.filename.split("\\")[-1]
                docfile.new_header(2, f"`{filename}`")

                # module docstring
                docfile.new_paragraph(pydoc.module_docstring)

                # imports
                docfile.new_header(3, "Imported Libraries")
                if len(pydoc.imported_libraries):
                    table = ["Module", "Name", "Alias"]
                    lib_list = []
                    for lib in pydoc.imported_libraries:
                        lib_list.extend(
                            [
                                ".".join(lib.module),
                                ".".join(lib.name),
                                lib.alias
                            ]
                        )
                    table.extend(lib_list)
                    docfile.new_table(
                        columns=3,
                        rows=len(pydoc.imported_libraries) + 1,
                        text=table,
                        text_align="center",
                    )
                else:
                    docfile.new_paragraph("*No external libraries used.*")

                # classes
                docfile.new_header(3, "Class Definitions")
                if len(pydoc.classes):
                    class_list = []
                    for class_def in pydoc.classes:
                        class_list.append(class_def.name)
                        class_list.append([class_def.docstring])
                    docfile.new_list(class_list)
                else:
                    docfile.new_paragraph("*No classes defined.*")

                # functions
                docfile.new_header(3, "Function Definitions")
                if len(pydoc.functions):
                    func_list = []
                    for func in pydoc.functions:
                        func_list.append(func.name.replace("_", "\\_"))
                        func_info = []
                        if func.docstring != "Docstring not defined.":
                            func_info.append(func.docstring)
                        else:
                            func_info.append("*Docstring not defined.*")
                        func_info.append("Arguments:")
                        func_info.append(func.args)
                        func_list.append(func_info)
                    docfile.new_list(func_list)
                else:
                    docfile.new_paragraph("*No functions defined.*")
                
                # line break before next file
                docfile.new_line("")
                docfile.new_line("---")

        # save the new file
        docfile.new_table_of_contents(table_title="Contents", depth=2)
        docfile.create_md_file()
