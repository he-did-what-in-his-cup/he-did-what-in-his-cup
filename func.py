from robomation import *

beagle = Beagle(0) # comment out when running

# 
def not_repeat_dist(current_distance, distance):
    if distance != current_distance:
        distance = current_distance
        return current_distance
    else:
        return

# if front detect something, then go around an obstacle
# if the sensor detects something that is less than half a meter infront of the robot, then scans left front and right front, then picks the lower value, 
# then goes in that direction to go around the obstacle

def in_place_turn(beagle):
    # take the minimum of the left or the right front of the robot, then choose the closer one because it would be easier to get to
    lf = beagle.lidar_directions('left_front')
    rf = beagle.lidar_directions('right_front')
    front = beagle.lidar_value(0)

    if lf <= rf:
        # turn until the front is reading greater than 1 meter
        while front <= 1000:
            beagle.turn_degree('left', 10)
            front = beagle.lidar_value(0)
            print("distance in the front: ", front)
    else:
        while front <= 1000:
            beagle.turn_degree('right', 10)
            front = beagle.lidar_value(0)
            print("distance in the front: ", front)
    print("distance is greater than 1 meter: ", front)

# input: beagle
def obs_avoid():
    beagle.set_wheel_speed

def get_dists():
    r_dists = []
    l_dists = []# if the front is reading less than 5 meters
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