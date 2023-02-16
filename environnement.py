import numpy as np
class Environnement :
    def __init__(self, edges,max_dim):
        self.edges=edges
        self.max_dim=max_dim
    def compute_edge_intersetion(self,edge,position,orientation):
       
        x1,y1 = edge[0]
        x2,y2 = edge[1]
        x3,y3 = position
        
        x4,y4 = [np.cos(orientation)*self.max_dim*2+position[0],np.sin(orientation)*2*self.max_dim+position[1]]
        denom = (y4-y3)*(x2-x1) - (x4-x3)*(y2-y1)
        if denom == 0: # parallel
          
            return None
        ua = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)) / denom
        
        if ua < 0 or ua > 1: # out of range
            return None
        ub = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3)) / denom
        
        if ub < 0 or ub > 1: # out of range
            return None
        x = x1 + ua * (x2-x1)
        y = y1 + ua * (y2-y1)
        return [x,y]
    def compute_distance_to_wall(self,position,orientation):
        dist=[]
        for ed in self.edges:
            dist.append(self.compute_edge_intersetion(ed,position,orientation))
        
        dist=[i for i in dist if i]
        dist=np.array(dist)
        print(dist)
        dist-=position
        
        return min([np.linalg.norm(i) for i in dist])
    
    



        

