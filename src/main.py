import pygame
import math
import os
from pygame.locals import *
from level import Level 
from tux import Tux, ENEMY_KILLED, TUX_DEAD
from scoreboard import Scoreboard
from common import YELLOW, BLACK
 
def main(width, height, scale):
    """ Main Program """
    pygame.init()
    command_log = []

    SCREEN_WIDTH = width*scale
    SCREEN_HEIGHT = height*scale
 
    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    # background scroll setup
    bg = pygame.image.load("assets/arctis.jpg").convert()
    bg_width = bg.get_width()
    scroll = 0
    tiles= math.ceil(width / bg_width) + 1
 
    pygame.display.set_caption("Tux")
 
    # Create all the levels
    levels_folder_path = "assets/levels/"
    level_list = []
    level_files = os.listdir(levels_folder_path)
    level_files.sort()
    for level in level_files:
        if level.endswith(".png"):
            level_list.append(Level(f"{levels_folder_path}/{level}", height=height, scale=scale))
 
    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]

    # Create the player
    x, y = current_level.player_start_position
    player = Tux("Tux", x, y, width, height, scale)
    player.controls(pygame.K_SPACE, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_g)

    scoreboard = Scoreboard(SCREEN_WIDTH, player)
    
    active_sprite_list = pygame.sprite.Group()
    player.level = current_level
 
    active_sprite_list.add(player)
    active_sprite_list.add(scoreboard)
 
    # flag to control game loop
    done = False
 
    clock = pygame.time.Clock()
    
    while not done:
        # fill background with image
        for i in range( 0, tiles):
            screen.blit(bg, (i*bg_width+scroll,0))

        for event in pygame.event.get():
            # if tux is dead then end game
            if event.type == pygame.QUIT or event.type == TUX_DEAD:
                done = True
              
            # enemy has been killed  
            if event.type == ENEMY_KILLED:
                event_enemy = event.__dict__["enemy"]
                current_level.kill_enemy(event_enemy)
                    
            # user presses a key
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_SPACE):
                    cmd = player.commands(event.key)
                    if cmd:
                        command_log.append(cmd)
            
            # when key is released tux stops walking
            if event.type == pygame.KEYUP:
                if (event.key == pygame.K_LEFT and player.change_x < 0) or (event.key == pygame.K_RIGHT and player.change_x > 0):
                    cmd = player.commands(None)
                    if cmd:
                        command_log.append(cmd)
        
        # send command to enemies
        current_level.send_enemy_commands()
        
        # Update the player
        active_sprite_list.update()
 
        # Update items in the level
        current_level.update()
 
        # If the player gets near the right side, shift the world left (-x)
        if player.rect.right >= 500:
            diff = player.rect.right - 500
            player.rect.right = 500
            current_level.shift_world(-diff)
 
        # If the player gets near the left side, shift the world right (+x)
        if player.rect.left <= 120:
            diff = 120 - player.rect.left
            player.rect.left = 120
            current_level.shift_world(diff)   

        # If player collides with egg power, player should grow
        block_hit_list = pygame.sprite.spritecollide(player, current_level.powers, False)
        for power in block_hit_list:
            power.deactivate()
            current_level.powers.remove(power)
            player.grow_toggle()  
 
        # If the player gets to the goal of the level, go to the next level
        block_hit_list = pygame.sprite.spritecollide(player, current_level.goal_list, False)
        if block_hit_list:
            msg = f"LEVEL {current_level_no+1} COMPLETED. PRESS ENTER TO CONTINUE"
            command_log.append(f"LEVEL {current_level_no+1} COMPLETED")
            if current_level_no == len(level_list) - 1:
                player.kill()
                done = True
                msg = f"LEVEL {current_level_no+1} COMPLETED. GAME FINISHED"
                command_log.append(f"GAME COMPLETED")
            player.stop()

            #show continue screen
            screen.fill("white")
            for i in range( 0, tiles):
                screen.blit(bg, (i*bg_width+scroll,0))
            
            font = pygame.font.Font('assets/SuperTux-Medium.ttf', 32)
            shadow_offset = 2
                    
            text = font.render(msg, True, YELLOW)
            textRect = text.get_rect()
            textRect.center = (width*scale // 2, height*scale // 4)
            
            shadow = font.render(msg, True, BLACK)
            shadowRect = shadow.get_rect()
            shadowRect.center = (width*scale // 2, height*scale // 4 + shadow_offset)
            
            screen.blit(shadow, shadowRect)
            screen.blit(text, textRect)
            pygame.display.update()
            
            next_level = False
            while not next_level:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            next_level = True
                            break
            # prepare next level
            if current_level_no < len(level_list)-1:
                current_level_no += 1
                current_level = level_list[current_level_no]
                player.level = current_level
                x, y = current_level.player_start_position
                player.set_start_position(x, y)
 
        # if the game still goes on then draw the sprites
        if not done:
            current_level.draw(screen)
            active_sprite_list.draw(screen)
 
        # Limit to 50 frames per second
        clock.tick(50)
        for cmd in command_log:
            print(cmd)
 
        # update the screen
        pygame.display.flip()
 
    pygame.quit()
 
if __name__ == "__main__":
    main(60, 30, 20)