#!/usr/bin/env python3
"""
Base class (interface) for an update processor.

"""

__version__ = "1.0"
__author__ = "Alexander L. Belikoff"
__email__ = "abelikoff@gmail.com"
__copyright__ = "Copyright 2018, Alexander L. Belikoff"
__license__ = "GPLv3"


def get_instance():
    """Return an instance of a processor class.
    """

    return UpdateProcessor()


class UpdateProcessor:
    #def __init__(self):
    #    raise Exception("not implemented")


    def update(self, update_data):
        """
        Process an update.

        Args:
        update_data: a dictionary with update information.

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
