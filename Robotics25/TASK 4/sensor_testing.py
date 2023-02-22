import time
import brickpi3
from Controller import Controller
from Map import Map
BP = brickpi3.BrickPi3()
BP.reset_all()
#BP.set_sensor_type(BP.PORT_2,BP.SENSOR_TYPE.NXT_ULTRASONIC)
edges = [[[0,0], [0,168]], [[0,168], [84, 168]], \
    [[84, 126], [84, 210]], [[84, 210], [168, 210]], \
         [[168, 210], [168, 84]], [[168, 84], [210, 84]], \
             [[210, 84], [210, 0]], [[210,0], [0,0]]]
env = Map(edges)
controller = Controller(BP, env)
"""
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
"""



it=10
while it>0:
    try:
        controller.get_sensor_2()
        it-=1
        BP.reset_all()
        controller.set_all()
        #time.sleep(0.02) 
    except KeyboardInterrupt:
        print("done")
        BP.reset_all()
    time.sleep(0.3)
    BP.set_sensor_type(BP.PORT_2,BP.SENSOR_TYPE.NONE)
