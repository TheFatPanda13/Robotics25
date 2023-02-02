import time, brickpi3

BP = brickpi3.BrickPi3()

BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.TOUCH)
BP.set_sensor_type(BP.PORT_2, BP.SENSOR_TYPE.TOUCH)

crashed = False

while not crashed:
    BP.set_motor_power(BP.PORT_B + BP.PORT_C, 20)
    crashed = BP.get_sensor(BP.PORT_1) or BP.get_sensor(BP.PORT_2)

print("We crashed!")

BP.set_motor_power(BP.PORT_B + BP.PORT_C, -20)
time.sleep(3)
BP.reset_all()

