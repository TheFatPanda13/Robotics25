import brickpi3, numpy
from control_test import Controller

BP = brickpi3.BrickPi3()

def drawSquare(controller):
    for i in range(4):
        controller.go_straight(20)
        rotate90(BP)

def rotate90(BP):
	BP.set_motor_position(BP.PORT_B, BP.get_motor_encoder(BP.PORT_B) + 244)
	BP.set_motor_position(BP.PORT_C, BP.get_motor_encoder(BP.PORT_C) - 244)


try:
    controller = Controller(BP)
    drawSquare(controller)


except KeyboardInterrupt:
    BP.reset_all()
