from robomation import *
import func

beagle = Beagle(0)

accer = 100 # wheel speed is -100 to 100

lp_dist = 0
rp_dist = 0
distance = 0
# put setup code here, to run once:
def setup():
	beagle.lidar_power(True)


# put control code here, to run repeatedly:
def loop():
	beagle.set_wheel_speed('both', 50)
	global distance
	dist = beagle.lidar_directions('front')
	print(func.not_repeat_dist(dist, distance))

	# when front detects an obstacle, detects the smallest angle of opening, 
	# put distances in a list, where distance of angle 1, 359, 2, 358, 3, 357, ..., then get the earliest one that is greater than the front dist
	if dist <= 500:
		

	
        
setup()
while True:
	loop()
