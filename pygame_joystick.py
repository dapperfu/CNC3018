import pygame
pygame.init()
 
from clsJoystick import Controller
 
#   Open a window so that events can be received.
pygame.display.set_mode((640, 480))
#   _.
 
 
print("Total number of controllers:", Controller.joystick_count())
js =[None, None, None, None] # Up to 4 controllers
 
js[0] =Controller(index =0)
 
 
js[0].read_joystick_buffer()
 
print("Axis:", js[0].axis)
print("Buttons:", js[0].buttons)
print("Hats:", js[0].hats)
