"""Contains all code needed to create and manage a Ruby Document object.
A ruby document stores all information on a ruby file that should be
documented. Only ruby files following Workato's connector format are parsed.
The following information is stored:

 - File name
 - Connector name
 - Custom actions
 - Custom triggers
 - Custom methods
"""


class RubyDoc:
    """A collection of documentation on a ruby connector file."""

    def __init__(self, filename):
        self.filename = filename
        self.connector_name = None

        self.custom_actions = []
        self.custom_triggers = []
        self.custom_methods = []
