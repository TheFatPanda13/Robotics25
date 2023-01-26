import brickpi3, numpy, time
from control_test import Controller

BP = brickpi3.BrickPi3()

def drawSquare(controller):
    for i in range(4):
        controller.go_straight(0.20)
        time.sleep(2)
        rotate90(BP)
        time.sleep(2)

def rotate90(BP):
    BP.set_motor_limits(BP.PORT_B, power=30, dps=40)
    BP.set_motor_limits(BP.PORT_C, power=30, dps=40)
    BP.set_motor_position(BP.PORT_B, BP.get_motor_encoder(BP.PORT_B) + 244)
    BP.set_motor_position(BP.PORT_C, BP.get_motor_encoder(BP.PORT_C) - 244)


try:
    controller = Controller(BP)
    drawSquare(controller)


except KeyboardInterrupt:
    BP.reset_all()
