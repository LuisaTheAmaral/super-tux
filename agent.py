import pygame 
from spritesheet import SpriteSheet
from common import Directions, Up, Left, Down, Right, ALPHA
import logging

# Global constants
CELL_SIZE = 50

class Agent(pygame.sprite.Sprite):
    def __init__(self, name, width, height, scale):
        super().__init__()
        self.name = name
        self.sheet = SpriteSheet("sprites/spritesheet_full.png")
        self.SCALE = scale
        self.control_keys = {}
        self.dead = False
        
        self.walking = [(2, 0), #walk-0 
                        (0, 1), #walk-1 
                        (1, 1), #walk-2
                        (2, 1), #walk-3
                        (0, 2), #walk-4
                        (1, 2), #walk-5
                        (2, 2), #walk-6
                        (3, 0)] #walk-7
        self.walking_r = [(2, 3), #walk-0 
                        (0, 4), #walk-1 
                        (1, 4), #walk-2
                        (2, 4), #walk-3
                        (0, 5), #walk-4
                        (1, 5), #walk-5
                        (2, 5), #walk-6
                        (3, 3)] #walk-7

        self.idle = (0, 0)
        self.idle_r = (0, 3)
        self.jump_sprite = (3, 1)
        self.jump_r = (3, 4)
        self.walking_pointer = 0
        
        self.facing_dir = Directions.RIGHT # starts facing right
        self.direction = Directions.RIGHT
        frameX, frameY = self.idle_r
        self.image = self.sheet.image_at((frameX * CELL_SIZE, frameY * CELL_SIZE, CELL_SIZE, CELL_SIZE), colorkey=ALPHA)
        self.rect = self.image.get_rect()
        self.HEIGHT = height*scale
        self.WIDTH = width*scale
 
        self.rect = self.image.get_rect()
        self.prev_body = (340, height - self.rect.height)
 
        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0
 
        # List of level sprites
        self.level = None

    def controls(self, up, left, down, right):
        self.control_keys = {
            up: Up, 
            left: Left, 
            down: Down, 
            right: Right}

    def commands(self, control):
        if control in self.control_keys.keys():
            cmd = self.control_keys[control]()
            cmd.execute(self)
            return cmd
 
    def update(self):
        # Get body
        x, y = self.rect.x, self.rect.y
        
        #if tux is jumping, render jump sprite
        if self.direction == Directions.UP:
            if self.facing_dir == Directions.LEFT:
                frameX, frameY = self.jump_r
            if self.facing_dir == Directions.RIGHT:
                frameX, frameY = self.jump_sprite

        #if tux is not jumping nor walking (he could be falling), render idle sprite
        if self.direction != Directions.RIGHT and self.direction != Directions.LEFT and self.direction != Directions.UP:
            #tux is idle
            self.walking_pointer = 0
            if self.facing_dir == Directions.LEFT:
                frameX, frameY = self.idle_r
            elif self.facing_dir == Directions.RIGHT:
                frameX, frameY = self.idle
        else:
            #tux is walking
            if self.direction == Directions.LEFT:
                frameX, frameY = self.walking_r[self.walking_pointer]
            elif self.direction == Directions.RIGHT:
                frameX, frameY = self.walking[self.walking_pointer]
            self.walking_pointer = (self.walking_pointer + 1) % len(self.walking)
        
        # Gravity
        self.calc_grav()
 
        # Move left/right
        self.rect.x += self.change_x
 
        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite
                self.rect.left = block.rect.right
 
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
            self.walking_pointer = 0
            if self.facing_dir == Directions.LEFT:
                frameX, frameY = self.idle_r
            elif self.facing_dir == Directions.RIGHT:
                frameX, frameY = self.idle

        self.image = self.sheet.image_at((frameX * CELL_SIZE, frameY * CELL_SIZE, CELL_SIZE, CELL_SIZE), colorkey=ALPHA)
        self.prev_body = x, y
        if self.direction == Directions.LEFT or self.direction == Directions.RIGHT:
            self.facing_dir = self.direction
 
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
        self.direction = Directions.UP
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


    # def go_left(self):
    #     """ Called when the user hits the left arrow. """
    #     self.change_x = -6
 
    # def go_right(self):
    #     """ Called when the user hits the right arrow. """
    #     self.change_x = 6
 
    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0

    def kill(self):
        logging.info("Agent died")
        self.dead = True