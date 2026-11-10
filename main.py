from robomation import *

beagle = Beagle(0)

past_distance = 0
# put setup code here, to run once:
def setup():
	beagle.lidar_power(True)


# put control code here, to run repeatedly:
def loop():
	global past_distance
	distance = beagle.lidar_directions('front') # in millimeters
	if distance != past_distance:
		print(distance)
		past_distance = distance

        
setup()
past_distance = 0
while True:
	beagle.gyroscope('x')
	loop()

