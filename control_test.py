import time, brickpi3, numpy as np    

BP = brickpi3.BrickPi3()

class Controller():
    def __init__(self, BP, wheel_radius = 0.0255, wheelbase = 0.152, total_power = 25):
        self.BP = BP
        self.wheel_radius = wheel_radius
        self.wheelbase = wheelbase
        self.wheel_circ = 2 * np.pi * self.wheel_radius

        self.ports = [self.BP.PORT_B, self.BP.PORT_C]
        self.total_power = total_power

    def convert_distance_to_rotation(self, distance):
        print(distance, self.wheel_circ)
        return  360 * distance / self.wheel_circ

    def go_straight(self, distance, gain = 0.5):
        for port in self.ports:
            self.BP.offset_motor_encoder(port, self.BP.get_motor_encoder(port))

        start_time = time.time()
        positions = np.array([self.BP.get_motor_encoder(port) for port in self.ports])
        degrees_to_rotate = self.convert_distance_to_rotation(distance)
        print(degrees_to_rotate)
        while np.any(positions < degrees_to_rotate):
            time.sleep(0.01)
            print(positions)
            positions = np.array([self.BP.get_motor_encoder(port) for port in self.ports])
            update = gain * abs(positions[0] - positions[1])
            faster_motor, slower_motor = np.argmax(positions), np.argmin(positions)

            # print(update, self.total_power - update, self.total_power + update)
            self.BP.set_motor_power(self.ports[faster_motor], self.total_power - update)
            self.BP.set_motor_power(self.ports[slower_motor], self.total_power)

        print([self.BP.get_motor_encoder(port) for port in self.ports])
        self.BP.reset_all()

    def robot_angle_to_wheel_rotation(self, angle):
        dist = self.wheelbase * angle / 360 * np.pi 
        degrees = self.convert_distance_to_rotation(dist)
        return degrees * 0.808

    def turn_on_spot(self, angle, gain = 0.3):
        for port in self.ports:
            self.BP.offset_motor_encoder(port, self.BP.get_motor_encoder(port))
        self.total_power = 20
        start_time = time.time()
        positions = np.array([self.BP.get_motor_encoder(port) for port in self.ports])
        degrees_to_rotate = self.robot_angle_to_wheel_rotation(angle)
        print(degrees_to_rotate)
        while np.all(np.abs(positions) < degrees_to_rotate):
            #time.sleep(0.0001)
            print(positions)
            print([self.BP.get_motor_status(port) for port in self.ports])
            positions = np.array([self.BP.get_motor_encoder(port) for port in self.ports])
            #update = gain * (positions[0] +positions[1])
            update = 0
            print(update)
            # print(update, self.total_power - update, self.total_power + update)

            if update>0:
                self.BP.set_motor_power(self.ports[0], self.total_power - update)
                self.BP.set_motor_power(self.ports[1], -self.total_power - update)
            else:
                self.BP.set_motor_power(self.ports[0], self.total_power - update)
                self.BP.set_motor_power(self.ports[1], -self.total_power - update)

        print([self.BP.get_motor_encoder(port) for port in self.ports])
        print([np.abs(self.BP.get_motor_encoder(port)) - degrees_to_rotate for port in self.ports])
        self.BP.reset_all()
        self.total_power = 30

    def draw_square(self):
        try:
            for _ in range(4):
                controller.go_straight(0.355)
                time.sleep(2)
                controller.turn_on_spot(90)
                time.sleep(2)
        except KeyboardInterrupt:
            BP.reset_all()

try:
    controller = Controller(BP)
    controller.draw_square()
except KeyboardInterrupt: 
    BP.reset_all() 




