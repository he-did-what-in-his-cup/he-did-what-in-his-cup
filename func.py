from robomation import *

# beagle = Beagle(0) # comment out when running

# 
def not_repeat_dist(current_distance, distance):
    if distance != current_distance:
        distance = current_distance
        return current_distance
    else:
        return

#returns angle and distance of that angle
def smooth_avoidance(beagle):
    arr = beagle.read(beagle.LIDAR_ARRAY)
    for i in range(1,60):
        if arr[i] and arr[i] != 65535:
            print(arr[i])
            # returns the first angle that is greater than 500
            if arr[i] >= 500:
                print("distance from angle ", i, "is greater than 500 mm with distance ", arr[i])
                beagle.turn_degree('right', i)
                print("turned to degree ", i)
                break
                # return i, arr[i]
        else:
            print("distance error for angle ", i)

#returns the angle error
def adjust():
    angle = beagle.gyroscope('x') # reads the angle of the current heading
    # if it is not going straight, adjust itself (later compare to the center of the tracked person, always puts the person
    # in the middle of the ka-mu-ra view)
    angle    