import time, brickpi3, random, numpy as np
from Map import Map

class Controller():
    def __init__(self, BP = None,environnement=None, wheel_radius = 0.0255, wheelbase = 0.152, total_power = 20, set_length = 200):
        self.BP = BP
        
        self.wheel_radius = wheel_radius
        self.wheelbase = wheelbase
        self.wheel_circ = 2 * np.pi * self.wheel_radius

        self.ports = [self.BP.PORT_B, self.BP.PORT_C]
        self.total_power = total_power
        self.environment=environnement
        particle = np.array([84,30,0,1/set_length])
        self.particles = np.tile(particle, (set_length,1)) #initialise particle set shape 100, 4
        self.set_length = set_length
        self.pos = np.array([84,30,0])
        self.sigma = 5
        self.sensor_value=255
        self.sleep_time=1
        
        self.BP.set_motor_limits(BP.PORT_B, dps = 200)
        self.BP.set_motor_limits(BP.PORT_C, dps = 200)
        self.BP.set_sensor_type(self.BP.PORT_1,self.BP.SENSOR_TYPE.NXT_ULTRASONIC)
      
    def mean_angle(self,angle_array):
        mean_cos=np.mean([np.cos(np.deg2rad(i)) for i in angle_array])
        mean_sin=np.mean([np.sin(np.deg2rad(i)) for i in angle_array])
        angle_deg = np.rad2deg(np.arctan2(mean_sin, mean_cos))
        return angle_deg
    
    def get_sensor_input(self):
        try:
            bool = True
            while bool:
                try:
                    value = self.BP.get_sensor(self.BP.PORT_1)
                    if value :
                        self.sensor_value=value
                        print(f"Sensor 1: {self.sensor_value}")
                        bool=False
                except brickpi3.SensorError as error:
                    print(error)
        
                time.sleep(0.02)  # delay for 0.02 seconds (20ms) to reduce the Raspberry Pi CPU load.

        except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
            self.BP.reset_all()  


    def set_all(self):
        self.BP.set_motor_limits(self.BP.PORT_B, dps = 200)
        self.BP.set_motor_limits(self.BP.PORT_C, dps = 200)
        self.BP.set_sensor_type(self.BP.PORT_1,self.BP.SENSOR_TYPE.NXT_ULTRASONIC)
        
    # distance is in meters
    def convert_distance_to_rotation(self, distance):
        return distance * 26

    def go_straight(self, distance, gain = 0.5):
        for port in self.ports:
            self.BP.offset_motor_encoder(port, self.BP.get_motor_encoder(port))

        #positions = np.array([self.BP.get_motor_encoder(port) for port in self.ports])
        self.BP.set_motor_limits(self.ports[0], dps=200)
        self.BP.set_motor_limits(self.ports[1], dps=200)

        self.BP.set_motor_position(self.BP.PORT_B, self.convert_distance_to_rotation(distance))
        self.BP.set_motor_position(self.BP.PORT_C, self.convert_distance_to_rotation(distance))
        """
        print(degrees_to_rotate)
        while np.all(positions < degrees_to_rotate):
            time.sleep(0.01)
            print(positions)
            positions = np.array([self.BP.get_motor_encoder(port) for port in self.ports])
            update = gain * abs(positions[0] - positions[1])
            faster_motor, slower_motor = np.argmax(positions), np.argmin(positions)

            # print(update, self.total_power - update, self.total_power + update)
            self.BP.set_motor_power(self.ports[faster_motor], self.total_power - update)
            self.BP.set_motor_power(self.ports[slower_motor], self.total_power + update)

        print([self.BP.get_motor_encoder(port) for port in self.ports])
        """
        #self.BP.reset_all()
        time.sleep(self.sleep_time)
        self.update_particles_straight(distance)
        #self.get_sensor_input()
        self.get_sensor_input()
        sensor_input=self.sensor_value
        time.sleep(self.sleep_time)
        self.BP.reset_all()
        time.sleep(self.sleep_time)
        self.set_all()
        time.sleep(self.sleep_time)
        self.update_weight_particles(sensor_input,self.environment,sigma=self.sigma)
        self.resampling()
        self.pos=np.array([np.mean(self.particles[:,0]), \
                           np.mean(self.particles[:,1]),self.mean_angle(self.particles[:,2])])
       

    def robot_angle_to_wheel_rotation(self, angle):
        dist = self.wheelbase * angle / 360 * np.pi 
        degrees = self.convert_distance_to_rotation(dist) * 100
        return 0.70 * degrees

    def turn_on_spot(self, angle, gain = 0.3):
        power=np.sign(angle)*self.total_power
        for port in self.ports:
            self.BP.offset_motor_encoder(port, self.BP.get_motor_encoder(port))

        start_time = time.time()
        positions = np.array([self.BP.get_motor_encoder(port) for port in self.ports])
        degrees_to_rotate = self.robot_angle_to_wheel_rotation(angle)
        while np.all(np.abs(positions) < np.abs(degrees_to_rotate)):
            #time.sleep(0.0001)
            #print(positions)
            #print([self.BP.get_motor_status(port) for port in self.ports])
            positions = np.array([self.BP.get_motor_encoder(port) for port in self.ports])
            update = gain * (positions[0] +positions[1])
            # print(update, self.total_power - update, self.total_power + update)

            if update>0:
                self.BP.set_motor_power(self.ports[0], power - update)
                self.BP.set_motor_power(self.ports[1], -power - update)
            else:
                self.BP.set_motor_power(self.ports[0], power - update)
                self.BP.set_motor_power(self.ports[1], -power - update)

        #print([self.BP.get_motor_encoder(port) for port in self.ports])
        #print([np.abs(self.BP.get_motor_encoder(port)) - degrees_to_rotate for port in self.ports])
        self.BP.set_motor_power(self.ports[0], 0)
        self.BP.set_motor_power(self.ports[1], 0)
        self.get_sensor_input()
        sensor_input=self.sensor_value
        self.BP.reset_all()
        #time.sleep(0.2)
        self.set_all()
        time.sleep(0.2)
        self.update_particles_rotate(angle)
        self.update_weight_particles(sensor_input,self.environment,sigma=self.sigma)
        self.resampling()
        self.pos=np.array([np.mean(self.particles[:,0]), \
                           np.mean(self.particles[:,1]),self.mean_angle(self.particles[:,2])])
                           
       

    def update_particles_straight(self, delta):
        angles = self.particles[:,-2] #grab the angles of each particle+
        # 0.14, 0.1 old std values
        
        update = np.array([[(delta + random.gauss(0, 0.2)) * np.cos(np.deg2rad(angles[i])), 
                            (delta + random.gauss(0, 0.2)) * np.sin(np.deg2rad(angles[i])), 
                            random.gauss(0, 1), 
                            0] for i in range(self.set_length)])

        self.particles += update
        
        self.environment.draw_particles(self.particles[:,:-1])
        
        
    
    def update_particles_rotate(self, theta):
        update = np.array([[0, 0, theta + random.gauss(0, 0.05), 0] for i in range(self.set_length)])
        
        self.particles += update
        
        

    def update_weight_particles(self,sensor_input,environment,sigma):
        for particle in self.particles:
            #distance=environment.compute_distance_to_wall(particle[:2],particle[2])
            #error=distance-sensor_input
            #print(f"Error {error}, distance: {distance}")
            #likelihood=np.exp(-(error/sigma)**2)
            #print(f"likelihood {likelihood}")
            likelihood = environment.calculate_likelihood(particle[:2], particle[3], sensor_input, self.sigma)

            particle[3]*=likelihood
        self.particles[:, 3] = self.particles[:,3]/np.sum(self.particles[:,3])

    def resampling(self):
        weights=self.particles[:,3]
        #print(weights)
        idxs=np.random.choice(np.arange(0, len(self.particles)), size=len(self.particles), replace=True, p=weights)
        self.particles = self.particles[idxs]
        self.particles[:,3] = 1/len(self.particles)


    
    def draw_square(self):
        for _ in range(4):
            for _ in range(4):
                self.go_straight(10)
                time.sleep(2)
            self.turn_on_spot(90)
            time.sleep(2)
    
    def draw_square_og(self):
        for _ in range(4):
            self.go_straight(40)
            time.sleep(3)
            self.turn_on_spot(90)
            time.sleep(0.5)
    
    def navigate_to_waypoint(self, wx, wy):
        #print(f"I think I'm at {self.pos}")
        #print(f"navigating to {wx}, {wy}")
        dx = wx - self.pos[0]
        dy = wy - self.pos[1]
        dist=np.sqrt(np.square(dx) + np.square(dy))
        if (dist >20):

            
            alpha = np.rad2deg(np.arctan2(dy, dx))
           
            theta = self.pos[2]

            #print(f"dy: {dy}, dx: {dx}, alpha: {alpha}, theta:{theta}")
            #print(f"angle to rotate is: {np.rad2deg(alpha - theta)}")
            angle_to_rotate=(alpha - theta) % 360
            print(f"Angle to rotqte:{angle_to_rotate}")
            if angle_to_rotate<-180:
                angle_to_rotate+=360
            elif angle_to_rotate>180:
                angle_to_rotate-=360
            print(f"Alpha:{alpha}")
            print(f"Theta:{theta}")
                
            print(f"Angle to rotqte:{angle_to_rotate}")
            
            self.turn_on_spot(angle_to_rotate)
            time.sleep(2)
            self.go_straight(20)
            time.sleep(2)
            self.navigate_to_waypoint(wx, wy)
        else:
            
            alpha = np.rad2deg(np.arctan2(dy, dx))
            print(f"Alpha:{alpha}")
            theta = self.pos[2]

            #print(f"dy: {dy}, dx: {dx}, alpha: {alpha}, theta:{theta}")
            #print(f"angle to rotate is: {np.rad2deg(alpha - theta)}")
            angle_to_rotate=(alpha - theta) % 360
            
            if angle_to_rotate<-180:
                angle_to_rotate+=360
            elif angle_to_rotate>180:
                angle_to_rotate-=360
            print(f"Angle to rotqte:{angle_to_rotate}")
                
                
            self.turn_on_spot(angle_to_rotate)
            time.sleep(2)
            self.go_straight(dist)
            time.sleep(2)
            
        