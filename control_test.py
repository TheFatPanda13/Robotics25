import time, brickpi3, numpy as np    

BP = brickpi3.BrickPi3()

class Controller():
	    def __init__(self, BP, wheel_radius = 0.034, wheelbase = 0.035, total_power = 20):
		    	self.BP = BP
		        self.wheel_radius = wheel_radius
		        self.wheelbase = wheelbase
		        self.wheel_circ = 2 * np.pi * self.wheel_radius
		        
		        self.ports = [self.BP.PORT_B, self.BP.PORT_C]
		        self.total_power = total_power

	    def convert_distance_to_rotation(self, distance):
	        	return  360 * distance / self.wheel_circ

	    def go_straight(self, distance, gain = 0.5):
		        for port in self.ports:
		            	self.BP.offset_motor_encoder(port, self.BP.get_motor_encoder(port))

				        start_time = time.time()
				        positions = np.array([self.BP.get_motor_encoder(port) for port in self.ports])
				        degrees_to_rotate = self.convert_distance_to_rotation(distance)

		        while np.all(positions) < degrees_to_rotate:
			            time.sleep(0.05)
			            positions = np.array([self.BP.get_motor_encoder(port) for port in self.ports])
			            update = gain * abs(positions[0] - positions[1])
			            faster_motor, slower_motor = np.argmax(positions), np.argmin(positions)

			            # print(update, self.total_power - update, self.total_power + update)
			            self.BP.set_motor_power(self.ports[faster_motor], self.total_power - update)
			            self.BP.set_motor_power(self.ports[slower_motor], self.total_power + update)

		        print([self.BP.get_motor_encoder(port) for port in self.ports])
		        
try:
	    controller = Controller(BP)
	    controller.go_straight(25)
	    contoller.BP.reset_all()

except KeyboardInterrupt: 
    	BP.reset_all() 





