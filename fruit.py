""" CS108 final project - fruit class

This is the model of the fruit class used in our final project

@author: Ben Kosters (bak32)
@author: Tyler Bylsma (tjb65)
@date: December, 2022
"""
import random

class Fruit:
    
    def __init__(self, x, y, vel_x=5, vel_y=5,acc_x = 0.25, acc_y = 1,height = 20, radius=40, pos_direction = True, fruit_type = "Watermelon"):
        """Instantiate a fruit object.
        """
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.acc_x = acc_x
        self.acc_y = acc_y
        self.height = height
        self.radius = radius
        self.pos_direction = pos_direction
        self.fruit_type = fruit_type
        
    def draw(self,drawing):
        """used to draw each circle
        """
        add_image_to_drawing(drawing = self.drawing, image= self.get_random_fruit()) #image = self.watermelon_picture)
        
        
        
    def move(self, drawing):
        """This method will handle the movements of each fruit, with parabolic trajectories
            The move method from the ball module was used as a base for this method
        """
        
        if self.vel_y > 30:
            self.acc_y *= -1
        if self.vel_x < 0:
            self.acc_x *= -1
            
        if self.pos_direction == True:
        
            self.x+= self.vel_x
            self.y -= self.vel_y
    
            self.vel_x += self.acc_x
            self.vel_y += self.acc_y
        else:
            self.x -= self.vel_x
            self.y += self.vel_y
            
            self.vel_x += self.acc_x
            self.vel_y += self.acc_y
        
        
        
    
        
    def slices(self, x,y, fruit):
        """This method is used to check if the fruit is sliced by the the mouse
        """
        if (self.x< x <self.x+fruit.height) and (self.y < y < self.y +fruit.height):
            return True
        else:
            return False
        
        
