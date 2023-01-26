import brickpi3, time, numpy
from control_test import Controller

BP = brickpi3.BrickPi3()

try:
    controller = Controller(BP)
    for distance in [5, 10, 15, 20, 25]:
        controller.go_straight(distance)
        time.sleep(30)
    controller.BP.reset_all()

except KeyboardInterrupt: 
    BP.reset_all()



