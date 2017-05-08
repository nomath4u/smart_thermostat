Temporary README to get the repo up.

This is a smart thermostat using a raspberry pi zero W, automation pHat and an MCP9808.

The fan control is on output 1

The heat control is on relay 1

There was a problem with fluttering when the heat wasn't isolated from the fan.

Basic wiring of Red to Ground
White to relay 1
Green to output 1

The code assumes that your furnace knows when it needs to have the fan on for heat. 
(So if the heat is on long enough to turn on the flame, after turning off the flame the furnace keep the fan on, even if we dont turn on the fan in code)

Upcoming features:
	Prettier readme
	io.adafruit.com data tracking
	pushbullet notifications
	temperature setpoint control without restart
	Location based input (maybe, this may be out of the scope of this)

Requires that the adafruit MCP9808 python library is installed
