import time, brickpi3    

BP = brickpi3.BrickPi3() 

#Using B

def go_straight(num_rotations):
	BP.set_motor_power(BP.PORT_A + BP.PORT_B + BP.PORT_C + BP.PORT_D, 0)
	BP.set_motor_position(BP.PORT_B, BP.get_motor_encoder(BP.PORT_B) + num_rotations*360)
	BP.set_motor_position(BP.PORT_C, BP.get_motor_encoder(BP.PORT_C) + num_rotations*360)
	
def rotate90():
	BP.set_motor_power(BP.PORT_A + BP.PORT_B + BP.PORT_C + BP.PORT_D, 0)
	BP.set_motor_position(BP.PORT_B, BP.get_motor_encoder(BP.PORT_B) + 244)
	BP.set_motor_position(BP.PORT_C, BP.get_motor_encoder(BP.PORT_C) - 244)

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
	go_straight(1)

except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
  	BP.reset_all() 