"""Contains all code needed to create and manage PDFWriter objects.

A PDFWriter generates a pdf consisting of collected documentation.
"""


class PDFWriter:
    """A PDF generator."""

    def __init__(self, pydocs=[], rubydocs=[]):
        
        self.pydocs = pydocs
        self.rubydocs = rubydocs
        for doc in self.pydocs:
            print(doc)
