from robomation import *

beagle = Beagle(0)

# 
def print_distance():
    distance = beagle.lidar_directions('front')

# if the front is reading less than 5 meters
def smooth_avoidance():
    arr = beagle.read(beagle.LIDAR_ARRAY)
    for i in range(46):
        if arr[i+1] and arr[359-i] and arr[i] != 65535 and arr[359-i] != 65535:
            if arr[i] >= 500 or arr[359-i] >= 500:
                if arr[i] >= arr[359-i]:
                    speed = 10 * ((180-i)/180) # proportional to the angle
                    beagle.change_wheel_speed('left', speed)
                else:
                    speed = 10 * ((180-i)/180)
                    beagle.change_wheel_speed('right', speed)
        else:
            print("distance is not valid")

#returns the angle error
def adjust():
    angle = beagle.gyroscope('x') # reads the angle of the current heading
    # if it is not going straight, adjust itself (later compare to the center of the tracked person, always puts the person
    # in the middle of the ka-mu-ra view)
    angle