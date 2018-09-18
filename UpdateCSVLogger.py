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


def get_instance(cfg=None):
    """Return an instance of a processor class.
    """

    return UpdateCSVLogger(cfg)


class UpdateCSVLogger(UpdateProcessor):
    def __init__(self, cfg):
        if cfg and "file" in cfg:
            output_file = os.path.expanduser(cfg["file"])
        else:
            output_file = "watering_stats.csv"

        self.file = open(output_file, "a")

        if cfg and "timestamp_format" in cfg:
            self.timestamp_format = cfg["timestamp_format"]
        else:
            self.timestamp_format = "%Y-%m-%d %H:%M:%S"


    def update(self, update_data):
        """
        Process an update.

        See UpdateProcessor.update() for information on arguments.
        """

        s = update_data["timestamp"].strftime(self.timestamp_format + ",")
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
