import numpy as np
import brickpi3
from Map import Map
from Controller import Controller

BP = brickpi3.BrickPi3()
edges = [[[0,0], [0,168]], [[0,168], [84, 168]], \
    [[84, 126], [84, 210]], [[84, 210], [168, 210]], \
         [[168, 210], [168, 84]], [[168, 84], [210, 84]], \
             [[210, 84], [210, 0]]]
env = Map(edges)
env.draw_walls()