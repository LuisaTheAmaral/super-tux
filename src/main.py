import pygame
from pygame.locals import *
import math
from agent import Agent
from level import Level 
from tux import Tux, ENEMY_KILLED, TUX_DEAD
from monster import Snowball, Spawner
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
    level_list = []
    level_list.append(Level("assets/levels/level1.png", height=height, scale=scale))
    level_list.append(Level("assets/levels/level2.png", height=height, scale=scale))
    level_list.append(Level("assets/levels/level3.png", height=height, scale=scale))
 
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
 
    # Loop until the user clicks the close button.
    done = False
 
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    
    dead_event=0
    # -------- Main Program Loop -----------
    while not done:
        # fill background with image
        for i in range( 0, tiles):
            screen.blit(bg, (i*bg_width+scroll,0))

        for event in pygame.event.get():
            # if tux is dead end game
            if event.type == pygame.QUIT or event.type == TUX_DEAD:
                done = True
              
            # enemy has been killed  
            if event.type == ENEMY_KILLED:
                tmp_enemy = event.__dict__["enemy"]
                current_level.kill_enemy(tmp_enemy)
                    
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_SPACE):
                    cmd = player.commands(event.key)
                    if cmd:
                        command_log.append(cmd)
 
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

        # If the player gets to the end of the level, go to the next level
        block_hit_list = pygame.sprite.spritecollide(player, current_level.powers, False)
        for power in block_hit_list:
            power.deactivate()
            current_level.powers.remove(power)
            player.grow_toggle()  
 
        # If the player gets to the end of the level, go to the next level
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
            pygame.display.flip()
            
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
                
        # current_position = player.rect.x + current_level.world_shift
        # if current_position < current_level.level_limit:
        #     player.rect.x = 120
            if current_level_no < len(level_list)-1:
                current_level_no += 1
                current_level = level_list[current_level_no]
                player.level = current_level
                # snowball.level = current_level
                x, y = current_level.player_start_position
                player.set_start_position(x, y)
 
        if not done:
            current_level.draw(screen)
            active_sprite_list.draw(screen)
 
        # Limit to 60 frames per second
        clock.tick(50)
        for cmd in command_log:
            print(cmd)
            # command_log.remove(cmd) #reduces cmd print spam
 
        # update the screen
        pygame.display.flip()
 
    pygame.quit()
 
if __name__ == "__main__":
    main(60, 30, 20)