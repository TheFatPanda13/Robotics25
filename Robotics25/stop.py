import brickpi3

BP = brickpi3.BrickPi3()

BP.set_motor_power(BP.PORT_A + BP.PORT_B + BP.PORT_C + BP.PORT_D, 0)

BP.reset_all()
