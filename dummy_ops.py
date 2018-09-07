import logging


def get_sensor_reading(sensor_config):
    logging.info("Dummy reading of sensor (channel %d)",
                 sensor_config['ADCChannel'])

    if sensor_config['ADCChannel'] == 2:
        return 50000

    return 100


def water_pot(pot_config):
    print(pot_config)
    logging.info("Dummy watering of pot (relay pin %d)",
                 pot_config['RelayBCMPin'])
