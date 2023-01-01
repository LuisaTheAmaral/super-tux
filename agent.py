import pygame 
from spritesheet import SpriteSheet
from common import Directions, Up, Left, Down, Right, ALPHA
import logging
from enum import Enum

# Global constants
CELL_SIZE = 50

class Agent(pygame.sprite.Sprite):
    def __init__(self, name, initial_x, initial_y, width, height, scale):
        super().__init__()
        self.name = name
        self.sheet = SpriteSheet("sprites/spritesheet_full.png")
        self.scale = scale
        self.control_keys = {}
        self.dead = False

        self.walking_pointer = 0
        self.direction = Directions.RIGHT
        frameX, frameY = (0, 3) # idle coords
        
        self.image = self.sheet.image_at((frameX * CELL_SIZE, frameY * CELL_SIZE, CELL_SIZE, CELL_SIZE), colorkey=ALPHA)
        self.rect = self.image.get_rect()
        self.set_start_position(initial_x, initial_y) #set player initial  position 

        self.HEIGHT = height*self.scale
        self.WIDTH = width*self.scale
  
        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0

        # List of level sprites
        self.level = None

    def set_start_position(self, x, y):
        self.rect.x, self.rect.y = x*self.scale, y*self.scale

    def controls(self, up, left, down, right):
        self.control_keys = {
            up: Up, 
            left: Left, 
            down: Down, 
            right: Right}
 
    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35
 
    def jump(self, previous):
        """ Called when user hits 'jump' button. """
        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down 1
        # when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2
 
        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= self.HEIGHT:
            self.change_y = -10
 
    # Player-controlled movement:
    def move(self, direction):
        self.direction = direction
        if direction == Directions.LEFT:
            self.change_x = -6
        elif direction == Directions.RIGHT:
            self.change_x = 6
            
    def update(self, x, y ,frameX, frameY):
        # Gravity
        self.calc_grav()
 
        # Move left/right
        self.rect.x += self.change_x
 
        # verify collisions
        frameX, frameY = self.collisions(frameX, frameY)

        self.image = self.sheet.image_at((frameX * CELL_SIZE, frameY * CELL_SIZE, CELL_SIZE, CELL_SIZE), colorkey=ALPHA)
        
            
    def collisions(self, frameX, frameY):
        # See if we hit anything
        idle = 0
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
                try:
                    self.direction_auto = Directions.LEFT
                except:
                    pass
                    
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite
                self.rect.left = block.rect.right
                try:
                    self.direction_auto = Directions.RIGHT
                except:
                    pass
 
        # Move up/down
        self.rect.y += self.change_y
 
        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
 
            # Reset our position based on the top/bottom of the object
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
 
            # Stop our vertical movement
            self.change_y = 0

        #making sure that tux changes to idle when he lands on the ground and does not move
        if self.change_y == 0 and self.change_x == 0:
            idle = 1
                
        return frameX, frameY, idle
 
    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0

    def kill(self):
        logging.info("Agent died")
        self.dead = True