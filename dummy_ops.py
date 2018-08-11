import logging


def get_sensor_reading(sensor_config):
    logging.info("Dummy reading of sensor (channel %d)",
                 sensor_config['ADCChannel'])
    return 100
