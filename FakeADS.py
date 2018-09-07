"""Bare-bones fake implementation of AdaFruit Adafruit_ADS1x15
module.
"""

__author__ = "Alexander L. Belikoff"
__email__ = "abelikoff@gmail.com"
__copyright__ = "Copyright 2018, Alexander L. Belikoff"
__license__ = "GPLv3"


class fake_adc:
    """Fake ADS1115 object.

    Only implements fake read_adc() method.
    """
    def read_adc(self, channel, gain):
        """Read and return value from an analog sensor via ADC through channel
        specified.
        """
        return 100000

def ADS1115():
    """Return fake ADS1115 object.
    """
    return fake_adc()
