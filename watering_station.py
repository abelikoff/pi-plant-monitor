#!/usr/bin/env python3
"""
Monitor moisture level of multiple pots and water them when needed.

Usage:
    See the help screen ('watering_station.py -h') for options.

    The program is intended to be run periodically (i.e. via cron). It
    keeps the state between runs.

Configuration:
    Configuration is done via a config file (by default,
    ~/.watering_station.config or specified via '-c' option). See the supplied
    config file for example configuration.
"""

__version__ = "1.0"
__author__ = "Alexander L. Belikoff"
__email__ = "abelikoff@gmail.com"
__copyright__ = "Copyright 2018, Alexander L. Belikoff"
__license__ = "GPLv3"


import argparse
import builtins
import configparser
import datetime
import logging
import os
import pickle
import sys
import time


class PotState:
    def __init__(self):
        self.last_watering_time = None
        self.dry_spell_start_time = None


    def __str__(self):
        s = "["

        if self.last_watering_time:
            s += self.last_watering_time.strftime("last watered: %Y-%m-%d %H:%M:%S, ")

        if self.dry_spell_start_time:
            s += self.dry_spell_start_time.strftime("dry since: %Y-%m-%d %H:%M:%S")

        s += "]"
        return s


class StateManager:
    STATE_FILE = "test.status"
    # FIXME
    #STATE_FILE = "/var/lock/watering_station.status"

    def __init__(self):
        self.pot_states = {}


    def create_new_state(self, pot_names):
        for name in pot_names:
            self.pot_states[name] = PotState()


    def get_pot_state(self, pot_name):
        return self.pot_states[pot_name]


    def load(self):
        #try:
        with open(StateManager.STATE_FILE, "rb") as f:
            self.pot_states = pickle.load(f)

        #except Exception as e:
        #    self.set_default_state()

        logging.debug("Loaded state:\n%s", self)


    def save(self):
        with open(StateManager.STATE_FILE, "wb") as f:
            pickle.dump(self.pot_states, f)


    def __str__(self):
        s = "=== STATE ===================\n"

        for name, state in self.pot_states.items():
            s += "%-16s  %s\n" % (name, state)

        s += "============================="
        return s


class Config:
    DEFAULT_SENSOR_DRY_LEVEL = 100000 # FIXME
    DEFAULT_MAX_DRY_HOURS = 6
    DEFAULT_WATERING_DURATION = 10

    MAX_DRY_HOURS = 48
    MAX_WATERING_DURATION = 15


    def __init__(self):
        self.pot_names = []
        self.pot_configs = {}


    def get_pot_names(self):
        return self.pot_names


    def get_pot_config(self, name):
        return self.pot_configs[name]


    def load(self, filename):
        if not os.path.exists(filename):
            logging.fatal("no config file %s", filename)
            sys.exit(1)

        cfg = configparser.ConfigParser()
        cfg.read(filename)
        self.pot_names = cfg["general"]["pots"].split()
        already_configured_channels = []
        already_configured_pins = []

        for sname in self.pot_names:
            pot_config = { "id" : sname }

            if "description" in cfg[sname]:
                pot_config["description"] = cfg[sname]["description"]
            else:
                pot_config["description"] = sname

            # sensor level for "dry"

            value = self._parse_parameter(cfg[sname],
                                          "SensorDryLevel",
                                          Config.DEFAULT_SENSOR_DRY_LEVEL,
                                          bounds = [1, 1000000])
            pot_config["SensorDryLevel"] = value

            # max dry period

            value = self._parse_parameter(cfg[sname],
                                          "MaxDryPeriod",
                                          Config.DEFAULT_MAX_DRY_HOURS,
                                          bounds = [1, Config.MAX_DRY_HOURS])
            pot_config["MaxDryPeriod"] = value

            # watering duration

            value = self._parse_parameter(cfg[sname],
                                          "WateringDuration",
                                          Config.DEFAULT_WATERING_DURATION,
                                          bounds = [1, Config.MAX_WATERING_DURATION])
            pot_config["WateringDuration"] = value

            # ADC channel

            value = self._parse_parameter(cfg[sname],
                                          "ADCChannel",
                                          -1,
                                          bounds = [0, 3])

            if value in already_configured_channels:
                logging.fatal("duplicate ADC channel: %d", value)
                sys.exit(1)

            pot_config["ADCChannel"] = value
            already_configured_channels.append(value)

            # Relay pin

            value = self._parse_parameter(cfg[sname],
                                          "RelayBCMPin",
                                          -1,
                                          bounds = [0, 50])

            if value in already_configured_pins:
                logging.fatal("duplicate relay pin: %d", value)
                sys.exit(1)

            pot_config["RelayBCMPin"] = value
            already_configured_pins.append(value)

            self.pot_configs[sname] = pot_config


    def _parse_parameter(self, cfg, key, default_val, bounds = None):
        if key in cfg:
            value = int(cfg[key])
        else:
            value = default_val

        if bounds and (value < bounds[0] or value > bounds[1]):
            logging.fatal("bad value for %s: %d", key, value)
            sys.exit(1)

        return value


