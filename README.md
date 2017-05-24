Smart Thermostat
====================================

This is a smart thermostat using a raspberry pi zero W, automation pHat and an MCP9808.

## Usage
python thermostat_main.py

This will start automatically running your thermostat with debug output. You will likely want this to be run at boot after getting it setup. It also has debug output so you can see when you are heating up and what the actual temperature is.

## Setup
### Thermostat
The fan control is on output 1
The heat control is on relay 1
(There was a problem with fluttering when the heat wasn't isolated from the fan.)

Basic wiring of Red to Ground
White to relay 1 NO (Normally Open)
Green to output 1
*Note* Assumes standard thermostat wiring

### Temperature Sensor
I2C must be enabled on the pi.
The MPC9808 is 5v or 3.3V tolerant so power with 5V so you can use the i2c pins without additional hardware
Recommended: Make sure you can see the sensor and the hat with i2cdetect (Instructions onthe pHate page linked below)

## Test your Thermostat
The code assumes that your furnace knows when it needs to have the fan on for heat. 
(So if the heat is on long enough to turn on the flame, after turning off the flame the furnace keep the fan on, even if we dont turn on the fan in code)

There are two helper scripts to turn on the heat and cooling. Use these to ensure your setup and see if your furnace will control the fan on its own when trying to heat.

## Safety

These are 24V lines. Make sure when dealing with the thermostat you are always working through the
pHat. Otherwise you are going to blow up part of your Pi.

All inputs and relays default to ground or their normal positions upon losing power. If you work with this setup, then in the case of failure your thermostat will stay off.

## Upcoming features:
	io.adafruit.com data tracking
	pushbullet notifications
	Location based input (maybe, this may be out of the scope of this)

## Dependancies
* Requires that the adafruit MCP9808 python library is installed. [Adafruit MCP9808](https://github.com/adafruit/Adafruit_Python_MCP9808)
* Requires the automation pHat is installed. [pHat](https://github.com/pimoroni/automation-hat)

Requires that you have a mosquitto server running. You may want this on this pi or you might want it elsewhere. Just know where it is

## Example Config file

You will need a config file to get MQTT working with this A skeleton one is provided below. It is a normal config that can be parsed by the ConfigParser modules

	[MQTT]
	broker_ip = 
	broker_user = 
	broker_pass = 
	broker_topic =
