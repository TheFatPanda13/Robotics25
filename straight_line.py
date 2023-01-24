import time, brickpi3    

BP = brickpi3.BrickPi3() 

#Using B

def go_straight(value, duration):
		start_time = time.time()
  	BP.set_motor_power(BP.PORT_A + BP.PORT_B + BP.PORT_C + BP.PORT_D, speed)
		while time.time() - start_time <= duration:
				(status, power, degrees, velocity) = BP.get_motor_status(BP.PORT_B)
	  		print(f"degrees: {degrees}, velocity: {velocity}")
		BP.set_motor_power(BP.PORT_A + BP.PORT_B + BP.PORT_C + BP.PORT_D, 0)

try:
		go_straight(10, 5)



except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
  	BP.reset_all() 