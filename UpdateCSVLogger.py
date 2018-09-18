#!/usr/bin/env python3
"""
An update processor that saves updates in a CSV file

"""

__version__ = "1.0"
__author__ = "Alexander L. Belikoff"
__email__ = "abelikoff@gmail.com"
__copyright__ = "Copyright 2018, Alexander L. Belikoff"
__license__ = "GPLv3"


from UpdateProcessor import UpdateProcessor
import os


def get_instance():
    """Return an instance of a processor class.
    """

    return UpdateCSVLogger()


class UpdateCSVLogger(UpdateProcessor):
    def __init__(self):
        #self.file = open(os.path.expanduser("~/log/stats.csv"), "a")
        self.file = open(os.path.expanduser("~/stats.csv"), "a")


    def update(self, update_data):
        """
        Process an update.

        See UpdateProcessor.update() for information on arguments.
        """

        s = update_data["timestamp"].strftime("%Y-%m-%d %H:%M:%S,")
        separator = ""

        for pot in sorted(update_data["pots"].keys()):
            pot_data = update_data["pots"][pot]

            if "watered" in pot_data:
                watered = '"Yes"'
                second_reading = pot_data["second_reading"]
            else:
                watered = ""
                second_reading = ""

            s += '%s"%s",%d,%d,%s,%s' % (separator,
                                          pot,
                                          pot_data["sensor_reading"],
                                          pot_data["cutoff_value"],
                                          watered,
                                          second_reading)
            separator = ','

        self.file.write(s + '\n')
