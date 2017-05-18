###########################################
# This is the auto thermostat

# It depends on a particular hardware setup
# defined in the README.md
# 
# There are a few defines that you can mess
# with in here for the type of temperature
# you would like to hold
#
# Currently changing the target temperature is
# not supported without restarting.
# Also, eventually this should be split
# into multiple threads for reading temp
# and performing tasks.
##########################################

import automationhat
import thread
import time
import Adafruit_MCP9808.MCP9808 as MCP9808

def c_to_f(c):
	return c * 9.0 / 5.0 +32 #Mostly need this for verification 

# Returns deviation from target temperature unless it is within temp_slop
# In which case it returns True
def is_deviated(t):
   	if abs(target_temp - t ) > temp_slop:
		return target_temp - t
	else:
		return False

def is_at_temp(t):
	if heating and ( t > target_temp ):
		return True
	if cooling and ( t < target_temp ):
		return True
	if not heating and not cooling:
		print "is_at_temp is being used incorrectly"
		return True
	return False	
		

#Assumes fan is on OUTPUT 1
def fan_on():
	automationhat.output.one.on()

def fan_off():
	automationhat.output.one.off()
#Assumes furnace is on OUTPUT 2
def furnace_on():
	automationhat.relay.one.on()

def furnace_off():
	automationhat.relay.one.off()

def heat_up():
#	fan_on()
#	time.sleep(fan_dwell)
	furnace_on()

def cool_down():
	fan_on()

def turn_off():
	furnace_off()
#	time.sleep(fan_dwell)
	fan_off()

sensor = MCP9808.MCP9808()
sensor.begin()
target_temp = 21.11 #Value is in Celcius
temp_slop = 1.0 #How much on either side before we need to do something about it
fan_dwell = (1 * 60) #How long to keep the fan on before and after furnace (seconds)

operating = False #This is safe because values are grounded on phat when script stops
heating = False
cooling = False

while True:
  temp = sensor.readTempC()
  print('Temperature: {0:0.3F}*C'.format(temp) )
  print('In range? ' + str(is_deviated(temp)))
  print('Heating? ' + str(heating))
  print('Cooling? ' + str(cooling))
  deviated = is_deviated(temp)
  if deviated is not False:
	if not operating: #Don't need to do it again if we are already doing something 
		operating = True #Make sure we know we need to turn off
		if deviated < 0: #Too hot cool down
			print "Cooling down"
			cooling = True
			thread.start_new_thread(cool_down, ())
		else: #Too cold, heat up
			print "Heating up"
			heating = True
			thread.start_new_thread(heat_up, ())
  else:
	if operating and is_at_temp(temp): #We are in range now but still operating, turn things off
		
		print "Now in range, shutting down"
		thread.start_new_thread(turn_off, ())
		heating = False
		cooling = False
  operating = heating or cooling
  #for clairity in the output
  print()
  print()
  time.sleep(1.0) #Time between each read

