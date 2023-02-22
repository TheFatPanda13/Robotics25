import numpy as np
class Map:
    def __init__(self, edges):
        self.walls = edges
        self.scale = 10

    def add_wall(self, wall):
        self.walls.append(wall)

    def draw_walls(self):
        for wall in self.walls:
            x0, y0 = wall[0]
            x1, y1 = wall[1]
            print("drawLine:" + str((x0,y0,x1,y1)))

    def dist_to_wall(self, position, theta):
        theta = np.rad2deg(theta)
        ms = np.ones(len(self.walls))*1000000
        for i,wall in enumerate(self.walls):
            x0, y0 = wall[0]
            x1, y1 = wall[1]
            num = (y1-y0)*(x0-position[0]) - (x1-x0)*(y0-position[1])
            denom = (y1-y0)*np.cos(theta) - (x1-x0)*np.sin(theta)
            num2 = (y0-y1)*np.cos(theta) + (x1-x0)*np.sin(theta)
            denom2 = np.sqrt((y0-y1)**2 + (x1-x0)**2)
            beta = np.arccos(num2/denom2)
            beta = np.rad2deg(beta)
            if denom==0 or beta>55:
                ms[i] = 1000000
            else:
                ms[i] = num/denom
        valid = np.where(ms>0, ms, ms)
        return np.min(valid), ms

    def calculate_likelihood(self, position, theta, z, sigma):
        m = self.dist_to_wall(position, theta)
        likelihood = np.exp(-((z-m)**2)/sigma**2)
        return likelihood

    def is_in_map(self, position):
        x,y = position
        ans = True
        if x < 0 or y < 0:
            ans = False
        if x > 210:
            ans = False
        if x > 168 and y > 84:
            ans = False
        if y > 210:
            ans = False
        if y > 168 and x < 84:
            ans = False

        return ans


    
