import time
import brickpi3
import Controller
BP = brickpi3.BrickPi3()
controller = Controller.Controller(BP)
BP.set_sensor_type(BP.PORT_2,BP.SENSOR_TYPE.NXT_ULTRASONIC)

try:
    while True:
        try:
            value = BP.get_sensor(BP.PORT_2)
            print(value)
            BP.reset_all()
            print(value)                       # print the distance in CM
        except brickpi3.SensorError as error:
            print(error)
        time.sleep(0.02)
    
        #time.sleep(0.02) 
except KeyboardInterrupt:
    BP.reset_all()