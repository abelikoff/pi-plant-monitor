#!/usr/bin/env python3
"""
An example stats processor that simply prints them.

"""

__version__ = "1.0"
__author__ = "Alexander L. Belikoff"
__email__ = "abelikoff@gmail.com"
__copyright__ = "Copyright 2018, Alexander L. Belikoff"
__license__ = "GPLv3"


from StatsProcessor import StatsProcessor


def get_instance():
    """Return an instance of a processor class.
    """

    return StatsPrinter()


class StatsPrinter(StatsProcessor):
    def process(self, stats):
        """
        Process new stats.

        See StatsProcessor.process() for information on arguments.
        """

        print(stats)
