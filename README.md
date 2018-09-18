# Raspberry Pi Plant Monitor

<div style="text-align:center">
<img src="https://github.com/abelikoff/pi-plant-monitor/raw/master/misc/installed.jpg" width="640">
</div>

This is a relatively simple system for monitoring and watering
multiple (up to 4) pots.


## Hardware

For the bill of components and assembly instructions see the
[blog post](http://belikoff.net/using-raspberry-pi-to-water-plants).


## Installation

IMPOIRTANT: in order to use the ADC, you need to enable I2C interface
via `raspi-config`.

The system is operated by running
[watering_station](https://github.com/abelikoff/pi-plant-monitor/raw/master/watering_station)
periodically (i.e. hourly), which will keep track of the state of each
pot and initiate watering when needed.

As user **pi** run `crontab -e` and add the invocation of
`watering_station` to your crontab. In my case, it looks like:

```bash
25  *  *  *  *  $HOME/bin/watering_station >> $HOME/log/watering_station.log 2>&1
```

By default the script runs mostly quietly. Run `watering_station -h`
to see the available options.


## Configuration

Copy the example `.watering_station.config` to your home directory and
edit it. Configuration mostly deals with hardware setup (i.e. which
GPIO pins and channels correspond to each pot) and pot- and
sensor-specific cut-off levels for dry soil (which should be
calibrated experimentally).


## Stats processing

The system implements a simple but relatively flexible framework for
collecting the sensor and watering stats. Once stats are gathered,
they can be passed to a _stats processor_ object, which can perform
custom processing of such stats. Such custom stats processor class is
implemented as a subclass of `UpdateProcessor`. Two example processors
are provided:

* `UpdatePrinter` simply prints the stats on _stdout_.
* `UpdateCSVLogger` appends the stats to a CSV file. It also
  demonstrates how such processor can be configured via a special
  section in the configuration file.

It should be easy to implement a class to do more elaborate stats
processing, e.g. uploading them to Google BigQuery, saving in a
database etc.

Stats processor is specified via `update_processor` directive in the
`[general]` section of the configuration file.


## Shutdown button

Raspberry Pi doesn't have any hardware based method to shut down. One
can either turn the power off which is a terrible idea for any OS or
to log into the machine and shut it down via the command line. Neither
is super convenient.

To make it slightly easier, I've added a hardware button connected to
GPIO and a script to power the device off when the button was pressed
for 5 seconds (to avoid accidental presses). The script is called
[shutdown_button](https://github.com/abelikoff/pi-plant-monitor/raw/master/shutdown_button)
(shocking, I know). To install and activate, do the following:

* Copy (or symlink) `shutdown_button` into `~/bin` directory of user
  **pi**.

* By default the script assumes the button is connected to GPIO pin 25.
If it is not, change the `shutdown_button.service` file to pass an
appropriate value via `--pin` option to the script.

* Set up `systemd` configuration for the script and start it:

```bash
sudo cp shutdown_button.service /etc/systemd/system/
sudo systemctl start shutdown_button.service
```

Now you can check the status to verify that the script is running:

```bash
sudo systemctl start shutdown_button.service
```
