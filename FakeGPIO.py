"""Bare-bones fake implementation of RaspberryPI GPIO module.
"""

__author__ = "Alexander L. Belikoff"
__email__ = "abelikoff@gmail.com"
__copyright__ = "Copyright 2018, Alexander L. Belikoff"
__license__ = "GPLv3"


BCM = 1                         # BCM mode flag (only used for API compatibility)
OUT = 1                         # GPIO direction flag.
LOW = 1                         # GPIO level
HIGH = 1                        # GPIO level


def setmode(mode):
    """
    Dummy analogue for GPIO.setmode().
    """
    pass


def setup(pin, mode):
    """
    Dummy analogue for GPIO.setup().
    """
    pass


def output(pin, level):
    """
    Dummy analogue for GPIO.output().
    """
    pass


def cleanup():
    """
    Dummy analogue for GPIO.cleanup().
    """
    pass
