# Raspberry Pi Plant Monitor

![Installed
 system](https://github.com/abelikoff/pi-plant-monitor/raw/master/misc/installed.jpg | width=640)


This is a relatively simple system for monitoring and watering
multiple pots.


## Hardware

For the bill of components and assembly instructions see the
[blog post](http://belikoff.net/using-raspberry-pi-to-water-plants)


## Installation

In order to use the ADC, you need to enable I2C interface via
`raspi-config`.

The system is operated by running `watering_station` periodically
(i.e. hourly), which will keep track of the state of each pot and
initiate watering when needed.

As user `pi` run `crontab -e` and add the invocation of
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


## Shutdown button

Raspberry Pi doesn't have any hardware based method to shut down. One
can either turn the power off which is a terrible idea for any OS or
to log into the machine and shut it down via the command line. Neither
is super convenient.

To make it slightly easier, I've added a hardware button connected to
GPIO and a script to power the device off when the button was pressed
for 5 seconds (to avoid accidental presses). The script is called
[shutdown_button](../blob/master/shutdown_button) (shocking, I
know). To install and activate, do the following:

* Copy (or symlink) `shutdown_button` into `~/bin` directory of user
  *pi*.

* By default the script assumes the button is connected to GPIO pin
  25. If it is not, change the `shutdown_button.service` file to pass
  an appropriate value via `--pin` option to the script.

* Set up `systemd` configuration for the script and start it:

```bash
sudo cp shutdown_button.service /etc/systemd/system/
sudo systemctl start shutdown_button.service
```

Now you can check the status to verify that the script is running:

```bash
sudo systemctl start shutdown_button.service
```
