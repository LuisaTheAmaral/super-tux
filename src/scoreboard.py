import pygame
from spritesheet import SpriteSheet
from common import CATCH_COIN, ENEMY_KILLED, YELLOW, BLACK

TEXT_HEIGHT = 15
class Scoreboard(pygame.sprite.Sprite):

    def __init__(self, screen_width, player):
        super().__init__()   
        
        self.scores = {}
        self.scores["points"] = 0
        self.scores["enemies"] = 0
        player.register(CATCH_COIN, self.increase_points)
        player.register(ENEMY_KILLED, self.increase_kill_count)

        self.image = pygame.Surface([120, 40], pygame.SRCALPHA)
        self.font = pygame.font.Font('assets/SuperTux-Medium.ttf', 16)
        self.shadow_offset = 2
                
        self.rect = self.image.get_rect()
        self.rect.x = screen_width - 85 #temp
        self.rect.y = 15

    def increase_points(self):
        self.scores["points"] += 1

    def increase_kill_count(self):
        self.scores["enemies"] += 1

    def show_score(self, score, img, y=0):
        
        #blit icon of score
        sheet = SpriteSheet(img).sheet
        scaled = pygame.transform.scale(sheet, (TEXT_HEIGHT, TEXT_HEIGHT))
        self.image.blit(scaled, (0, y))

        #blit score
        msg = f'x {score}'
        text = self.font.render(msg, True, YELLOW)
        shadow = self.font.render(msg, True, BLACK)
        self.image.blit(shadow, ((TEXT_HEIGHT + 5) + self.shadow_offset, y + self.shadow_offset))
        self.image.blit(text, ((TEXT_HEIGHT + 5), y))

    def update(self):
        self.image.fill("blue")
        self.image.set_colorkey("blue")
        self.show_score(self.scores["points"], "assets/scoreboard/coin.png")
        self.show_score(self.scores["enemies"], "assets/scoreboard/enemy.png", y=20)
        