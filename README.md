# First Assignment

In this assignment we should gather all tokens(6 tokens) together which using this code they all are
gathered on the center.
In figure 1 and figure 2 shows the environment of the program in the initial and the final frame.

![](sr/the initial frame.png)
> Fig.1) The configuration of the initial frame

![](sr/the final frame.png)
> Fig.2)The configuration of the final frame

Python Robotics Simulator
================================

This is a simple, portable robot simulator developed by [Student Robotics](https://studentrobotics.org).
Some of the arenas and the exercises have been modified for the Research Track I course


### Installing & Running
----------------------

The simulator requires a Python 2.7 installation, the [pygame](http://pygame.org/) library, [PyPyBox2D](https://pypi.python.org/pypi/pypybox2d/2.1-r331), and [PyYAML](https://pypi.python.org/pypi/PyYAML/).

Pygame, unfortunately, can be tricky (though [not impossible](http://askubuntu.com/q/312767)) to install in virtual environments. If you are using `pip`, you might try `pip install hg+https://bitbucket.org/pygame/pygame`, or you could use your operating system's package manager. Windows users could use [Portable Python](http://portablepython.com/). PyPyBox2D and PyYAML are more forgiving, and should install just fine using `pip` or `easy_install`.


to run the program follow the next steps:

1) Go to desktop and Clone the repository https://github.com/Mobina-A/RT1_-First-
Assignment/tree/main/Assignment/python_simulator with:

```bash

$ git clone https://github.com/Mobina-A/RT1_FirstAssignment.git


```
2) Go to file including assignment.py with:
```bash
$ cd ~/root/Desktop/Assignment/python_simulator/robot-sim
```
3) run the program with:
```bash
$ python2 run.py assignment.py
```

### Troubleshooting
-----------------------

When running `python run.py <file>`, you may be presented with an error: `ImportError: No module named 'robot'`. This may be due to a conflict between sr.tools and sr.robot. To resolve, symlink simulator/sr/robot to the location of sr.tools.

On Ubuntu, this can be accomplished by:
* Find the location of srtools: `pip show sr.tools`
* Get the location. In my case this was `/usr/local/lib/python2.7/dist-packages`
* Create symlink: `ln -s path/to/simulator/sr/robot /usr/local/lib/python2.7/dist-packages/sr/`

### Functions & Methods
-----------------------------
### Robot API

The API for controlling a simulated robot is designed to be as similar as possible to the [SR API][sr-api].

#### Motors ####

The simulated robot has two motors configured for skid steering, connected to a two-output [Motor
Board](https://studentrobotics.org/docs/kit/motor_board). The left motor is connected to output `0` and
the right motor to output `1`.

The Motor Board API is identical to [that of the SR API]
(https://studentrobotics.org/docs/programming/sr/motors/), except that motor boards cannot be
addressed by serial number. So, to turn on the spot at one quarter of full power, one might write the
following:

```python
R.motors[0].m0.power = 25
R.motors[0].m1.power = -25
```
#### The Grabber ####

The robot is equipped with a grabber, capable of picking up a token which is in front of the robot and
within 0.4 metres of the robot's centre. To pick up a token, call the `R.grab` method:

```python
success = R.grab()
```

The `R.grab` function returns `True` if a token was successfully picked up, or `False` otherwise. If the
robot is already holding a token, it will throw an `AlreadyHoldingSomethingException`.

To drop the token, call the `R.release` method.

Cable-tie flails are not implemented.

#### Vision ####

To help the robot find tokens and navigate, each token has markers stuck to it, as does each wall. The
`R.see` method returns a list of all the markers the robot can see, as `Marker` objects. The robot can only
see markers which it is facing towards.

Each `Marker` object has the following attributes:

* `info`: a `MarkerInfo` object describing the marker itself. Has the following attributes:
* `code`: the numeric code of the marker.
* `marker_type`: the type of object the marker is attached to (either `MARKER_TOKEN_GOLD`,
`MARKER_TOKEN_SILVER` or `MARKER_ARENA`).
* `offset`: offset of the numeric code of the marker from the lowest numbered marker of its type. For
example, token number 3 has the code 43, but offset 3.
* `size`: the size that the marker would be in the real game, for compatibility with the SR API.
* `centre`: the location of the marker in polar coordinates, as a `PolarCoord` object. Has the following
attributes:
* `length`: the distance from the centre of the robot to the object (in metres).

* `rot_y`: rotation about the Y axis in degrees.
* `dist`: an alias for `centre.length`
* `res`: the value of the `res` parameter of `R.see`, for compatibility with the SR API.
* `rot_y`: an alias for `centre.rot_y`
* `timestamp`: the time at which the marker was seen (when `R.see` was called).

For example, the following code lists the code of all tokens located on the side of the robot's view.

```python
List_of_token_code=[]
for token in R.see():
token_code = token.info.code
List_of_token_code.append(token_code)

print('token codes:',List_of_token_code)
```
[sr-api]: https://studentrobotics.org/docs/programming/sr/

### Code
-----------------------------
The code consists of four functions:
* drive(speed, seconds)
* turn(speed, seconds)
* find()
* grab_and_release(t_1,t_2,t_3)

#### Function drive()
This function has two aurguments; 'speed' and 'seconds'.
In this function, we set the same speed for both of the robot's motors. By using the argument 'seconds'
and the 'sleep' function from the time module, we allow the robot to continue its path at the previously set
speed and then set the motor speeds to zero to stop it.
```python
def drive(speed, seconds):
R.motors[0].m0.power = speed
R.motors[0].m1.power = speed
time.sleep(seconds)
R.motors[0].m0.power = 0
R.motors[0].m1.power = 0
```

#### Function turn()
This function has two aurguments; 'speed' and 'seconds'.
To turn the robot, there is two methods:
* The speeds of the motors should be different. If we want to turn the robot to the left, the speed of the
right motor should be higher than the left one, and vice versa.
* The motors turn at the same speed but in different directions. For example, if we want the robot to turn
left, the speed of the right motor should be positive, and the speed of the left motor should be negative.

We follow the second method in this function.
By using the argument 'seconds' and the 'sleep' function from the time module, we allow the robot to
continue its path at the previously set speed and then set the motor speeds to zero to stop it.
```python
def turn(speed, seconds):
R.motors[0].m0.power = speed
R.motors[0].m1.power = -speed
time.sleep(seconds)
R.motors[0].m0.power = 0
R.motors[0].m1.power = 0
```
#### Function find()
In this function, we store the attributes of tokens within the robot's field of view in a list. Then, we sort the
list based on the distance of each token from the robot to find the nearest token. After sorting, the first
item (index[0]) in the list represents the nearest token to the robot.
```python
def find():
Golden_tokens_initial = []

dist = 100
for token in R.see():
token_type = token.info.marker_type
dist = token.dist
rot_y = token.rot_y
marker_data = [dist, rot_y]

Golden_tokens_initial.append(marker_data)

Golden_tokens = sorted(Golden_tokens_initial, key=lambda x: x[0]) # Sort the list of marker data by
dist
if Golden_tokens[0][0] < 100:
return Golden_tokens
else:

return None

```
#### Function grab_and_release()
This function has two aurguments; 't_1','t_2' and 't_3'.they are are 'second' argument in functions turn()
and drive().
* t_1: Time that the robot turns after grabbing the token
* t_2: Time that the robot turns after releasing the token
* t_3: Time that the robot continues in a straight line toward the center to release the token

This function guides the robot toward the nearest token, grab it, move toward the center, and release the
token.

```python
def grab_and_release(t_1,t_2,t_3):

while True:
Golden_tokens = find()
print(Golden_tokens)

if Golden_tokens == None:
print("I don't see any token!!")
exit()
elif Golden_tokens[0][0] < d_th:
print("Found the GOLDEN TOKEN!")
R.grab()
turn(-5, t_1)
print("I turned")
drive(30,t_3)
R.release()
print("released the token")
drive(-10, 2)
turn(-5, t_2)
print("I turned back")
print("Gotcha!")
break;
elif Golden_tokens[0][1] <= a_th:
print("Ah, here we are!.")
drive(10, 0.5)

elif Golden_tokens[0][1] < -a_th:
print("Left a bit...")
turn(-2, 0.5)
elif Golden_tokens[0][1] > a_th:
print("Right a bit...")
turn(+1, 0.5)

```
#### Call the function
For the last step, we call the function for each of the tokens.
```python
grab_and_release(2,8,6)
grab_and_release(13,8,4)
grab_and_release(13,8,4)
grab_and_release(13,7,4.5)
grab_and_release(13,7,4)
grab_and_release(13,0,4)
```
