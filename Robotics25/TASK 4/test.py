import numpy as np
import brickpi3
from Map import Map
from Controller import Controller

BP = brickpi3.BrickPi3()
edges = [[[0,0], [0,168]], [[0,168], [84, 168]], \
    [[84, 126], [84, 210]], [[84, 210], [168, 210]], \
         [[168, 210], [168, 84]], [[168, 84], [210, 84]], \
             [[210, 84], [210, 0]], [[210,0], [0,0]]]


env = Map(edges)
env.draw_walls()

BP.set_sensor_type(BP.PORT_2,BP.SENSOR_TYPE.NXT_ULTRASONIC)
controller = Controller(BP,env)
waypoints2=[[84,0],[120,0]]
waypoints = [[180,30], [180,54], [138,54], [138,168], [114,168], [114,84], [84,84], [84,30]]
try:
    for waypoint in waypoints:
        controller.navigate_to_waypoint(*waypoint)
        env.draw_particles(controller.particles[:,:3])
        print(f"Angle particles: {controller.particles[:,2]}")
        print(f"Angle robot: {controller.pos[2]}")
    #controller.navigate_to_waypoint(60,0)
    #controller.navigate_to_waypoint(80,0)  
     
    #controller.turn_on_spot(55)
    #controller.draw_square()
    #print(np.var(controller.particles[:,:-1], axis=0))

except KeyboardInterrupt:
    BP.reset_all()