import brickpi3, time, numpy
from control_test import Controller

BP = brickpi3.BrickPi3()

try:
    controller = Controller(BP)
    for distance in [35.5]:
        distance = distance / 100 
        controller.go_straight(distance= distance)
        controller.BP.reset_all()
        time.sleep(10)

except KeyboardInterrupt: 
    BP.reset_all()


