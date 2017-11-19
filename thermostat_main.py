###########################################
# This is the auto thermostat

# It depends on a particular hardware setup
# defined in the README.md
# 
# There are a few defines that you can mess
# with in here for the type of temperature
# you would like to hold
#
##########################################

import automationhat
import thread
from threading import Timer
import time
import Adafruit_MCP9808.MCP9808 as MCP9808
import paho.mqtt.client as mqtt
import ConfigParser

def c_to_f(c):
	return c * 9.0 / 5.0 +32 #Mostly need this for verification 

# Returns deviation from target temperature unless it is within temp_slop
# In which case it returns True
#def is_deviated(t):
#   	if abs(target_temp - t ) > temp_slop:
#                print "Deviated"
#		return target_temp - t
#	else:
#                print "Not deviated"
#		return False
def is_deviated_heat(t):
   	if (target_temp - t ) > temp_slop:
                print "Deviated"
		return target_temp - t
	else:
                print "Not deviated"
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
	furnace_on()

def cool_down():
	fan_on()

def turn_off():
	furnace_off()
	fan_off()

def set_target_temp(t):
	global target_temp
	target_temp = t

def on_connect(client, userdata, flags, rc):
	client.subscribe(topic)

def on_message(client, userdata,msg):
	global temp_changed
	set_target_temp(float(msg.payload))
	print("got a message")
	temp_changed = True

def send_temp(temp):
        client.publish(cur_temp_topic, payload=round(temp,1))

def timer_timeout():
        global temp
        global timing
	print "Timer ended"
	send_temp(temp)
        timing = False
#Config file stuff
Config = ConfigParser.ConfigParser()
Config.read("./config.conf")

#Mosquitto settings
broker = Config.get("MQTT", "broker_ip") 
broker_port = 1883
broker_user = Config.get("MQTT", "broker_user") 
brokerpass = Config.get("MQTT", "broker_pass") 
topic = Config.get("MQTT", "broker_topic") 
cur_temp_topic = Config.get("MQTT", "broker_cur_temp_topic")
timeout= 10 
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker, broker_port, timeout)

#Start with everything off
furnace_off()
fan_off()

sensor = MCP9808.MCP9808()
sensor.begin()
target_temp = 23.11 #Value is in Celcius
temp_slop = 1.0 #How much on either side before we need to do something about it
fan_dwell = (1 * 60) #How long to keep the fan on before and after furnace (seconds)

operating = False #This is safe because values are grounded on phat when script stops
heating = False
cooling = False
temp_changed = False #Indicator that the set temperature needs to be serviced
temp =  -99.9
timing = False

while True:
  #Need to periodically check MQTT without blocking
  client.loop(timeout=1.0, max_packets=1)

  #if not timing:
  #  print "Starting Timer"
  #  t = Timer(30, timer_timeout)
  #  t.start()
  #  timing = True

  temp = sensor.readTempC()
  send_temp(temp)
  print('Temperature: {0:0.3F}*C'.format(temp) )
  print('Target: {0:0.3F}*C'.format(target_temp))
#  print('In range? ' + str(is_deviated(temp)))
  print('Heating? ' + str(heating))
  print('Cooling? ' + str(cooling))
  print('Temp Changed? ' + str(temp_changed))
  print('Operating? ' + str(operating))
  #deviated = is_deviated(temp)
  deviated = is_deviated_heat(temp)
  #if deviated is not False and temp_changed is False:
  if deviated is not False:
	if not operating: #Don't need to do it again if we are already doing something 
		operating = True #Make sure we know we need to turn off
		if deviated < 0: #Too hot cool down
			print "Cooling down"
			cooling = True
			#TODO Disabled for now #thread.start_new_thread(cool_down, ())
		else: #Too cold, heat up
			print "Heating up"
			heating = True
			thread.start_new_thread(heat_up, ())
  elif operating and (is_at_temp(temp) ): #We are in range now but still operating, turn things off
		
		print "Now in range, shutting down"
		thread.start_new_thread(turn_off, ())
		heating = False
		cooling = False
		temp_changed = False

  operating = heating or cooling
  #for clairity in the output
  print()
  print()
  time.sleep(5.0) #Time between each read

