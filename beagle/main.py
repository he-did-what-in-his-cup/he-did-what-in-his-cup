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
	global distance
	dist = beagle.lidar_directions('front')
	print(func.not_repeat_dist(dist, distance))
	# beagle.move_distance(10, 'cm', False)
	if dist <= 500:
		func.in_place_turn(beagle)
	
        
setup()
while True:
	loop()

