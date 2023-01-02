import pygame
from spritesheet import SpriteSheet
from common import ALPHA

class Coin(pygame.sprite.Sprite):

    def __init__(self, x, y) -> None:
        super().__init__()
        self.sheets = [f"assets/coin/coin-{x}.png" for x in range(0, 16)]
        self.image = pygame.Surface([32, 32], pygame.SRCALPHA)
        self.image.set_colorkey(ALPHA, pygame.RLEACCEL)
        self.sheet_pointer = 0
        self.sheet = SpriteSheet(self.sheets[self.sheet_pointer]).sheet
        self.image.blit( self.sheet, ( 0, 0 ) )
        
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.image.fill("white")
        self.image.set_colorkey("white")
        self.sheet_pointer = (self.sheet_pointer + 0.20) % 15
        self.sheet = SpriteSheet(self.sheets[int(self.sheet_pointer)]).sheet
        self.image.blit( self.sheet, ( 0, 0 ) )
