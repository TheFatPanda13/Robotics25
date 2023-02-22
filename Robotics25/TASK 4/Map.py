import numpy as np
class Map:
    def __init__(self, edges):
        self.walls = edges
        self.scale = 10

    def add_wall(self, wall):
        self.walls.append(wall)

    def draw_walls(self):
        map_inverter = lambda x: [[x[0][0], 210-x[0][1]], [x[1][0], 210-x[1][1]]]
        new_edges = [map_inverter(x) for x in self.walls]
        
        for wall in new_edges:
            x0, y0 = wall[0]
            x1, y1 = wall[1]
            print("drawLine:" + str((x0,y0,x1,y1)))

    def dist_to_wall(self, position, theta):
        theta = np.deg2rad(theta)
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
            if denom==0:
                ms[i] = 1000000
            else:
                ms[i] = num/denom
        #valid = np.where(ms>0, ms, ms)
        return ms

    def calculate_likelihood(self, position, theta, z, sigma, k=0.005):
        dists = self.dist_to_wall(position, theta)
        #print(f"dists:{dists}")
        valid_idxs = self.is_valid_intersection(dists, position, theta)
        valid_dists = dists[valid_idxs]
        #print(f"valid_dists: {valid_dists}")
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
                #print(f"Wall{i} gives distance {m}")
            else:
                x_int = position[0] + m*np.cos(theta)
                y_int = position[1] + m*np.sin(theta)
                
                if not self.is_point_between([x_int, y_int], self.walls[i]):
                    ans[i] = False
                        #print(f"Wall{i} gives distance {m} which does not intersect with wall")
        return ans

    def is_point_between(self, point, edge):
        x0, y0 = edge[0]
        x1, y1 = edge[1]
        ans = True
        eps=1
        if point[0]<min(x0,x1)-eps:
            ans = False
        if point[0]>max(x0,x1)+eps:
            ans = False
        if point[1] > max(y0,y1)+eps:
            ans = False
        if point[1] < min(y0,y1)-eps:
            ans = False
        return ans

    def draw_particles(self, particles):
        print("drawParticles:" + str(self.transform_particles(particles)))

#transform the particles (x,y) coordinates to suitable screen coordinates
    def transform_particles(self, particles):
        return [(x, 210 - y, theta) for (x,y,theta) in particles]



            



    
