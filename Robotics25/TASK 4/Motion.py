import Controller, brickpi3, time, numpy as np
from environnement import Environnement
BP = brickpi3.BrickPi3()
env=Environnement([[[100,-100],[100,100]]],200)
controller = Controller.Controller(BP,env)

try:
    controller.navigate_to_waypoint(20,0)
    controller.navigate_to_waypoint(40,0)
    controller.navigate_to_waypoint(60,0)
    controller.navigate_to_waypoint(80,0)    
    #controller.turn_on_spot(55)
    #controller.draw_square()
    print(np.var(controller.particles[:,:-1], axis=0))

except KeyboardInterrupt:
    BP.reset_all()
