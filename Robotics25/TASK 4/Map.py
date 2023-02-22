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
        #valid = np.where(ms>0, ms, ms)
        return ms

    def calculate_likelihood(self, position, theta, z, sigma, k=0.05):
        dists = self.dist_to_wall(position, theta)
        valid_idxs = self.is_valid_intersection(dists, position, theta)
        valid_dists = dists[valid_idxs]
        m = np.min(valid_dists)
        likelihood = np.exp(-((z-m)**2)/sigma**2) + k
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

    def is_valid_intersection(self, dists, position, theta):
        theta = np.deg2rad(theta)
        ans = np.ones(len(self.walls), dtype=bool)
        for i,m in enumerate(dists):
            if m<0:
                ans[i] = False
            else:
                x_int = position[0] + m*np.cos(theta)
                y_int = position[1] + m*np.sin(theta)
                if not self.is_in_map([x_int, y_int]):
                    ans[i] = False
                else:
                    if not self.is_point_between([position[0], position[1]], self.walls[i]):
                        ans[i] = False
        return ans

    def is_point_between(self, point, edge):
        x0, y0 = edge[0]
        x1, y1 = edge[1]
        ans = True
        if point[0]<min(x0,x1):
            ans = False
        if point[0]>max(x0,x1):
            ans = False
        if point[1] > max(y0,y1):
            ans = False
        if point[1] < min(y0,y1):
            ans = False
        return ans

    def draw_particles(self, particles):
        print("drawParticles:" + str(self.transform_particles(particles)))

#transform the particles (x,y) coordinates to suitable screen coordinates
    def transform_particles(self, particles):
        return [(x, 210 - y, theta) for (x,y,theta) in particles]



            



    
