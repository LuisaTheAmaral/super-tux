import pygame
from platforms import SnowPlatform, WoodPlatform, FlyingPlatform
from PIL import Image
from tiles import Tiles
from goal import Goal, Home
from coin import Coin
from bonus_block import EggBlock, CoinBlock, Egg
from monster import Spawner, Snowball, Spiky

class Level():

    def __init__(self, filename, height, scale=20) -> None:
        self.filename = filename
        self.scale = scale
        self.height = height
        
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.goal_list = pygame.sprite.Group()
        self.coin_list = pygame.sprite.Group()
        self.blocks_list = pygame.sprite.Group()
        self.powers = pygame.sprite.Group()
        
        self.player_start_position = (0, 0)

        # How far this world has been scrolled left/right
        self.world_shift = 0
        self.coords = []

        self.parse_level_file() #obtain level details from level byte map
        
    def add_enemy(self, enemy):
        self.enemy_list.add(enemy)
        enemy.level = self

    def parse_level_file(self):
        img = Image.open(self.filename)
        pixels = img.load() 
        width, height = img.size
        snow_platforms = []
        wood_platforms = []
        flying_platforms = []
        flying_platforms_limits = []
        bonus_blocks = []
        
        spawner = Spawner()
        snowball_prototype = Snowball(1, 1, width, height, self.scale) # temp location
        spiky_prototype = Spiky(1, 1, width, height, self.scale) # temp location

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
                elif hex_code == Tiles.SNOWBALL_FACED_RIGHT.value:
                    snowball = spawner.spawn_enemy(snowball_prototype, x, y-1.5, is_right=1)
                    self.add_enemy(snowball)
                elif hex_code == Tiles.SNOWBALL_FACED_LEFT.value:
                    snowball = spawner.spawn_enemy(snowball_prototype, x, y-1.5, is_right=0)
                    self.add_enemy(snowball)
                elif hex_code == Tiles.SPIKY_FACED_RIGHT.value:
                    spiky = spawner.spawn_enemy(spiky_prototype, x, y-1.5, is_right=1)
                    self.add_enemy(spiky)
                elif hex_code == Tiles.SPIKY_FACED_LEFT.value:
                    spiky = spawner.spawn_enemy(spiky_prototype, x, y-1.5, is_right=0)
                    self.add_enemy(spiky)
                elif hex_code == Tiles.GOAL.value:
                    self.goal_list.add(Goal(x, y, self.scale))
                elif hex_code == Tiles.HOME.value:
                    self.goal_list.add(Home(x, y, self.scale))
                elif hex_code == Tiles.FLYING_PLATFORM.value:
                    flying_platforms.append(coords)
                elif hex_code == Tiles.FLYING_PLATFORM_LIMIT.value:
                    flying_platforms_limits.append(coords)
                elif hex_code == Tiles.COIN.value:
                    self.coin_list.add(Coin(x*self.scale, y*self.scale))
                elif hex_code == Tiles.COIN_BLOCK.value:
                    bonus_blocks.append(CoinBlock(x*self.scale, y*self.scale))
                elif hex_code == Tiles.EGG_BLOCK.value:
                    egg = Egg(x*self.scale, y*self.scale, self.height*self.scale)
                    egg_block = EggBlock(x*self.scale, y*self.scale, egg)
                    bonus_blocks.append(egg_block)
                    self.powers.add(egg_block.egg)
                    

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

        def _define_flying_platforms(flying_platforms, flying_platforms_limits):
            coords = []
            for p in flying_platforms:
                coords.append(p)
                for pl in flying_platforms_limits:
                    if p[0] == pl[0]:
                        coords.append(pl[1])
                x, y = coords[0]
                limits = coords[1], coords[2]
                self.platform_list.add(FlyingPlatform(x*self.scale, y*self.scale, min(limits)*self.scale, max(limits)*self.scale))
                coords = []

        _define_platforms(snow_platforms, "snow")
        _define_platforms(wood_platforms, "wood")
        for block in bonus_blocks:
            self.platform_list.add(block)
        _define_flying_platforms(flying_platforms, flying_platforms_limits)

        #egg needs to know where the platforms are to detect collisions
        for egg in self.powers:
            egg.set_platforms(self.platform_list)

    def update(self):
        """ Update everything in this level."""
        self.coin_list.update()
        self.platform_list.update()
        self.goal_list.update()
        self.blocks_list.update()
        self.powers.update()
        self.enemy_list.update()
        
    def send_enemy_commands(self):
        """ Send command to all enemies."""
        for enemy in self.enemy_list:
            enemy.commands(enemy.dead)
            
    def kill_enemy(self, enemy):
        """ Kill enemy."""
        enemy.commands(True)
 
    def draw(self, screen):
        """ Draw everything on this level. """ 
        self.coin_list.draw(screen)
        self.platform_list.draw(screen)
        self.goal_list.draw(screen)
        self.blocks_list.draw(screen)
        self.powers.draw(screen)
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

        for goal in self.goal_list:
            goal.rect.x += shift_x

        for coin in self.coin_list:
            coin.rect.x += shift_x

        for block in self.blocks_list:
            block.rect.x += shift_x

        for block in self.powers:
            block.rect.x += shift_x