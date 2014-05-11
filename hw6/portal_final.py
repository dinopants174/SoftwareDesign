# -*- coding: utf-8 -*-
"""
Created on Fri Mar  7 16:58:55 2014

@author: zoherghadyali, jaywoo, sophiali
"""

import pygame, random, math, time
from pygame.locals import *
from world import *
         
class Portal_Platformer_Model:      #game encoded in model, view, controller format
    """ Encodes all of the data in the game into one model """
    def __init__(self): #initial conditions for mode
        self.player = Player(40,40)
        self.portal_orange = 'null'
        self.portal_blue = 'null'
        # Python has a None for precisely this reason. And its great for many reasons,
        # chief among them, that you can test "if variable:" as though variable were a
        # variable, and if it is None, it will return false. Use it. Love it.
        self.level = 0
        self.construct_environment(0)   #builds the first level immediately
        
    def construct_environment(self, number):
        """ Generates rectangles for every wall and the cake and stores it in the variable "walls" """

        # Great! I love that this is a method that actually 'loads in' levels rather than them being
        # hardcoded. I also do like that the worlds are held in a seperate file to avoid clutter. One
        # good final step here might actually be to go all the way to pickling them and saving them in
        # that format, but that is optional. Nice work here!

        self.walls = [] #initalizes empty list to hold the positions of all of our walls
        self.cake = None
        level = world   #world contains a list of lists of each level, consisting of W's, spaces, and C's
        for platform in level:
            x = y = 0 
            for row in level[number]:
                for col in row:
                    if col == "W":  #if the level has a W encoded, build a wall there
                        self.walls.append(Wall((x, y)))
                    if col == "C":
                        self.cake = Cake_top((x,y)) #if the level has a C encoded, build a cake there
                        self.cake2 = Cake_bottom((x,y))
                    x += 20 #Traverses each column in the world file
                y += 20 #Goes to the next row
                x = 0 #Restarts at the first column
        
    def playerCollisionsX(self, dx):
        """ Moves the player in the x axis by a certain amount and checks if there are collisions """
        self.player.rect.x += dx #Moves the player by dx
        
        for wall in self.walls: #Checks if the player is colliding with any of the walls
            if self.player.rect.colliderect(wall):
                if dx > 0:
                    self.player.rect.right = wall.rect.left #Prevents right side of player from going through left side of wall
                if dx < 0:
                    self.player.rect.left = wall.rect.right #Prevents left side of player from going through right side of wall
                    
    def playerCollisionsY(self):
        """ Moves the player in the y axis, depending on the velocity and the acceleration """
        self.player.vy += self.player.ay #Updates the velocity, depending on acceleration
        if self.player.vy >= 5.0: #Terminal velocity
            self.player.vy = 5.0
        if self.player.vy <= -5.0:
            self.player.vy = -5.0
            
        self.player.rect.y += self.player.vy #Moves the player by vy
        
        for wall in self.walls: #Checks if the player is colliding with any of the walls
            if self.player.rect.colliderect(wall):
                if self.player.vy > 0:
                    self.player.rect.bottom = wall.rect.top #Prevents bottom side of player from going through top of wall
                    self.player.canJump = True
                if self.player.vy < 0:
                    self.player.rect.top = wall.rect.bottom #Prevents top side of player from going through bottom of wall
            
   
    def update(self):
        """ Updates the model to react to changes made by the controller, ex. if they finish the level, loads the next one in the model or
        if they collide with a portal, positions them out of second portal"""
        self.playerCollisionsY() #Updates the y component of player
        
        if self.player.rect.colliderect(self.cake.rect): #Checks if the player gets to the cake and takes the player to the next level
            self.level += 1     #if player collides with cake, calls create_environment for next level
            if self.level > 4:  #if we are out of levels, displays the end-game picture
                image("cake.png",True)
            self.walls = []
            self.player.rect.x = 40
            self.player.rect.y = 40
            self.player.vx= 0
            self.player.vy = 0
            self.portal_blue = 'null'
            self.portal_orange = 'null'
            self.construct_environment(self.level)  #reinitalizing empty objects / lists for the next level and puts player back to initial location

        if self.portal_blue != 'null' and self.portal_orange != 'null':
            # Use the Nonetype here as noted above: its much cleaner
            if self.player.rect.colliderect(self.portal_orange.rectp): #Moves player from orange portal to blue portal
                # And kill the dead code...
#                print "Collision detected!"   #FOR DEBUGGING PURPOSES
                xp = self.portal_blue.rectp.x
                yp = self.portal_blue.rectp.y
                self.player.rect.x = xp + 30 #Adds an offset of 30
                self.player.rect.y = yp + 30 #to prevent an infinite loop
                return
                
            if self.player.rect.colliderect(self.portal_blue.rectp): #Moves player from blue portal to orange portal
#                print "Collision detected!"  #FOR DEBUGGING PURPOSES
                xp = self.portal_orange.rectp.x
                yp = self.portal_orange.rectp.y
                self.player.rect.x = xp + 30 #Adds an offset of 30
                self.player.rect.y = yp + 30 #to prevent an infinite loop
                return  
            
            else:
                pass
            
    def portal_update_orange(self,portalclick):
        """ Changes the wall to an orange portal block on click"""
        self.portal_orange = Portal(portalclick)
        
    def portal_update_blue(self,portalclick):
        """ Changes the wall to a blue portal block on click"""
        self.portal_blue = Portal(portalclick)
        
