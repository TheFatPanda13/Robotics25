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

def rotate90(value, duration):
	BP.set_motor_power(BP.PORT_A + BP.PORT_B + BP.PORT_C + BP.PORT_D, 0)
	BP.set_motor_power(BP.PORT_B, value)
	BP.set_motor_power(BP.PORT_C, -value)
	time.sleep(duration)
	BP.set_motor_power(BP.PORT_B, BP.PORT_C, 0)

def drawSquare():
    for i in range(4):
        go_straight()
        rotate90()
    rotate90() #to face the correct direction again

def drawX():
	for i in range(4):
		go_straight(5,1)
		go_straight(-5,1)
		rotate90()
		
 #to do calibrate and find optimal values for go_straight and rotate90

try:
	go_straight(10, 5)
	rotate90(10,2)
	go_straight(10,5)

except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
  	BP.reset_all() 