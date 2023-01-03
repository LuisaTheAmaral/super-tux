import pygame
from spritesheet import SpriteSheet
from common import ALPHA, Directions

# Global constants
CELL_SIZE = 32

class BonusBlock(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()
        self.sprites = [f"assets/bonus_block/full-{i}.png" for i in range (0,5)]
        self.empty_sheet = SpriteSheet("assets/bonus_block/empty.png").sheet
        self.sheet_pointer = 0
        self.image = pygame.Surface([CELL_SIZE, CELL_SIZE], pygame.SRCALPHA)
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
            if isinstance(self, EggBlock):
                self.egg.show()
            self.image.blit( self.empty_sheet, ( 0, 0 ) )
            return True
        return False

class EggBlock(BonusBlock):
    def __init__(self, x, y, egg) -> None:
        super().__init__(x, y)
        self.egg = egg
        self.active_sprite_list = pygame.sprite.Group()
        self.active_sprite_list.add(self.egg)

    def update(self):        
        if self.broken == True and self.egg.show_egg:
            self.egg.move(Directions.LEFT, 1)
        super().update()
        
class CoinBlock(BonusBlock):
    def __init__(self, x, y) -> None:
        super().__init__(x, y)


class Egg(pygame.sprite.Sprite):
    def __init__(self, x, y, height) -> None:
        super().__init__()
        self.sheet = SpriteSheet("assets/bonus_block/egg.png").sheet
        self.image = pygame.Surface([CELL_SIZE, CELL_SIZE], pygame.SRCALPHA)
        self.image.set_colorkey(ALPHA, pygame.RLEACCEL)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y - CELL_SIZE)
        
        self.change_x = 0
        self.change_y = 0
        self.height = height
        
        self.show_egg = False
        self.platforms = None

    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35

        # Deactivate power if it falls
        if self.rect.y >= self.height and self.change_y >= 0:
            self.deactivate()

    def update(self):
        self.image.fill("white")
        self.image.set_colorkey("white")
        if self.show_egg:
            self.calc_grav()
            self.collisions()
            self.image.blit( self.sheet, ( 0, 0 ) )

    def collisions(self):
        self.rect.x += self.change_x
        block_hit_list = pygame.sprite.spritecollide(self, self.platforms, False)
        for block in block_hit_list:
            # If moving right, set right side to the left side of the collided item
            if self.change_x > 0:
                self.rect.right = block.rect.left
                    
            elif self.change_x < 0:
                # Otherwise if moving left, do the opposite
                self.rect.left = block.rect.right
 
        # Move up/down
        self.rect.y += self.change_y

        block_hit_list = pygame.sprite.spritecollide(self, self.platforms, False)
        for block in block_hit_list:
 
            # Reset position based on the top/bottom of the object
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
 
            # Stop vertical movement
            self.change_y = 0       

    def show(self):
        self.show_egg = True

    def deactivate(self):
        self.show_egg = False

    def set_platforms(self, platforms):
        self.platforms = platforms

    def move(self, direction, change_x):
        """ Move agent. """
        self.direction = direction
        if direction == Directions.LEFT:
            self.change_x = change_x*-1
        elif direction == Directions.RIGHT:
            self.change_x = change_x
        
