import pygame
from agent import Agent
from spritesheet import SpriteSheet
from common import Directions

CELL_SIZE = 50
BLACK = (0, 0, 0)

class AgentSprite(pygame.sprite.Sprite):
    def __init__(self, agent: Agent, sprite_sheet, WIDTH, HEIGHT, SCALE):
        super().__init__()

        self.sheet = sprite_sheet
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
        self.walking_pointer = 0
        # self.idle = [(0,0), #idle-0
        #             (1,0)] #idle-1
        self.idle = [(0,0)]
        self.idle_pointer = 0

        self.image = pygame.Surface([WIDTH * SCALE, HEIGHT * SCALE])
        self.update()
        self.rect = self.image.get_rect()

    def update(self):
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        # Render tux

        def get_direction(x, y, prev_x, prev_y):
            """given 2 coordinates returns direction taken."""
            dir = None
            if x - prev_x > 0:
                dir = Directions.RIGHT
            elif x - prev_x < 0:
                dir = Directions.LEFT
            elif y - prev_y > 0:
                dir = Directions.DOWN
            elif y - prev_y < 0:
                dir = Directions.UP
            return dir

        # Get body
        prev_x, prev_y = self.prev_body
        x, y = self.agent.body

        dir = get_direction(x, y, prev_x, prev_y)
        if dir == None:
            #tux is idle
            self.walking_pointer = 0
            frameX, frameY = self.idle[self.idle_pointer]
            self.idle_pointer = (self.idle_pointer + 1) % len(self.idle)
        else:
            #tux is walking
            self.idle_pointer = 0
            frameX, frameY = self.walking[self.walking_pointer]
            self.walking_pointer = (self.walking_pointer + 1) % len(self.walking)

        self.image.blit(self.sheet, (self.SCALE * prev_x, self.SCALE * prev_y), ((frameX*CELL_SIZE), (frameY*CELL_SIZE), CELL_SIZE, CELL_SIZE ))
            
        self.prev_body = x, y
        prev_dir = dir #not being used yet
    
    
    