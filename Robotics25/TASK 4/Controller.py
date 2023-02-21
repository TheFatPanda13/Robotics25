import time, brickpi3, random, Display, numpy as np
from environnement import Environnement

class Controller():
    def __init__(self, BP = None,environnement=None wheel_radius = 0.0255, wheelbase = 0.152, total_power = 20, set_length = 100):
        self.BP = BP
        
        self.wheel_radius = wheel_radius
        self.wheelbase = wheelbase
        self.wheel_circ = 2 * np.pi * self.wheel_radius

        self.ports = [self.BP.PORT_B, self.BP.PORT_C]
        self.total_power = total_power
        self.environment=environnement
        particle = np.array([0,0,0,1/set_length])
        self.particles = np.tile(particle, (100,1)) #initialise particle set shape 100, 4
        self.set_length = set_length
        self.pos = np.array([0,0,0])
        
        self.BP.set_motor_limits(BP.PORT_B, dps = 300)
        self.BP.set_motor_limits(BP.PORT_C, dps = 300)
        BP.set_sensor_type(BP.PORT_1,BP.SENSOR_TYPE.NXT_ULTRASOSONIC)
    def get_sensor_input(self):
        try :
            value=self.BP.get_sensor(BP.PORT_1)
            return value
        except brickpi3.SensorError as error:
            print(error)
        return 255


    # distance is in meters
    def convert_distance_to_rotation(self, distance):
        return distance * 20.5

    def go_straight(self, distance, gain = 0.5):
        for port in self.ports:
            self.BP.offset_motor_encoder(port, self.BP.get_motor_encoder(port))

        #positions = np.array([self.BP.get_motor_encoder(port) for port in self.ports])


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
        
        self.update_particles_straight(distance)
        sensor_input=self.get_sensor_input()
        self.update_weight_particles(sensor_input,self.environment,sigma=0.5)
        self.resampling()

    def robot_angle_to_wheel_rotation(self, angle):
        dist = self.wheelbase * angle / 360 * np.pi 
        degrees = self.convert_distance_to_rotation(dist) * 100
        return 0.88 * degrees

    def turn_on_spot(self, angle, gain = 0.3):

        for port in self.ports:
            self.BP.offset_motor_encoder(port, self.BP.get_motor_encoder(port))

        start_time = time.time()
        positions = np.array([self.BP.get_motor_encoder(port) for port in self.ports])
        degrees_to_rotate = self.robot_angle_to_wheel_rotation(angle)
        while np.all(np.abs(positions) < degrees_to_rotate):
            #time.sleep(0.0001)
            #print(positions)
            #print([self.BP.get_motor_status(port) for port in self.ports])
            positions = np.array([self.BP.get_motor_encoder(port) for port in self.ports])
            update = gain * (positions[0] +positions[1])
            # print(update, self.total_power - update, self.total_power + update)

            if update>0:
                self.BP.set_motor_power(self.ports[0], self.total_power - update)
                self.BP.set_motor_power(self.ports[1], -self.total_power - update)
            else:
                self.BP.set_motor_power(self.ports[0], self.total_power - update)
                self.BP.set_motor_power(self.ports[1], -self.total_power - update)

        print([self.BP.get_motor_encoder(port) for port in self.ports])
        print([np.abs(self.BP.get_motor_encoder(port)) - degrees_to_rotate for port in self.ports])
        self.BP.set_motor_power(self.ports[0], 0)
        self.BP.set_motor_power(self.ports[1], 0)
        sensor_input=self.get_sensor_input()
        self.update_particles_rotate(angle)
        self.update_weight_particles(sensor_input,self.environment,sigma=0.5)
        self.resampling()

    def update_particles_straight(self, delta):
        angles = self.particles[:,-2] #grab the angles of each particle
        
        update = np.array([[(delta + random.gauss(0, 0.14)) * np.cos(np.deg2rad(angles[i])), 
                            (delta + random.gauss(0, 0.14)) * np.sin(np.deg2rad(angles[i])), 
                            random.gauss(0, 1), 
                            0] for i in range(self.set_length)])

        self.particles += update
        
        Display.draw_particles(self.particles[:,:-1])
        
        self.pos = np.array(np.mean(self.particles[:,:-1], axis=0))
    
    def update_particles_rotate(self, theta):
        update = np.array([[0, 0, theta + random.gauss(0, 0.05), 0] for i in range(self.set_length)])
        
        self.particles += update
        
        self.pos = np.array(np.mean(self.particles[:,:-1], axis=0))
    def update_weight_particles(self,sensor_input,environment,sigma):
        total_norm=0
        for particle in self.particles:
            distance=environment.compute_distance_to_wall(particle[:1],particle[2])
            error=distance-sensor_input
            likelihood=np.exp(-(error/sigma)**2)
            total_norm+=likelihood
            particle[3]*=likelihood
        self.particles[3]/=total_norm
    def resampling(self):
        weights=self.particles[3]
        self.particles=np=random.choice(self.particles, size=len(self.particles), replace=True, p=weights)


    
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
        print(f"I think I'm at {self.pos}")
        print(f"navigating to {wx}, {wy}")

        dx = wx - self.pos[0]
        dy = wy - self.pos[1]
        alpha = np.rad2deg(np.arctan2(dy, dx))

        theta = self.pos[2]
                
        print(f"dy: {dy}, dx: {dx}, alpha: {alpha}, theta:{theta}")
        print(f"angle to rotate is: {np.rad2deg(alpha - theta)}")
        self.turn_on_spot((alpha - theta) % 360)
        time.sleep(3)
        self.go_straight(np.sqrt(np.square(dx) + np.square(dy)))
        time.sleep(5)
        