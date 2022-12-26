import pygame
from spritesheet import SpriteSheet
from common import ALPHA

class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """
 
    def __init__(self, sheet, width, height, x, y):
        super().__init__()
        self.sheet = sheet
        self.image = pygame.Surface([width, height], pygame.SRCALPHA)
        self.image.set_colorkey(ALPHA, pygame.RLEACCEL)

        #scaled = pygame.transform.scale(self.image, (1500, 1500))
        self.image.blit(self.sheet.sheet, (0,0))
        self.rect = self.image.get_rect()
        
        self.rect.x = x
        self.rect.y = y 

class WoodPlatform(Platform):
    def __init__(self, width, height, x, y):
        super().__init__(SpriteSheet("assets/blocks/block_horiz.png"), 96, 32, x, y)

class SnowPlatform(pygame.sprite.Sprite):
    
    def __init__(self, width, height, x, y):
        super().__init__()
        
        x_cursor = 0
        y_cursor = 0
        
        self.image = pygame.Surface([width, height], pygame.SRCALPHA)
        self.image.set_colorkey(ALPHA, pygame.RLEACCEL)
        
        self.sheet1 = SpriteSheet("assets/snow_block_1.png").sheet
        self.sheet2 = SpriteSheet("assets/snow_block_2.png").sheet
        self.sheet3 = SpriteSheet("assets/snow_block_3.png").sheet
        self.sheet1_snow = SpriteSheet("assets/snow_block_4.png").sheet
        self.sheet2_snow = SpriteSheet("assets/snow_block_5.png").sheet
        self.sheet3_snow = SpriteSheet("assets/snow_block_6.png").sheet
        
        while ( y_cursor < height ):
            if y_cursor == 0: #snow
                self.image.blit( self.sheet1_snow, ( 0, y_cursor ) )
            else: #wall tile
                self.image.blit( self.sheet1, ( 0, y_cursor ) )
            y_cursor += self.sheet1.get_height()
            
        y_cursor = 0
        x_cursor = self.sheet1.get_width()
        while ( y_cursor < height ):
            while ( x_cursor < width-self.sheet3.get_width() ):
                if y_cursor == 0: #snow
                    self.image.blit( self.sheet2_snow, ( x_cursor, y_cursor ) )
                else: #wall tile
                    self.image.blit( self.sheet2, ( x_cursor, y_cursor ) )
                x_cursor += self.sheet2.get_width()
            y_cursor += self.sheet2.get_height()
            x_cursor = self.sheet1.get_width()
        
        y_cursor = 0
        x_cursor = width-self.sheet3.get_width()
        while ( y_cursor < height ):
            if y_cursor == 0: #snow
                self.image.blit( self.sheet3_snow, ( x_cursor, y_cursor ) )
            else: #wall tile
                self.image.blit( self.sheet3, ( x_cursor, y_cursor ) )
            y_cursor += self.sheet3.get_height()
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 
