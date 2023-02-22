import numpy as np
import brickpi3
from Map import Map
from Controller import Controller

BP = brickpi3.BrickPi3()
edges = [[[0,0], [0,168]], [[0,168], [84, 168]], \
    [[84, 126], [84, 210]], [[84, 210], [168, 210]], \
         [[168, 210], [168, 84]], [[168, 84], [210, 84]], \
             [[210, 84], [210, 0]], [[210,0], [0,0]]]

map_inverter = lambda x: [[x[0][0], 210-x[0][1]], [x[1][0], 210-x[1][1]]]
new_edges = [map_inverter(x) for x in edges]
env = Map(new_edges)
env.draw_walls()

BP.set_sensor_type(BP.PORT_1,BP.SENSOR_TYPE.NXT_ULTRASONIC)
controller = Controller.Controller(BP,env)

try:
    controller.navigate_to_waypoint(100,0)
    controller.navigate_to_waypoint(40,0)
    controller.navigate_to_waypoint(60,0)
    controller.navigate_to_waypoint(80,0)  
    env.draw_particles(controller.particles)  
    #controller.turn_on_spot(55)
    #controller.draw_square()
    #print(np.var(controller.particles[:,:-1], axis=0))

except KeyboardInterrupt:
    BP.reset_all()