def update_state_and_decide(new_reading, pot_config, pot_state):
    """
    Use the new sensor reading to update the pot state and to decide
    whether watering is needed.

    Args:
        new_reading: New sensor reading.
        pot_config: Pot configuration.
        pot_state: Pot state.

    Returns:
        True, if watering is needed; otherwise False.
    """

    if new_reading < pot_config["SensorDryLevel"]: # soil is wet enough
        if pot_state.dry_spell_start_time:
            pot_state.dry_spell_start_time = None
            logging.debug("dry spell stopped for pot %s",
                          pot_config["description"])
        else:
            logging.debug("pot %s still moist enough",
                          pot_config["description"])

        return False

    # From this point on we are dealing with dry soil

    num_dry_hours = 0

    if not pot_state.dry_spell_start_time:
        pot_state.dry_spell_start_time = datetime.datetime.now()
        logging.debug("dry spell started for pot %s",
                      pot_config["description"])
    else:
        num_dry_hours = datetime.datetime.now() - pot_state.dry_spell_start_time
        num_dry_hours = num_dry_hours.total_seconds() / 3600.0
        logging.debug("dry spell for %.1f hrs for pot %s (since %s)",
                      num_dry_hours,
                      pot_config["description"],
                      pot_state.dry_spell_start_time.strftime("%Y-%m-%d %H:%M"))

    return True


def main(args):

    SECOND_READING_DELAY = 30   # after watering, delay and read again
    config = Config()
    config.load(args.config_file)
    pot_names = config.get_pot_names()

    if args.fake_mode:
        builtins.FAKE_HARDWARE_MODE = True

    import HardwareManager
    hw_manager = HardwareManager.HardwareManager()

    state_mgr = StateManager()

    try:
        state_mgr.load()

    except Exception as ex:
        state_mgr.create_new_state(pot_names)

    for name in pot_names:
        pot_config = config.get_pot_config(name)
        pot_state = state_mgr.get_pot_state(name)

        sensor_reading = hw_manager.read_sensor(pot_config)
        pot_state.last_sensor_reading_time = datetime.datetime.now()
        needs_watering = update_state_and_decide(sensor_reading,
                                                 pot_config,
                                                 pot_state)

        if needs_watering:
            logging.info("will water pot %s", name)
            hw_manager.water_pot(pot_config)
            pot_state.last_watering_time = datetime.datetime.now()
            logging.debug("pausing before second reading of the sensor")
            time.sleep(SECOND_READING_DELAY)
            sensor_reading = hw_manager.read_sensor(pot_config)



        # record new data

        # update state
    state_mgr.save()


def _parse_args():
    """
    Parse command line args.
    """

    parser = argparse.ArgumentParser(
        description=globals()["__doc__"],
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-c", "--config-file",
                        dest="config_file",
                        default=os.path.expanduser("~/.watering_station.config"),
                        help="configuration file")
    parser.add_argument("-D", "--debug", action="store_true",
                        dest="debug_mode", default=False,
                        help="debug mode")
    parser.add_argument("--fake", action="store_true",
                        dest="fake_mode", default=False,
                        help="Fake hardware operations")
    parser.add_argument("-v", "--verbose", action="store_true",
                        dest="verbose_mode", default=False,
                        help="verbose mode")
    parser.add_argument("--version", action="version",
                        version="%(prog)s {version}".format(version=
                                                            __version__))
    parser.add_argument("args", type=str, nargs="*",
                        help="Arguments to the program")
    return parser.parse_args()


if __name__ == "__main__":
    OPTIONS = _parse_args()

    if OPTIONS.debug_mode:
        logging.basicConfig(level=logging.DEBUG,
                            format="%(levelname)s: %(message)s")
    else:
        logging.basicConfig(format="%(levelname)s: %(message)s")

    try:
        main(OPTIONS)
        sys.exit(0)

    except KeyboardInterrupt as exc: # Ctrl-C
        raise exc


# Local Variables:
# compile-command: "pylint -r n pycan.py"
# end:
