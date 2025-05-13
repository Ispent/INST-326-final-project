""" Defines a car class that performs a series of movements and prints
    its final coordinates. 
"""
import math

class Car:
    """ A class representing a car's movement.
    
    Attributes:
        x (float): the starting x coordinate of the car.
        y (float): the starting y coordinate of the car.
        heading (float): the starting direction of the car.
    """
    def __init__(self, x=0, y=0, heading=0):
        """ Initializes the car and sets its default coordinates and direction.
    
        Args:
            x (float): see class documentation.
            y (float): the starting y coordinate of the car.
            heading (float): the starting direction of the car.
        """
        self.x = x
        self.y = y 
        self.heading = heading
        
    def turn(self, degrees):
        """ Turns the car by a specified # of degrees.
    
        Args:
            degrees (float): the direction the car turns in; a positive # of degrees.
            indicates a clockwise turn; a negative # of degrees indicates a counterclockwise turn.
        Side effects:
            Modifies the heading attribute of the Car.
        """
        self.degrees = degrees
        
        #updating heading by adding a specified # of degrees, then performing modulo 360 on the sum
        self.heading += degrees
        self.heading %= 360 
    
    def drive(self, distance):
        """ Moves the car forward by a specified distance in the current direction.
    
        Args:
            x (float): see class documentation.
            y (float): the starting y coordinate of the car.
            heading (float): the starting direction of the car.
        Side effects:
            Modifies the x and y attributes of the Car. 
        """
        self.distance = distance
        
        h = self.heading * (math.pi /180) #converting degrees to radians
        
        #updating x and y attributes to reflect movement in x and y axes.
        self.x += self.distance * (math.sin(h))
        self.y -= self.distance * (math.cos(h)) 
        
def sanity_check():
    """ Performs a series of movements to test the Car class' functionality
     Side effects:
            Prints the car's final coordinates and heading.
    """
    #creating an instance of the Car class
    car_drive = Car()
    
    #performs a series of movements 
    car_drive.turn(90)
    car_drive.drive(10)
    car_drive.turn(30)
    car_drive.drive(20)

    print(f"Location: {car_drive.x}, {car_drive.y}")
    print(f"Heading: {car_drive.heading}")
    return car_drive
    
if __name__ == "__main__":
    sanity_check() 
    
    