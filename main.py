import pygame
from pygame.locals import *
import math
from agent import Agent
from level import Level 
 
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
    level_list.append(Level("levels/level1.png", scale=20))
 
    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]

    # Create the player
    x, y = current_level.player_start_position
    player = Agent("Tux", x, y, width, height, scale)
    player.controls(pygame.K_SPACE, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT)
 
    active_sprite_list = pygame.sprite.Group()
    player.level = current_level
 
    active_sprite_list.add(player)
 
    # Loop until the user clicks the close button.
    done = False
 
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
 
    # -------- Main Program Loop -----------
    while not done:
        # fill background with image
        for i in range( 0, tiles):
            screen.blit(bg, (i*bg_width+scroll,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                player.kill()
                done = True
 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    cmd = player.commands(pygame.K_LEFT)
                    if cmd:
                        command_log.append(cmd)
                if event.key == pygame.K_RIGHT:
                    cmd = player.commands(pygame.K_RIGHT)
                    if cmd:
                        command_log.append(cmd)
                if event.key == pygame.K_SPACE:
                    cmd = player.commands(pygame.K_SPACE)
                    if cmd:
                        command_log.append(cmd)
 
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()
 
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
        current_position = player.rect.x + current_level.world_shift
        if current_position < current_level.level_limit:
            player.rect.x = 120
            if current_level_no < len(level_list)-1:
                current_level_no += 1
                current_level = level_list[current_level_no]
                player.level = current_level
 
        current_level.draw(screen)
        active_sprite_list.draw(screen)
 
        # Limit to 60 frames per second
        clock.tick(60)
        for cmd in command_log:
            print(cmd)
            command_log.remove(cmd) #reduces cmd print spam
 
        # update the screen
        pygame.display.flip()
 
    pygame.quit()
 
if __name__ == "__main__":
    main(60, 30, 20)