class PyGameWindowView:
    """ Draws our game in a Pygame window, the view part of our model, view, controller"""
    def __init__(self,model,screen):
        """ Initializes view when the game starts """
        self.model = model
        self.screen = screen
    
    def draw(self):
        """Draws our level, player, cake, and portals on click in the screen"""
        self.screen.fill(pygame.Color(0,0,0)) #Background
        pygame.draw.rect(self.screen, pygame.Color(109, 109, 109), self.model.player.rect) #Player
        for wall in self.model.walls: #Draws each wall block
            pygame.draw.rect(screen, pygame.Color(255, 255, 255), wall.rect)
        pygame.draw.rect(screen, pygame.Color(255,105,201), self.model.cake.rect)
        pygame.draw.rect(screen, pygame.Color(94, 38, 25), self.model.cake2.rect) #Cake
   
        if self.model.portal_orange != 'null': #Orange portal
            pygame.draw.rect(self.screen, pygame.Color(255,153,0),self.model.portal_orange.rectp)
        if self.model.portal_blue != 'null': #Blue portal
            pygame.draw.rect(self.screen, pygame.Color(102,204,255),self.model.portal_blue.rectp)    
       
        pygame.display.update() #updates view to respond to changes made by controller


class PyGameKeyboardController:
    """ Manipulate game state based on keyboard input, the controller part of our model, view, controller"""
    def __init__(self, model):
        """ Initializes controller to deal with keyboard input """
        self.model = model
    
    def handle_pygame_key(self):
        """ Changes x and y position of the player with key presses, also checks for collision detection"""
        keypressed = pygame.key.get_pressed()
        if keypressed[pygame.K_LEFT]:
            self.model.playerCollisionsX(-2)
        if keypressed[pygame.K_RIGHT]:
            self.model.playerCollisionsX(2)
        if keypressed[pygame.K_UP] and self.model.player.canJump:
            self.model.player.vy = -5.0
            self.model.player.canJump = False
            
    def handle_pygame_mouse(self, event):
        """Takes position of mouse click and passes coordinates of collision
        to model to draw portals"""
        x, y = event.pos #Sets click position
        xp = float(self.model.player.rect.x+10) #Finds the center 
        yp = float(self.model.player.rect.y+10) #of the block
        distance = math.sqrt((x-xp)**2 + (y-yp)**2) #Finds distance between player and click
        dx = (x-xp)/distance * 2 #X component of unit vector (times 2 for faster processing)
        dy = (y-yp)/distance * 2 #Y component of unit vector (times 2)

        while distance >= 2:
            xp += dx #loops through the x and y positions on the line connecting the mouse click and the player
            yp += dy
            
            distance -= 2
            
            for wall in self.model.walls:
                if wall.rect.collidepoint(xp,yp):
                    portalclick = pygame.Rect.copy(wall.rect) #when there's collision, passes coordinates to model
                    if event.button == 1:
                        self.model.portal_update_orange(portalclick) #left click orange portal
                    if event.button == 3:
                        self.model.portal_update_blue(portalclick) #right click blue portal
                    return
        
class Player:
    """Code for our moving player"""
    def __init__(self,x,y):
        self.rect = pygame.Rect(x,y,20,20)
        self.canJump = False
        self.vy = 0.0
        self.ay = 0.15
        
class Wall:
    """ Encodes the state of a singular rectangular platform in the game """
    def __init__(self, pos):
        self.rect = pygame.Rect(pos[0], pos[1], 20, 20)
    
class Cake_top(object):
    """The icing on the cake """
    # Haha. I appreciate the docstring.
    def __init__(self, pos):
         self.rect = pygame.Rect(pos[0], pos[1], 25, 10)
         
class Cake_bottom(object):
    """The chocolate cakey part of the cake"""
    def __init__(self, pos):
         self.rect = pygame.Rect(pos[0], pos[1]+10, 25, 15)
         
class Portal(object):
    """This is a portal"""
    def __init__(self,wall):
        if wall == 'null':
            pass
        else:
            box = wall
            self.rectp = box.inflate(10,10)

def image(image,end):
    """Takes an image and displays it for a few seconds
    These are our punchline images, purely for artistic purposes"""

    # I think these ar fantastic. Nice job with these!
    
    time.sleep(1)
    startscreen = pygame.image.load(image).convert()
    screen.blit(startscreen,(175,75))
    pygame.display.flip()
    time.sleep(0.5)
    screen.blit(startscreen,(175,70))
    pygame.display.flip()
    time.sleep(0.5)
    screen.blit(startscreen,(175,75))
    pygame.display.flip()
    time.sleep(0.5)
    screen.blit(startscreen,(175,75))
    pygame.display.flip()
    time.sleep(0.5)
    screen.blit(startscreen,(175,75))
    pygame.display.flip()
    time.sleep(0.5)
    screen.blit(startscreen,(175,75))
    pygame.display.flip()
    time.sleep(0.5)
    screen.blit(startscreen,(175,70))
    time.sleep(0.5)
    if end:
        pygame.quit()

if __name__ == '__main__':
    pygame.init()   #initializes our game
    size = (700, 500)
    screen = pygame.display.set_mode(size)
    model = Portal_Platformer_Model()
    view = PyGameWindowView(model,screen)
    controller = PyGameKeyboardController(model)
    
    music = pygame.mixer.music.load("StillAlive.mp3")   #loads our background music and plays it 
    pygame.mixer.music.play()
    
    image("companion_cube.png",False)   #our starting image

    running = True

    while running:
           
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == MOUSEBUTTONDOWN:
                controller.handle_pygame_mouse(event)
        controller.handle_pygame_key()
        model.update()
        view.draw()
        time.sleep(0.001)
        
    image("plate.png", True)
