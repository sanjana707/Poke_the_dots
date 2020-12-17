# Poke the Dots Version 3
# This game has a two graphical objects - dots moving in the window
# One dot is big and the other is small
# One dot moves vertically and th e other moves horizontally
# When the dots touch the window edge they bounce back and keep moving
# The score increases by 1 per second untill the dots don't collide
# The window closes if the player clicks the close button
# When the player clicks the left mouse button the dots teleport to any new random location 
# The game ends when the two dots collide with each other
# Then the window displays the final score and the GAME OVER message on the screen

from uagame import Window
from math import sqrt
from pygame import QUIT, Color, MOUSEBUTTONUP
from pygame.time import Clock , get_ticks 
from pygame.event import get as get_events
from pygame.draw import circle as draw_circle
from random import randint

def main():
    #create_game
    game = Game()
    game.play()

class Game :
    #An object in this class represents the whole game
    #----window
    #----close_selected
    #----clock
    #----frame_rate
    #----small dot
    #----big dot
    
    def __init__(self):
        #create window
        self._window =  Window('Move the Dots', 500, 400)
        self._adjust_window()
        #create clock
        #create small dot
        #create big dot
        #Dot: randomize small_dot
        #Dot: randomize big_dot
        self._close_selected = False
        self._clock = Clock()
        self._frame_rate = 90
        self._score = 0
        self._small_dot = Dot('red', [50, 75], 30, [1,2], self._window)
        self._big_dot = Dot('blue', [200,100], 40, [2,1], self._window) 
        self._small_dot.randomize()
        self._big_dot.randomize() 
        self._continue_game = True
    
    def _adjust_window(self):
        self._window.set_bg_color('black')
        self._window.set_font_name('ariel')
        self._window.set_font_size(64)        
        
    
    def play(self):
        #while player has not selected close
          #play frame
          #----Game: handle events
          #----Game: draw
          #----Game: update
        #close window
        while not self._close_selected:
            # play frame
            self.handle_events()
            self.draw()
            self.update()   
        self._window.close()    
    
    
    def handle_events(self):
        #for event in event_list
           #Game: handle one event
        event_list = get_events()
        for event in event_list :
            self.handle_one_event(event)
            
    def handle_one_event(self, event):
        #if event category equals close:
        #-----remember player has selected close
        #else :
        # handle non close event
        #----if event category equals mouse click
        #-------handle mouse click
        #handle one event
        if event.type == QUIT:
            self._close_selected  = True
        #---if event category equals mouse click    
        elif self._continue_game and event.type == MOUSEBUTTONUP :
            self.handle_mouse_click()        
    
    
    def handle_mouse_click(self):
        #Dot: randomize small dot
        #Dot: randomize big dot
        self._small_dot.randomize()
        self._big_dot.randomize()   
        
    
    def draw(self):
        #clear window
        #Game: draw score
        #Dot: draw small dot
        #Dot: draw big dot
        #update display
        self._window.clear()
        self.draw_score()
        self._small_dot.draw()
        self._big_dot.draw()
       
        if not self._continue_game :
            self.draw_game_over()
            
        self._window.update()     
        
    def draw_score(self):
      #Draws the score string every time it is called with the current time elapsed
      score_string = 'Score :' + str(self._score)
      self._window.draw_string(score_string, 0, 0)    
      
    def draw_game_over(self):
        string = 'GAME OVER'
        font_color = self._small_dot.get_color()
        bg_color = self._big_dot.get_color()
        original_font_color = self._window.get_font_color()
        original_bg_color = self._window.get_bg_color()
        self._window.set_bg_color(bg_color)
        self._window.set_font_color(font_color)
        height = self._window.get_height() - self._window.get_font_height()
        self._window.draw_string(string, 0, height)
        self._window.set_bg_color(original_bg_color)
        self._window.set_font_color(original_font_color)        
    
    def update(self):
        #Dot: move small dot
        #Dot: move big dot
        #Control frame rate
        #Update score using time elapsed
        if self._continue_game :
           self._small_dot.move_dot()
           self._big_dot.move_dot()
           self._score = get_ticks()//1000
        self._clock.tick(self._frame_rate)
         
        if self._small_dot.intersects(self._big_dot):
            self._continue_game = False
            
    

class Dot:
    #An object in this class represents the dots
    #---color
    #---center
    #---radius
    #---velocity
    #---window
    
    def __init__(self, color, center, radius, velocity, window):
        self._color = color
        self._center = center
        self._radius = radius
        self._velocity = velocity
        self._window = window        
    
    def draw(self):
        # Draw the dot on the surface.
        # - self is the Dot        
        surface = self._window.get_surface()
        color_string = Color(self._color)
        draw_circle(surface, color_string, self._center, self._radius)
   
    def move_dot(self): 
        #Moves the dots across the window
        #---When the dot hits the right edge the velocity of the dot is reversed and it seems to bounce back
        #---Same happens for top, bottom, and left edge
        size = (self._window.get_width(), self._window.get_height())
        for index in range(0, 2):
           self._center[index] = self._center[index] + self._velocity[index]
           if (self._center[index] + self._radius >= size[index]) or (self._center[index]<= self._radius):
                  self._velocity[index] = -self._velocity[index]                
    
    def randomize(self):
    # Change the dot so that its center is at a random
    # point on the surface. Ensure that no part of a dot
    # extends beyond the surface boundary.
    # - dot is the Dot to randomize    
      size = (self._window.get_width(), self._window.get_height())
      for index in range(0, 2):
          self._center[index] = randint(self._radius, size[index] - self._radius)  
          
    def intersects(self,dot):
        # Return True if the two dots intersect and False if
            # they do not.
            # - self is a Dot
            # - dot is the other Dot        
        distance = sqrt((self._center[0] - dot._center[0])**2 + (self._center[1] - dot._center[1])**2)
        return distance <= self._radius + dot._radius
        
        
    def get_color(self):
        # Return a str that represents the color of the dot.
            # - self is the Dot        
        return self._color
    
main()
