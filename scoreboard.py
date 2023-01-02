import pygame
from spritesheet import SpriteSheet
from common import CATCH_COIN, ENEMY_KILLED

YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

class Scoreboard(pygame.sprite.Sprite):

    def __init__(self, screen_width, player):
        super().__init__()   
        
        self.scores = {}
        self.scores["points"] = 0
        self.scores["enemies"] = 0
        player.register(CATCH_COIN, self.increase_points)
        player.register(ENEMY_KILLED, self.increase_kill_count)

        self.image = pygame.Surface([120, 30], pygame.SRCALPHA)
        self.font = pygame.font.Font('assets/SuperTux-Medium.ttf', 16)
        self.shadow_offset = 2
                
        self.rect = self.image.get_rect()
        self.rect.x = screen_width - 185 #temp
        self.rect.y = 15

    def increase_points(self):
        self.scores["points"] += 1

    def increase_kill_count(self):
        self.scores["enemies"] += 1

    def update(self):
        self.image.fill("blue")
        self.image.set_colorkey("blue")

        sheet = SpriteSheet("assets/coin/coin-0.png").sheet
        scaled = pygame.transform.scale(sheet, (15, 15))
        self.image.blit(scaled, (0, 0))
        
        msg = f'x {self.scores["points"]} x {self.scores["enemies"]}'
        text = self.font.render(msg, True, YELLOW)
        shadow = self.font.render(msg, True, BLACK)
        self.image.blit(shadow, (20+self.shadow_offset, 0+self.shadow_offset))
        self.image.blit(text, (20, 0))
        