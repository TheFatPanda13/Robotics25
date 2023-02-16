import Controller, brickpi3, time, numpy as np

BP = brickpi3.BrickPi3()

controller = Controller.Controller(BP)

try:
    controller.navigate_to_waypoint(20,20)
    controller.navigate_to_waypoint(20,-20)
    controller.navigate_to_waypoint(40,0)
    controller.navigate_to_waypoint(0,0)    
    #controller.turn_on_spot(55)
    #controller.draw_square()
    print(np.var(controller.particles[:,:-1], axis=0))

except KeyboardInterrupt:
    BP.reset_all()
