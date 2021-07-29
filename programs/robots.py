"""
Simulates robots cleaning rectangular rooms.
Time required for two types of robots to clean rooms is analyzed.

# 6.00.2x Problem Set 2: Simulating robots
"""

import math
import random

# Original assignment has custom packages for visualization.
#import ps2_visualize
# Updated to standard packages.
import matplotlib.pyplot as plt

# For Python 2.7:
#from ps2_verify_movement27 import testRobotMovement
# If you get a "Bad magic number" ImportError, you are not using
# Python 2.7 and using most likely Python 2.6:

# Package 'ps2_verify_movement27' is not used because running Python 3.8.5
# ImportError: bad magic number in 'ps2_verify_movement27': b'\x03\xf3\r\n'


# === Provided class Position
class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """

    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: number representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        angle = float(angle)
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

    def __str__(self):
        return "(%0.2f, %0.2f)" % (self.x, self.y)


# === Problem 1
class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """

    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.

        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        self.width = width
        self.height = height
        self.tiles = {}

        for x in range(width):
            for y in range(height):
                self.tiles[(x, y)] = False

        def getWidth(self):
            return self.width

        def getHeight(self):
            return self.height

    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        self.tiles[(int(pos.getX()), int(pos.getY()))] = True

    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        return self.tiles[(m, n)]

    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return len(self.tiles)

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        numCleaned = 0
        for tile in self.tiles:
            if self.tiles[tile]:
                numCleaned += 1
        return numCleaned

    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        return Position(random.random()*self.width,
                        random.random()*self.height)

    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        return self.width > pos.getX() >= 0 and self.height > pos.getY() >= 0


class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """

    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.room = room
        self.speed = speed
        self.direction = 360*random.random()
        self.position = room.getRandomPosition()
        room.cleanTileAtPosition(self.position)

    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.position

    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.direction

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.position = position

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.direction = direction

    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        raise NotImplementedError  # don't change this!


# === Problem 2
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current
    direction; when it would hit a wall, it *instead* chooses a new direction
    randomly.
    """

    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        newPos = self.position.getNewPosition(self.direction, self.speed)
        if self.room.isPositionInRoom(newPos):
            self.setRobotPosition(newPos)
            self.room.cleanTileAtPosition(newPos)
        else:
            self.setRobotDirection(random.randint(0, 359))


# Code to see implementation of StandardRobot in action depends on
# package 'ps2_verify_movement27'
#testRobotMovement(StandardRobot, RectangularRoom)


# === Problem 3
def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. StandardRobot or
                RandomWalkRobot)
    """
    min_to_clean = min_coverage*width*height
    all_times = []
    for nt in range(num_trials):
        room = RectangularRoom(width, height)
        robots = []
        this_time = 0
        for nr in range(num_robots):
            robots.append(robot_type(room, speed))
        while room.getNumCleanedTiles() < min_to_clean:
            for i in range(num_robots):
                robots[i].updatePositionAndClean()
            this_time += 1
        all_times.append(this_time)
    return float(sum(all_times))/num_trials


mean_time = runSimulation(1, 1.0, 10, 10, 0.75, 30, StandardRobot)
print("The mean time for one standard robot to clean 80% of a room is ",
      mean_time, "seconds.")
print("Next, we compare times to clean a certain room",
      "for various numbers of standard robots and random-walk robots.")


# === Problem 4
class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random at the end of each time-step.
    """

    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        newPos = self.position.getNewPosition(self.direction, self.speed)
        if self.room.isPositionInRoom(newPos):
            self.setRobotPosition(newPos)
            self.room.cleanTileAtPosition(newPos)
        self.setRobotDirection(random.randint(0, 359))


def showPlot1(title, x_label, y_label):
    """
    What information does the plot produced by this function tell you?
    """
    num_robot_range = range(1, 11)
    times1 = []
    times2 = []
    for num_robots in num_robot_range:
        times1.append(runSimulation(
            num_robots, 1.0, 20, 20, 0.8, 20, StandardRobot))
        times2.append(runSimulation(
            num_robots, 1.0, 20, 20, 0.8, 20, RandomWalkRobot))
    plt.subplot(1, 2, 1)
    plt.plot(num_robot_range, times1)
    plt.plot(num_robot_range, times2)
    plt.title(title)
    plt.legend(('StandardRobot', 'RandomWalkRobot'))
    plt.xlabel(x_label)
    plt.ylabel(y_label)
#    plt.show()


def showPlot2(title, x_label, y_label):
    """
    What information does the plot produced by this function tell you?
    """
    aspect_ratios = []
    times1 = []
    times2 = []
    for width in [10, 20, 25, 50]:
        height = 300//width
#        print("Plotting cleaning time for a room of width:",
#              width, "by height:", height)
        aspect_ratios.append(width / height)
        times1.append(runSimulation(
            2, 1.0, width, height, 0.8, 200, StandardRobot))
        times2.append(runSimulation(
            2, 1.0, width, height, 0.8, 200, RandomWalkRobot))
    plt.subplot(1, 2, 2)
    plt.plot(aspect_ratios, times1)
    plt.plot(aspect_ratios, times2)
    plt.title(title)
    plt.legend(('StandardRobot', 'RandomWalkRobot'))
    plt.xlabel(x_label)
    plt.ylabel(y_label)
#    plt.show()


plt.figure(1, figsize=(15, 10))
# === Problem 5
#
# 1) Write a function call to showPlot1 that generates an appropriately-labeled
#     plot.
#
showPlot1('Standard vs. Random Robots', 'Number of Robots', 'Time to Clean')
#
# 2) Write a function call to showPlot2 that generates an appropriately-labeled
#     plot.
#
showPlot2('Standard vs. Random Robots', 'Aspect Ratio of Room', 'Time to Clean')
#
plt.show()
room = RectangularRoom(3, 5)
speed = 3.1
robot = StandardRobot(room, speed)
print("End position: {}.".format(robot.getRobotPosition()))
robot.updatePositionAndClean()
