import pygame
from platforms import SnowPlatform, WoodPlatform
from PIL import Image
from tiles import Tiles

class Level():

    def __init__(self, filename, scale=20) -> None:
        self.filename = filename
        self.scale = scale
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.level_limit = -1000
        self.player_start_position = (0, 0)

        # How far this world has been scrolled left/right
        self.world_shift = 0
        self.coords = []

        self.parse_level_file()

    def parse_level_file(self):
        img = Image.open(self.filename)
        pixels = img.load() 
        width, height = img.size
        snow_platforms = []
        wood_platforms = []

        for y in range(height):      
            for x in range(width):   
                r, g, b, a = pixels[x, y]
                hex_code = f"{r:02x}{g:02x}{b:02x}"
                coords = (x, y)

                if hex_code == Tiles.SNOW_WALL.value:
                    snow_platforms.append(coords)
                elif hex_code == Tiles.WOOD_TILE.value:
                    wood_platforms.append(coords)
                elif hex_code == Tiles.TUX.value:
                    self.player_start_position = (x, y)

        def _get_platform_details(group):
            x, y = min(group)
            max_coords = max(group)
            width, height = max_coords[0] - x+1, max_coords[1] - y+1
            return x, y, width, height

        def _define_platforms(platforms, type="snow"):
            groups = [] #list that will store list of points that belong to the same platform
            for i in range(len(platforms)):
                point = platforms[i]
                belong = False
                for group in groups:
                    if any(abs(g[0] - point[0]) + abs(g[1] - point[1]) == 1 for g in group):
                        group.append(point)
                        belong = True
                if not belong:
                    groups.append([point]) #create new list of points to store new platform

            for group in groups:
                x, y, width, height = _get_platform_details(group)
                if type == "wood":
                    self.platform_list.add(WoodPlatform(width*self.scale, height*self.scale, x*self.scale, y*self.scale))
                else:
                    self.platform_list.add(SnowPlatform(width*self.scale, height*self.scale, x*self.scale, y*self.scale))

        _define_platforms(snow_platforms, "snow")
        _define_platforms(wood_platforms, "wood")

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