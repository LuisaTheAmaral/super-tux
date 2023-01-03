import pygame 
from spritesheet import SpriteSheet
from common import Directions, Up, Left, Down, Right, Size_Up, ALPHA
import logging
from bonus_block import CoinBlock, EggBlock
from platforms import FlyingPlatform

# Global constants
CELL_SIZE = 50

class Agent(pygame.sprite.Sprite):
    def __init__(self, name, width, height, scale, direction):
        super().__init__()
        self.name = name
        self.sheet = SpriteSheet("assets/creatures/spritesheet_full.png")
        self.scale = scale
        self.control_keys = {}
        self.dead = False

        self.walking_pointer = 0
        self.direction = direction

        self.HEIGHT = height*self.scale
        self.WIDTH = width*self.scale
  
        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0

        # List of level sprites
        self.level = None

    def set_start_position(self, x, y):
        self.change_x, self.change_y = 0,0
        self.rect.x, self.rect.y = x*self.scale, y*self.scale

    def controls(self, up, left, down, right, grow):
        self.control_keys = {
            up: Up, 
            left: Left, 
            down: Down, 
            right: Right, 
            grow: Size_Up}
 
    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35

        # See if we are on the ground
        if self.rect.y >= self.HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = self.HEIGHT - self.rect.height
 
    def jump(self):
        """ Called when user hits 'jump' button. """
        # Move down 2 pixels to see if there is a platform bellow us
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2
 
        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= self.HEIGHT:
            self.change_y = -10
    
    def move(self, direction, change_x):
        """ Move agent. """
        self.direction = direction
        if direction == Directions.LEFT:
            self.change_x = change_x*-1
        elif direction == Directions.RIGHT:
            self.change_x = change_x
          
    def update(self, x, y ,frameX, frameY, cell_size=(CELL_SIZE,CELL_SIZE)):
        """ Update Agent's sprite. """
        # Gravity
        self.calc_grav()
 
        # Move left/right
        self.rect.x += self.change_x
 
        # verify collisions
        self.collisions()

        self.image = self.sheet.image_at((frameX * cell_size[0], frameY * cell_size[1], cell_size[0], cell_size[1]), colorkey=ALPHA)
        
     
    def collisions(self):
        """ Verify collisions of agent with platforms. """
        # See if we hit anything
        idle = 0
        n_coins_hit = 0
        n_eggs_hit = 0
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if not isinstance(block,FlyingPlatform):
            # If moving right, set right side to the left side of the item we hit
                if self.change_x > 0:
                    self.rect.right = block.rect.left
                    self.direction_auto = Directions.LEFT
                        
                elif self.change_x < 0:
                    # Otherwise if we are moving left, do the opposite
                    self.rect.left = block.rect.right
                    self.direction_auto = Directions.RIGHT
 
        # Move up/down
        self.rect.y += self.change_y
 
        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
 
            # if enemy is on the edge of the platform change direction 
            if self.rect.centerx+20 >= block.rect.right:
                self.direction_auto = Directions.LEFT
                
            elif self.rect.centerx-20 < block.rect.left:
                self.direction_auto = Directions.RIGHT
 
            # Reset our position based on the top/bottom of the object
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
                #if tux hits a coin block break it
                if isinstance(block, CoinBlock):
                    box_broken = block.break_block()
                    if box_broken:
                        n_coins_hit += 1
                #if tux hits a power block break it
                elif isinstance(block, EggBlock):
                    box_broken = block.break_block()
                    if box_broken:
                        n_eggs_hit += 1
 
            # Stop our vertical movement
            self.change_y = 0

        #making sure that tux changes to idle when he lands on the ground and does not move
        if self.change_y == 0 and self.change_x == 0:
            idle = 1
                
        return idle, n_coins_hit, n_eggs_hit
 
    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0

    def kill(self):
        """ Kill agent. """
        logging.info("Agent died")
        self.dead = True