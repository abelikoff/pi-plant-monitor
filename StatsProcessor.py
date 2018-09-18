#!/usr/bin/env python3
"""
Base class (interface) for a stats processor.

"""

__version__ = "1.0"
__author__ = "Alexander L. Belikoff"
__email__ = "abelikoff@gmail.com"
__copyright__ = "Copyright 2018, Alexander L. Belikoff"
__license__ = "GPLv3"


def get_instance():
    """Return an instance of a processor class.
    """

    return StatsProcessor()


class StatsProcessor:
    def process(self, stats):

        """
        Process new stats.

        Args:
        stats: a dictionary in the following format.

        {
            "timestamp" : datetime : update timestamp

            "updates" : {
                <pot_id> : {
                    "sensor_reading" : <reading>,
                    "cutoff_value" : <sensor cutoff value>,
                    "watered" : True,
                    "second_reading" : <reading after watering>
                }
            }
        }

        """

        raise Exception("not implemented")
