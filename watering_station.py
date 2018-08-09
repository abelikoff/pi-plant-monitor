#!/usr/bin/env python3
"""

<<<PROGRAM DESCRIPTION>>>

"""

import argparse
import configparser
import logging
import os
import pickle
import sys
from collections import defaultdict


__version__ = '1.0'


class PotState:
    def __init__(self):
        self.last_watering_time = None
        self.dry_spell_start_time = None


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
        return self.pot_states[name]


    def load(self):
        #try:
        with open(State.STATE_FILE, "rb") as f:
            self.pot_states = pickle.load(f)

        #except Exception as e:
        #    self.set_default_state()

        logging.debug("Loaded state: %s", self)


    def save(self):
        with open(State.STATE_FILE, "wb") as f:
            pickle.dump(self.pot_states, f)


    def __str__(self):
        s = "=== STATE ===================\n"

        for name, state in self.pot_states.iteritems():
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
        self.target_names = []
        self.sensor_dry_level = defaultdict(int)
        self.max_dry_hours = defaultdict(int)
        self.watering_duration = defaultdict(int)


    def targets(self):
        return self.target_names


    def load(self, filename):
        if not os.path.exists(filename):
            logging.fatal("no config file %s", filename)
            sys.exit(1)

        cfg = configparser.ConfigParser()
        cfg.read(filename)
        self.sensor_names = cfg["general"]["pots"].split()

        for sname in self.sensor_names:

            # sensor level for "dry"

            if "SensorDryLevel" in cfg[sname]:
                dry_level = int(cfg[sname]["SensorDryLevel"])
            else:
                dry_level = Config.DEFAULT_SENSOR_DRY_LEVEL

            if dry_level < 1:
                logging.fatal("bad SensorDryLevel for %s", sname)
                sys.exit(1)

            self.sensor_dry_level[sname] = dry_level

            # max dry period

            if "MaxDryPeriod" in cfg[sname]:
                dry_hours = int(cfg[sname]["MaxDryPeriod"])
            else:
                dry_hours = Config.DEFAULT_MAX_DRY_HOURS

            if dry_hours < 1 or dry_hours > Config.MAX_DRY_HOURS:
                logging.fatal("bad MaxDryPeriod for %s", sname)
                sys.exit(1)

            self.max_dry_hours[sname] = dry_hours

            # watering duration

            if "WateringDuration" in cfg[sname]:
                watering_dur = int(cfg[sname]["WateringDuration"])
            else:
                watering_dur = Config.DEFAULT_WATERING_DURATION

            if watering_dur < 1 or \
                    watering_dur > Config.MAX_WATERING_DURATION:
                logging.fatal("bad WateringDuration for %s", sname)
                sys.exit(1)

            self.watering_duration[sname] = watering_dur




def main(args):
    "Main entry point."

    config = Config()
    config.load(args.config_file)
    pot_names = config.get_pot_names()

    state_mgr = StateManager()

    try:
        state_mgr.load()

    except Exception ex:
        state_mgr.create_new_state(pot_names)

    for name in pot_names:
        pot_config = config.get_pot_config(name)
        pot_state = state_mgr.get_pot_state(name)

        sensor_reading = get_sensor_reading(cfg)
        pot_state.last_sensor_reading_time = datetime.datetime.now()
        needs_watering = update_state_and_decide(sensor_reading,
                                                 pot_config,
                                                 pot_state)

        if needs_watering:
            logging.verbose("will water pot %s", name)
            water_pot(pot_config)
            pot_state.last_watering_time = datetime.datetime.now()
            time.sleep(SECOND_READING_DELAY)
            sensor_reading = get_sensor_reading(cfg)



        # record new data

        # update state

    state.save()









def _parse_args():
    "Parse command line args."

    parser = argparse.ArgumentParser(
        description=globals()['__doc__'],
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-c', '--config-file',
                        dest='config_file',
                        default=os.path.expanduser("~/.watering_station.config"),
                        help='configuration file')
    parser.add_argument('-D', '--debug', action='store_true',
                        dest='debug_mode', default=False,
                        help='debug mode')
    parser.add_argument('-v', '--verbose', action='store_true',
                        dest='verbose_mode', default=False,
                        help='verbose mode')
    parser.add_argument('--version', action='version',
                        version='%(prog)s {version}'.format(version=
                                                            __version__))
    parser.add_argument('args', type=str, nargs='*',
                        help='Arguments to the program')
    return parser.parse_args()


if __name__ == '__main__':
    OPTIONS = _parse_args()

    if OPTIONS.debug_mode:
        logging.basicConfig(level=logging.DEBUG,
                            format='%(levelname)s: %(message)s')
    else:
        logging.basicConfig(format='%(levelname)s: %(message)s')

    try:
        main(OPTIONS)
        sys.exit(0)

    except KeyboardInterrupt as exc: # Ctrl-C
        raise exc


# Local Variables:
# compile-command: "pylint -r n pycan.py"
# end:
