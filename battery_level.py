import time, sys
import ps_drone

# Start using drone, connects to drone and starts subprocesses
drone = ps_drone.Drone()
drone.startup()

# Sets drone's status to good (LEDs turn green when red)
drone.reset()

# Waits until drone has done its reset, then display battery information
while (drone.getBattery()[0] == -1):
    time.sleep(0.1)
print 'Battery at ' + str(drone.getBattery()[0]) + '% - ' + str(drone.getBattery()[1])