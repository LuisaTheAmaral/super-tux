import pygame
from spritesheet import SpriteSheet
from common import ALPHA

GOAL_WIDTH = 32
N = 7
GOAL_HEIGHT = 32 * N

HOME_WIDTH = 353
HOME_HEIGHT = 195

class Goal(pygame.sprite.Sprite):

    def __init__(self, x, y, scale) -> None:
        super().__init__()

        self.image = pygame.Surface([GOAL_WIDTH, GOAL_HEIGHT], pygame.SRCALPHA)
        self.image.set_colorkey(ALPHA, pygame.RLEACCEL)
        self.top_sheet = SpriteSheet("assets/goal/goal2-4.png").sheet
        self.bottom_sheet = SpriteSheet("assets/goal/goal1-4.png").sheet
        self.image.blit( self.top_sheet, ( 0, 0 ) )
        
        for i in range(GOAL_WIDTH, GOAL_HEIGHT+1, GOAL_WIDTH):
            self.image.blit( self.bottom_sheet, ( 0, i ) )

        self.rect = self.image.get_rect()
        self.rect.x = x*scale
        self.rect.y = y*scale - GOAL_HEIGHT + scale

class Home(pygame.sprite.Sprite):
    
    def __init__(self, x, y, scale) -> None:
        super().__init__()

        self.image = pygame.Surface([HOME_WIDTH, HOME_HEIGHT], pygame.SRCALPHA)
        self.image.set_colorkey(ALPHA, pygame.RLEACCEL)
        self.left_sheet = SpriteSheet("assets/goal/exitbg.png").sheet
        self.right_sheet = SpriteSheet("assets/goal/exitfg.png").sheet
        self.image.blit( self.left_sheet, ( 0, 0 ) )
        self.image.blit( self.right_sheet, ( 95, 0 ) )

        self.rect = self.image.get_rect()
        self.rect.x = x*scale
        self.rect.y = y*scale - HOME_HEIGHT + scale