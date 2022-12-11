import pygame
from agent import Agent
from spritesheet import SpriteSheet
from common import Directions
from pygame.locals import *
from spritesheet import SpriteSheet
import math

# Global constants
CELL_SIZE = 50
ALPHA = (0, 255, 0)
 
class Agent(pygame.sprite.Sprite):
    def __init__(self, width, height, scale):
        super().__init__()

        self.sheet = SpriteSheet("sprites/spritesheet_full.png")
        self.SCALE = scale
        
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
        self.idle = (0,0)
        self.idle_r = (0,3)
        self.walking_pointer = 0
        
        self.prev_dir = Directions.RIGHT # starts facing right
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
 
    def update(self):

        def get_direction(x, y, prev_x, prev_y):
            """given 2 coordinates returns direction taken."""
            dir = None
            if x - prev_x > 0:
                return Directions.RIGHT, Directions.RIGHT
            elif x - prev_x < 0:
                return Directions.LEFT, Directions.LEFT
            elif y - prev_y > 0:
                dir = Directions.DOWN
            elif y - prev_y < 0:
                dir = Directions.UP
            return dir, self.prev_dir

        # Get body
        prev_x, prev_y = self.prev_body
        x, y = self.rect.x, self.rect.y
        dir, dir_body = get_direction(x, y, prev_x, prev_y)

        if dir == None or dir == Directions.DOWN:
            #tux is idle
            self.walking_pointer = 0
            if dir_body == Directions.LEFT:
                frameX, frameY = self.idle_r
            elif dir_body == Directions.RIGHT:
                frameX, frameY = self.idle
        else:
            #tux is walking
            if dir_body == Directions.LEFT:
                frameX, frameY = self.walking_r[self.walking_pointer]
            elif dir_body == Directions.RIGHT:
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

        self.image = self.sheet.image_at((frameX * CELL_SIZE, frameY * CELL_SIZE, CELL_SIZE, CELL_SIZE), colorkey=ALPHA)
        self.prev_body = x, y
 
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
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = -6
 
    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = 6
 
    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0
 
 
class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """
 
    def __init__(self, width, height, x, y):
        super().__init__()
        self.sheet = SpriteSheet("assets/blocks/block_horiz.png")
        self.image = pygame.Surface([width, height], pygame.SRCALPHA)
        self.image.set_colorkey(ALPHA, pygame.RLEACCEL)
        self.image.blit(self.sheet.sheet, (0,0))
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y 
 
class Level():
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """
 
    def __init__(self, player):
        """ Constructor. Pass in a handle to player. Needed for when moving
            platforms collide with the player. """
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player
 
        # How far this world has been scrolled left/right
        self.world_shift = 0
 
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()
        self.enemy_list.update()
 
    def draw(self, screen):
        """ Draw everything on this level. """ 
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
 
    def shift_world(self, shift_x):
        """ When the user moves left/right and we need to scroll
        everything: """
 
        # Keep track of the shift amount
        self.world_shift += shift_x
 
        # Go through all the sprite lists and shift
        for platform in self.platform_list:
            platform.rect.x += shift_x
 
        for enemy in self.enemy_list:
            enemy.rect.x += shift_x
 
 
# Create platforms for the level
class Level_01(Level):
    """ Definition for level 1. """
 
    def __init__(self, player):
        """ Create level 1. """
 
        # Call the parent constructor
        Level.__init__(self, player)
 
        self.level_limit = -1000
 
        # Array with width, height, x, and y of platform
        level = [[96, 32, 500, 500],
                 [96, 32, 800, 400],
                 [96, 32, 1000, 500],
                 [96, 32, 1120, 280],
                 ]
 
        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1], platform[2], platform[3])
            # block.rect.x = platform[2]
            # block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)
 
 
# Create platforms for the level
# class Level_02(Level):
#     """ Definition for level 2. """
 
#     def __init__(self, player):
#         """ Create level 1. """
 
#         # Call the parent constructor
#         Level.__init__(self, player)
 
#         self.level_limit = -1000
 
#         # Array with type of platform, and x, y location of the platform.
#         level = [[210, 30, 450, 570],
#                  [210, 30, 850, 420],
#                  [210, 30, 1000, 520],
#                  [210, 30, 1120, 280],
#                  ]
 
#         # Go through the array above and add platforms
#         for platform in level:
#             block = Platform(platform[0], platform[1])
#             block.rect.x = platform[2]
#             block.rect.y = platform[3]
#             block.player = self.player
#             self.platform_list.add(block)
 
 
def main(width, height, scale):
    """ Main Program """
    pygame.init()

    SCREEN_WIDTH = width*scale
    SCREEN_HEIGHT = height*scale
 
    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    # background scroll setup
    bg = pygame.image.load("assets/arctis.jpg").convert()
    bg_width = bg.get_width()
    scroll = 0
    tiles= math.ceil(width / bg_width) + 1
 
    pygame.display.set_caption("Tux")
 
    # Create the player
    player = Agent(width, height, scale)
 
    # Create all the levels
    level_list = []
    level_list.append(Level_01(player))
    # level_list.append(Level_02(player))
 
    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]
 
    active_sprite_list = pygame.sprite.Group()
    player.level = current_level
 
    active_sprite_list.add(player)
 
    # Loop until the user clicks the close button.
    done = False
 
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
 
    # -------- Main Program Loop -----------
    while not done:
        # fill background with image
        for i in range( 0, tiles):
            screen.blit(bg, (i*bg_width+scroll,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.jump()
 
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()
 
        # Update the player
        active_sprite_list.update()
 
        # Update items in the level
        current_level.update()
 
        # If the player gets near the right side, shift the world left (-x)
        if player.rect.right >= 500:
            diff = player.rect.right - 500
            player.rect.right = 500
            current_level.shift_world(-diff)
 
        # If the player gets near the left side, shift the world right (+x)
        if player.rect.left <= 120:
            diff = 120 - player.rect.left
            player.rect.left = 120
            current_level.shift_world(diff)
 
        # If the player gets to the end of the level, go to the next level
        current_position = player.rect.x + current_level.world_shift
        if current_position < current_level.level_limit:
            player.rect.x = 120
            if current_level_no < len(level_list)-1:
                current_level_no += 1
                current_level = level_list[current_level_no]
                player.level = current_level
 
        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        current_level.draw(screen)
        active_sprite_list.draw(screen)
 
        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
 
        # Limit to 60 frames per second
        clock.tick(60)
 
        # update the screen
        pygame.display.flip()
 
    pygame.quit()
 
if __name__ == "__main__":
    main(60, 30, 20)