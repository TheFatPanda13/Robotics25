import time, brickpi3    

class Controller():
	def __init__(wheel_radius, wheelbase, total_power):
		BP = brickpi3.BrickPi3() 

		self.wheel_radius = wheel_radius
		self.wheelbase = wheelbase
		self.wheel_circ = 2 * np.pi * self.wheel_radius
		
		self.ports = [BP.PORT_B, BP.PORT_C]
		self.total_power

	def convert_distance_to_rotation(self, distance):
		return = 360 * distance / self.wheel_circ

	def go_straight(self, distance, gain):
		for port in ports:
			BP.offset_motor_encoder(BP.port, BP.get_motor_encoder(port))

		start_time = time.time()
		while time.time() - start_time <= 10:
			time.sleep(0.05)
			positions = np.array([BP.get_motor_encoder(port) for port in ports])

			update = gain * abs(positions[0] - positions[1])
			faster_motor, slower_motor = np.argmax(positions), np.argmin(positions)

			BP.set_motor_power(ports[farthest], self.total_power - update)
			BP.set_motor_power(ports[slower_motor], self.total_power + update)

try:
	controller = Contoller(1, 1, 20)
	controller.go_straight(1, 10)
except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
  	BP.reset_all() 



