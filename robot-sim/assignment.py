from __future__ import print_function

import time
from sr.robot import *

R = Robot()


a_th = 2.0
""" float: Threshold for the control of the orientation"""

d_th = 0.4
""" float: Threshold for the control of the linear distance"""


def drive(speed, seconds):
    """
    Function for setting a linear velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)  #continue its way 
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)   #continue its way 
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def find():

	"""
	Function for detecting tokens and storing their information
	"""
   
    Golden_tokens_initial = [] #create an empty list to store marker_data of all tokens

    dist = 100
    for token in R.see():
        token_type = token.info.marker_type
        dist = token.dist
        rot_y = token.rot_y
        marker_data = [dist, rot_y]  # Create a list for each token

        Golden_tokens_initial.append(marker_data)  #adding marker_data of each token to 'Golden_tokens_initial' list

    Golden_tokens = sorted(Golden_tokens_initial, key=lambda x: x[0])  # Sort the list of Golden_tokens_initial according to dist of tokens
    if Golden_tokens[0][0] < 100:
        return Golden_tokens
    else:
        return None 


def grab_and_release(t_1,t_2,t_3):

	"""
	Function to guide the robot toward the nearest token, grab it, move toward the center, and release the token
	"""
   
	while True:
	    Golden_tokens = find()
	    print(Golden_tokens)

	    if Golden_tokens == None:
		print("I don't see any token!!")
		exit()  # If no markers are detected, the program ends
	    elif Golden_tokens[0][0] < d_th:
		print("Found the GOLDEN TOKEN!")
		R.grab()  # If we are close to the token, we grab it.
		turn(-5, t_1) #turn after grabing the token
		print("I turned")
		drive(30,t_3) #drive to the centre to release the token
		R.release() #release the token
		print("released the token")
		drive(-10, 2) #drive back after releasing the token
		turn(-5, t_2) #turn to find the other tokens
		print("I turned back")    
		print("Gotcha!")
		break; #exit the while loop
	    elif Golden_tokens[0][1] <= a_th:
		print("Ah, here we are!.")
		drive(10, 0.5)
	    elif Golden_tokens[0][1] < -a_th:
		print("Left a bit...")
		turn(-2, 0.5)
	    elif Golden_tokens[0][1] > a_th:
		print("Right a bit...")
		turn(+1, 0.5)

    
# Call the funtion "grab_and_release()" for each token   
grab_and_release(2,8,6)
grab_and_release(13,8,4)
grab_and_release(13,8,4)
grab_and_release(13,7,4.5)
grab_and_release(13,7,4)
grab_and_release(13,0,4)
	 



