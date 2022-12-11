import pygame
from agent import Agent
from spritesheet import SpriteSheet
from common import Directions
from pygame.locals import *
from spritesheet import SpriteSheet

CELL_SIZE = 50
ALPHA = (0, 255, 0)

class AgentSprite(pygame.sprite.Sprite):
    def __init__(self, agent: Agent, WIDTH, HEIGHT, SCALE, platforms):
        super().__init__()

        self.sheet = SpriteSheet("sprites/spritesheet_full.png")
        self.SCALE = SCALE
        self.agent = agent
        self.prev_body = self.agent.body
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
        self.idle = [(0,0)]
        self.walking_pointer = 0
        self.idle_pointer = 0
        self.idle_r = [(0,3)]

        self.prev_dir = Directions.RIGHT # starts facing right
        frameX, frameY = self.idle_r[self.idle_pointer]
        self.image = self.sheet.image_at((frameX * CELL_SIZE, frameY * CELL_SIZE, CELL_SIZE, CELL_SIZE), colorkey=ALPHA)
        self.rect = self.image.get_rect()
        self.platforms = platforms
        self.HEIGHT = HEIGHT*SCALE
        self.WIDTH = WIDTH*SCALE
        self.change_y = 0
        self.update()


    def update(self):
        # Render tux
        # self.calc_grav()

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
        x, y = self.agent.body

        # print(self.prev_body)
        # print(self.agent.body)
        # print(self.change_y)
        # print("-----")
        # y += self.change_y #force gravity
        

        dir, dir_body = get_direction(x, y, prev_x, prev_y)

        if dir == None or dir == Directions.DOWN:
            #tux is idle
            self.walking_pointer = 0
            if dir_body == Directions.LEFT:
                frameX, frameY = self.idle_r[self.idle_pointer]
            elif dir_body == Directions.RIGHT:
                frameX, frameY = self.idle[self.idle_pointer]
            self.idle_pointer = (self.idle_pointer + 1) % len(self.idle)
        else:
            #tux is walking
            self.idle_pointer = 0
            if dir_body == Directions.LEFT:
                frameX, frameY = self.walking_r[self.walking_pointer]
            elif dir_body == Directions.RIGHT:
                frameX, frameY = self.walking[self.walking_pointer]
            self.walking_pointer = (self.walking_pointer + 1) % len(self.walking)
        

        self.image = self.sheet.image_at((frameX * CELL_SIZE, frameY * CELL_SIZE, CELL_SIZE, CELL_SIZE), colorkey=ALPHA)
        self.rect.x = self.SCALE * prev_x
        self.rect.y = self.SCALE * prev_y
        self.prev_body = x, y
        self.prev_dir = dir_body

    def calc_grav(self):
        """ Calculate effect of gravity. """
        # See if we are on the ground.
        if self.rect.y >= self.HEIGHT - 100 and self.change_y >= 0:
            self.change_y = 0
        else:
            self.change_y += .35
            # self.agent.body = (self.agent.body[0], self.HEIGHT - 100)

    def check_collisions(self, obstacle):
        collisions = [False]*9
        collisions[0] = self.rect.collidepoint(obstacle.rect.topleft)
        collisions[1] = self.rect.collidepoint(obstacle.rect.topright)
        collisions[2] = self.rect.collidepoint(obstacle.rect.bottomleft)
        collisions[3] = self.rect.collidepoint(obstacle.rect.bottomright)

        collisions[4] = self.rect.collidepoint(obstacle.rect.midleft)
        collisions[5] = self.rect.collidepoint(obstacle.rect.midright)
        collisions[6] = self.rect.collidepoint(obstacle.rect.midtop)
        collisions[7] = self.rect.collidepoint(obstacle.rect.midbottom)

        collisions[8] = self.rect.collidepoint(obstacle.rect.center)

        # if collisions[0] or collisions[2] or collisions[4]:
        #     print("left")
        #     self.rect.x += obstacle.platform_vel

        if collisions[1] or collisions[3] or collisions[5]:
            print("right")
            #self.prev_body = (self.prev_body[0] + obstacle.platform_vel, self.prev_body[1])

        if collisions[0] or collisions[1] or collisions[6]:
            print("top")
            self.rect.bottom = obstacle.rect.top

        # if collisions[2] or collisions[3] or collisions[7]:
        #     print("bottom")

        # if collisions[8]:
        #     print("center")
    
    
# x location, y location, img width, img height, img file
class Platform(pygame.sprite.Sprite):
    def __init__(self, xloc, yloc, width, height): #xloc, yloc, imgw, imgh, img,
        pygame.sprite.Sprite.__init__(self)
        self.width = width
        self.height = height
        self.sheet = SpriteSheet("assets/blocks/block_horiz.png")
        self.image = pygame.Surface([width, height], pygame.SRCALPHA)
        self.image.set_colorkey(ALPHA, pygame.RLEACCEL)
        #self.image = pygame.transform.scale(self.sheet.sheet, (width*2, height*2))
        #self.image.blit(self.sheet.sheet, (0, 0))

        x_cursor = 0
        y_cursor = 0
        while ( y_cursor < height ):
            while ( x_cursor < width ):
                self.image.blit( self.sheet.sheet, ( x_cursor, y_cursor ) )
                x_cursor += self.sheet.sheet.get_width()
            y_cursor += self.sheet.sheet.get_height()
            x_cursor = 0

        #self.image = self.sheet.image_at((0, 0, self.width, self.height), colorkey=ALPHA)
        
        # width = self.image.get_rect().width
        # height = self.image.get_rect().height
        # self.image = pygame.transform.scale(self.sheet.sheet, (width*2, height*2))
        #self.rect = self.image.get_rect()
        #self.rect.y = yloc
        #self.rect.x = xloc
        # Starting coordinates of the platform
        x = 100
        y = 150
        
        # Creating a rect with width and height
        
        # self.rect = Rect(xloc, yloc, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = xloc
        self.rect.y = yloc
        

    def update(self):
        pass
        # pygame.draw.rect(self.image, (255, 0, 0), self.rect)

class FloatingPlatform(Platform):
    def __init__(self):
        super().__init__()
        self.platform_vel = 5

    def update(self):
        # Multiplying platform_vel with -1
        # if its x coordinate is less then 100
        # or greater than or equal to 300.
        if self.rect.left >=600 or self.rect.left<100:
            self.platform_vel*= -1
    
        # Adding platform_vel to x
        # coordinate of our rect
        self.rect.left += self.platform_vel
        # pygame.draw.rect(self.image, (255, 0, 0), self.rect)