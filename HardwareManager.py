import builtins
import logging
import time

if hasattr(builtins, "FAKE_HARDWARE_MODE"):
    import FakeGPIO as GPIO
    import FakeADS as ADS
else:
    import RPi.GPIO as GPIO
    import Adafruit_ADS1x15 as ADS


class HardwareManager:

    # Gain value for reading voltages from 0 to 4.09V.
    #  - 2/3 = +/-6.144V
    #  -   1 = +/-4.096V
    #  -   2 = +/-2.048V
    #  -   4 = +/-1.024V
    #  -   8 = +/-0.512V
    #  -  16 = +/-0.256V
    # See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.
    GAIN = 1


    def __init__(self):

        self.gpio_initialized = False
        self.adc = None


    def cleanup(self):
        self.__cleanup_adc()
        self.__cleanup_gpio()


    def read_sensor(self, pot_config):
        self.__init_adc()
        channel = pot_config["ADCChannel"]

        logging.debug("Reading sensor for pot %s (%s) (channel %d)",
                      pot_config["id"],
                      pot_config["description"],
                      channel)

        reading = self.adc.read_adc(channel, gain=HardwareManager.GAIN)

        logging.debug("Sensor reading = %d", reading)
        return reading


    def water_pot(self, pot_config):
        self.__init_gpio()
        pin = pot_config['RelayBCMPin']
        duration = pot_config['WateringDuration']

        logging.debug("Watering of pot %s (%s) (relay pin %d)",
                     pot_config["id"],
                     pot_config["description"],
                     pin)

        try:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)
            time.sleep(duration);
            GPIO.output(pin, GPIO.HIGH)

        except KeyboardInterrupt:
            GPIO.output(pin, GPIO.HIGH)
            self.__cleanup_gpio()


    def __init_gpio(self):
        if self.gpio_initialized:
            return

        logging.debug("Initializing GPIO")
        GPIO.setmode(GPIO.BCM)
        self.gpio_initialized = True


    def __cleanup_gpio(self):
        if not self.gpio_initialized:
            return

        logging.debug("Cleaning up GPIO")
        GPIO.cleanup()
        self.gpio_initialized = False



    def __init_adc(self):
        if self.adc:
            return

        logging.debug("Initializing ADC")
        self.adc = ADS.ADS1115()


    def __cleanup_adc(self):
        if not self.adc:
            return

        logging.debug("Cleaning up ADC")
        self.adc = None
