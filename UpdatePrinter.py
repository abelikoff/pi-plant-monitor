#!/usr/bin/env python3
"""
An example update processor that simply prints an update.

"""

__version__ = "1.0"
__author__ = "Alexander L. Belikoff"
__email__ = "abelikoff@gmail.com"
__copyright__ = "Copyright 2018, Alexander L. Belikoff"
__license__ = "GPLv3"


from UpdateProcessor import UpdateProcessor


def get_instance():
    """Return an instance of a processor class.
    """

    return UpdatePrinter()


class UpdatePrinter(UpdateProcessor):
    def update(self, update_data):
        """
        Process an update.

        See UpdateProcessor.update() for information on arguments.
        """

        print(update_data)
