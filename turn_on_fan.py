##############################
# This is for backup in case
# Something happens.
# If the heat is on but the fan
# isn't running or they both turn off simultaneously
#Running this will just turn on the fan to make the furnace not wear out

import automationhat
import time

automationhat.output.one.on()
time.sleep(30.0)
