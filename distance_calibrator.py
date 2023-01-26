import brickpi3, time, numpy
from control_test import Controller

BP = brickpi3.BrickPi3()

try:
    controller = Controller(BP)
    for distance in [5, 10, 15, 20, 25]:
        distance = distance / 100 
        controller.go_straight(distance= distance)
        controller.BP.reset_all()
        time.sleep(30)

except KeyboardInterrupt: 
    BP.reset_all()


