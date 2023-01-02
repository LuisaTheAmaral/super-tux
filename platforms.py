import pygame
from spritesheet import SpriteSheet
from common import ALPHA

class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """
 
    def __init__(self, sheets, width, height, x, y):
        super().__init__()
        
        x_cursor = 0
        y_cursor = 0
        
        self.image = pygame.Surface([width, height], pygame.SRCALPHA)
        self.image.set_colorkey(ALPHA, pygame.RLEACCEL)
        
        self.top_left_sheet = SpriteSheet(sheets[0]).sheet
        self.bottom_left_sheet = SpriteSheet(sheets[1]).sheet
        self.top_right_sheet = SpriteSheet(sheets[2]).sheet
        self.bottom_right_sheet = SpriteSheet(sheets[3]).sheet
        self.top_sheet = SpriteSheet(sheets[4]).sheet
        self.bottom_sheet = SpriteSheet(sheets[5]).sheet
        
        while ( y_cursor < height ):
            if y_cursor == 0: #snow
                self.image.blit( self.top_left_sheet, ( 0, y_cursor ) )
            else: #wall tile
                self.image.blit( self.bottom_left_sheet, ( 0, y_cursor ) )
            y_cursor += self.bottom_left_sheet.get_height()
            
        y_cursor = 0
        x_cursor = self.bottom_left_sheet.get_width()
        while ( y_cursor < height ):
            while ( x_cursor < width-self.top_right_sheet.get_width() ):
                if y_cursor == 0: #snow
                    self.image.blit( self.top_sheet, ( x_cursor, y_cursor ) )
                else: #wall tile
                    self.image.blit( self.bottom_sheet, ( x_cursor, y_cursor ) )
                x_cursor += self.bottom_sheet.get_width()
            y_cursor += self.bottom_sheet.get_height()
            x_cursor = self.bottom_left_sheet.get_width()
        
        y_cursor = 0
        x_cursor = width-self.bottom_right_sheet.get_width()
        while ( y_cursor < height ):
            if y_cursor == 0: #snow
                self.image.blit( self.top_right_sheet, ( x_cursor, y_cursor ) )
            else: #wall tile
                self.image.blit( self.bottom_right_sheet, ( x_cursor, y_cursor ) )
            y_cursor += self.bottom_right_sheet.get_height()
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class WoodPlatform(Platform):
    def __init__(self, width, height, x, y):
        sheets = [f"assets/blocks/wood_{x}.png" for x in range(1,7)]
        super().__init__(sheets, width, height, x, y)

class SnowPlatform(Platform):
    def __init__(self, width, height, x, y):
        sheets = [f"assets/blocks/snow_{x}.png" for x in range(1,7)]
        super().__init__(sheets, width, height, x, y)

class FlyingPlatform(pygame.sprite.Sprite):
    def __init__(self, x, y, y_min_limit, y_max_limit):
        super().__init__()
        self.sheets = [f"assets/flying_platform/flying_platform-{x}.png" for x in range(4)]
        self.sheet_pointer = 0

        self.y_min = y_min_limit
        self.y_max = y_max_limit
        
        self.image = pygame.Surface([128, 61], pygame.SRCALPHA)
        self.image.set_colorkey(ALPHA, pygame.RLEACCEL)
        
        self.sheet = SpriteSheet(self.sheets[self.sheet_pointer]).sheet
        self.image.blit( self.sheet, ( 0, 0 ) )
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = 1


    def update(self):
        self.image.fill("white")
        self.image.set_colorkey("white")

        self.sheet_pointer = (self.sheet_pointer + 0.20) % 3
        self.sheet = SpriteSheet(self.sheets[int(self.sheet_pointer)]).sheet
        self.image.blit( self.sheet, ( 0, 0 ) )
        if self.rect.y == self.y_max:
            self.direction = -1
        elif self.rect.y == self.y_min:
            self.direction = 1
        self.rect.y += self.direction 
