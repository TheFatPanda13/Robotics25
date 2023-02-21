import time

BP = brickpi3.BrickPi3()

BP.set_sensor_type(BP.PORT_1,BP.SENSOR_TYPE.NXT_ULTRASONIC)

def get_sensor_data():
    try:
        value = BP.get_sensor(BP.PORT_1)
        print(value)                         # print the distance in CM
    except brickpi3.SensorError as error:
        print(error)
        
    time.sleep(0.02) 

for _ in range(100):
    time.sleep(0.02)
    print(get_sensor_data())