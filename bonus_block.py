import pygame
from spritesheet import SpriteSheet
from common import ALPHA

class BonusBlock(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()
        self.sprites = [f"assets/bonus_block/full-{i}.png" for i in range (0,5)]
        self.empty_sheet = SpriteSheet("assets/bonus_block/empty.png").sheet
        self.sheet_pointer = 0
        self.image = pygame.Surface([32, 32], pygame.SRCALPHA)
        self.image.set_colorkey(ALPHA, pygame.RLEACCEL)
        
        self.sheet = SpriteSheet(self.sprites[self.sheet_pointer]).sheet
        self.image.blit( self.sheet, ( 0, 0 ) )
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)  
        self.broken = False

    def update(self):
        self.image.fill("white")
        self.image.set_colorkey("white")
        if self.broken == True:
            self.image.blit( self.empty_sheet, ( 0, 0 ) )
        else:
            self.sheet_pointer = (self.sheet_pointer + 0.1) % 3
            self.sheet = SpriteSheet(self.sprites[int(self.sheet_pointer)]).sheet
            self.image.blit( self.sheet, ( 0, 0 ) )

    def break_block(self):
        if not self.broken:
            self.broken = True
            self.image.blit( self.empty_sheet, ( 0, 0 ) )
            return True
        return False

class EggBlock(BonusBlock):
    def __init__(self, x, y) -> None:
        super().__init__(x, y)
        
class CoinBlock(BonusBlock):
    def __init__(self, x, y) -> None:
        super().__init__(x, y)