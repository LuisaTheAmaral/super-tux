import pygame
from spritesheet import SpriteSheet
from common import ALPHA

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