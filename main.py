import pygame, math
from agent import Agent
from spritesheet import SpriteSheet
from common import Directions
from sprites import AgentSprite

BLACK = (0, 0, 0)

def main(WIDTH, HEIGHT, SCALE=20):
    pygame.init()
    command_log = []
    display = pygame.display.set_mode((SCALE * WIDTH, SCALE * HEIGHT))
    clock = pygame.time.Clock()

    # background scroll setup
    bg = pygame.image.load("assets/arctis.jpg").convert()
    bg_width = bg.get_width()
    scroll = 0
    tiles= math.ceil(WIDTH / bg_width) + 1

    pygame.display.set_caption('Super Tux')

    #sprite = SpriteSheet("sprites/spritesheet.png")
    sprite = SpriteSheet("sprites/spritesheet_full.png")

    agent = Agent("Tux", WIDTH, HEIGHT)
    agent_sprite = AgentSprite(agent, sprite.sheet, WIDTH, HEIGHT, SCALE)
    agent.controls(pygame.K_SPACE, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT)

    all_sprites = pygame.sprite.Group()
    all_sprites.add(agent_sprite)

    while True: # main game loop

        # fill background with image
        for i in range( 0, tiles):
            display.blit(bg, (i*bg_width+scroll,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                agent.kill()
                pygame.quit()
                exit(0)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                cmd = agent.commands(event.key)
                if cmd:
                    command_log.append(cmd)
                    agent.move()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            cmd = agent.commands(pygame.K_LEFT)
            if cmd:
                command_log.append(cmd)
                agent.move()
                # move background
                scroll += 2
        if keys[pygame.K_RIGHT]:
            cmd = agent.commands(pygame.K_RIGHT)
            if cmd:
                command_log.append(cmd)
                agent.move()
                # move background
                scroll -= 2
        if keys[pygame.K_DOWN]:
            cmd = agent.commands(pygame.K_DOWN)
            if cmd:
                command_log.append(cmd)
                agent.move()

        # Render sprites
        all_sprites.update()
        
        #if tux moved up then it has to come down (jump)
        if agent.direction == Directions.UP:
            cmd = agent.commands(pygame.K_DOWN)
            if cmd:
                command_log.append(cmd)
                agent.move()
        

        #display.fill(BLACK)
        all_sprites.draw(display)
        pygame.display.flip()
        clock.tick(10)
        for cmd in command_log:
            print(cmd)

if __name__ == "__main__":
    main(60, 30)
