from robomation import *
import func

beagle = Beagle(0)

accer = 100 # wheel speed is -100 to 100

distance = 0
beagle.lidar_power(True)
Utils.wait(2) # for the motor to spin up the lidar, the lidar updates around every 0.2 seconds 


while True:
	beagle.set_wheel_speed('both', 5)
	dist = round(beagle.lidar_value(0))
	print(func.not_repeat_dist(dist, distance))

	# when front detects an obstacle, detects the smallest angle of opening, 
	# put distances in a list, where distance of angle 1, 359, 2, 358, 3, 357, ..., then get the earliest one that is greater than the front dist
	if dist <= 500:
		func.smooth_avoidance(beagle)
		break
