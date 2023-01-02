import pygame
from pygame.locals import *
import math
from agent import Agent
from level import Level 
from tux import Tux, ENEMY_KILLED, TUX_DEAD
from monster import Snowball
from scoreboard import Scoreboard
 
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
    level_list.append(Level("levels/level1.png", scale=scale))
    level_list.append(Level("levels/level2.png", scale=scale))
    level_list.append(Level("levels/level3.png", scale=scale))
 
    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]

    scoreboard = Scoreboard(SCREEN_WIDTH)

    # Create the player
    x, y = current_level.player_start_position
    player = Tux("Tux", x, y, width, height, scale)
    player.controls(pygame.K_SPACE, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_g)
    
    snowball = Snowball(x+27, y-4, width, height, scale) # temp location
    
    current_level.add_enemy(snowball)
    
    active_sprite_list = pygame.sprite.Group()
    player.level = current_level
    snowball.level = current_level
 
    active_sprite_list.add(player)
    active_sprite_list.add(scoreboard)
    # active_sprite_list.add(snowball)
 
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
                dead_event = 1
                    
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_SPACE, pygame.K_g):
                    cmd = player.commands(event.key)
                    if cmd:
                        command_log.append(cmd)
 
            if event.type == pygame.KEYUP:
                if (event.key == pygame.K_LEFT and player.change_x < 0) or (event.key == pygame.K_RIGHT and player.change_x > 0):
                    cmd = player.commands(None)
                    if cmd:
                        command_log.append(cmd)
        
        # send command to enemy
        snowball.commands(dead_event)
        
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

        # If the player collides with a coin it has to disappear and the scoreboard needs to be updated
        coin_hit_list = pygame.sprite.spritecollide(player, current_level.coin_list, False)
        for coin in coin_hit_list:
            current_level.coin_list.remove(coin)
            scoreboard.increase_points()
 
        # If the player gets to the end of the level, go to the next level
        block_hit_list = pygame.sprite.spritecollide(player, current_level.goal_list, False)
        if block_hit_list:
            print(f"LEVEL {current_level_no+1} COMPLETED")
            if current_level_no == len(level_list) - 1:
                player.kill()
                done = True
            player.stop() #temporary

        # current_position = player.rect.x + current_level.world_shift
        # if current_position < current_level.level_limit:
        #     player.rect.x = 120
            if current_level_no < len(level_list)-1:
                current_level_no += 1
                current_level = level_list[current_level_no]
                player.level = current_level
                snowball.level = current_level
                x, y = current_level.player_start_position
                player.set_start_position(x, y)
 
        current_level.draw(screen)
        active_sprite_list.draw(screen)
 
        # Limit to 60 frames per second
        clock.tick(50)
        for cmd in command_log:
            print(cmd)
            command_log.remove(cmd) #reduces cmd print spam
 
        # update the screen
        pygame.display.flip()
 
    pygame.quit()
 
if __name__ == "__main__":
    main(60, 30, 20)