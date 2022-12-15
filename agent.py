import pygame 
from spritesheet import SpriteSheet
from common import Directions, Up, Left, Down, Right, ALPHA
import logging
from fsm import FSM, State, Transition
from enum import Enum

# Global constants
CELL_SIZE = 50

# TUX STATES  
class Event(Enum):
    IDLE = 1,
    WALK = 2,
    JUMP = 3,
    GROW = 4,
    SHRINK = 5,
    DIE = 6
    
class Idle(State):
    def __init__(self) -> None:
        super().__init__(self.__class__.__name__)

    def update(self, object, dir, previous):
        object.stop()
        
    def get_xy(self, dir, walking_pointer):
        walking_pointer = 0
        if dir == Directions.LEFT:
            frameX, frameY = (0, 3)
        elif dir == Directions.RIGHT:
            # idle sprite
            frameX, frameY = (0, 0)
        return frameX, frameY, walking_pointer

class Walk(State):
    WALKING =   [(2, 0), #walk-0
                (0, 1), #walk-1 
                (1, 1), #walk-2
                (2, 1), #walk-3
                (0, 2), #walk-4
                (1, 2), #walk-5
                (2, 2), #walk-6
                (3, 0)] #walk-7
    WALKING_R = [(2, 3), #walk-0 
                (0, 4), #walk-1 
                (1, 4), #walk-2
                (2, 4), #walk-3
                (0, 5), #walk-4
                (1, 5), #walk-5
                (2, 5), #walk-6
                (3, 3)] #walk-7
    def __init__(self) -> None:
        print("new WALK")
        super().__init__(self.__class__.__name__)

    def update(self, object, dir, previous):
        
        if dir==Directions.LEFT:
            object.move(Directions.LEFT)
        else:
            object.move(Directions.RIGHT)
            
    def get_xy(self, dir, walking_pointer):
        if dir == Directions.LEFT:
            frameX, frameY = self.WALKING_R[walking_pointer]
        elif dir == Directions.RIGHT:
            frameX, frameY = self.WALKING[walking_pointer]
        walking_pointer = (walking_pointer + 1) % len(self.WALKING)
        print(walking_pointer)
        return frameX, frameY, walking_pointer

    
class Jump(State):
    def __init__(self) -> None:
        super().__init__(self.__class__.__name__)

    def update(self, object, dir, previous):
        object.jump(previous)
    
    def get_xy(self, dir):
        #tux is jumping
        if dir == Directions.LEFT:
            frameX, frameY = (3, 4)
        if dir == Directions.RIGHT:
            frameX, frameY = (3, 1)
        return frameX, frameY
    
class Grow(State):
    def __init__(self) -> None:
        super().__init__(self.__class__.__name__)

    def update(self, object, dir):
        #print("Tux Growing")
        return super().update(object)
    
class Die(State):
    def __init__(self) -> None:
        super().__init__(self.__class__.__name__)

    def update(self, object,dir):
        #print("Tux Growing")
        return super().update(object)
    
class Shrink(State):
    def __init__(self) -> None:
        super().__init__(self.__class__.__name__)

    def update(self, object):
        #print("Tux Growing")
        return super().update(object)
    
STATES = [Grow, Shrink]

TRANSITIONS = {
    Event.GROW: [
        Transition(Shrink, Grow)
    ],
    Event.SHRINK: [
        Transition(Grow, Shrink)
    ]
}

STATES_MINI = [Idle, Walk, Jump, Grow, Die]

TRANSITIONS_MINI = {
    Event.IDLE: [Transition(Walk, Idle), Transition(Jump, Idle)],
    Event.WALK: [Transition(Idle, Walk), Transition(Jump, Walk)],
    Event.GROW: [
        Transition(Idle, Grow),
        Transition(Walk, Grow),
        Transition(Jump, Grow)
    ],
    Event.DIE: [
        Transition(Idle, Die),
        Transition(Walk, Die)
    ],
    Event.JUMP: [
        Transition(Idle, Jump),
        Transition(Walk, Jump)
    ]
}

STATES_BIG = [Idle, Walk, Jump, Shrink, Die]

TRANSITIONS_BIG = {
    Event.IDLE: [Transition(Walk, Idle), Transition(Jump, Idle)],
    Event.WALK: [Transition(Idle, Walk), Transition(Jump, Walk)],
    Event.SHRINK: [
        Transition(Idle, Shrink),
        Transition(Walk, Shrink),
        Transition(Jump, Shrink),
    ],
    Event.DIE: [
        Transition(Idle, Die),
        Transition(Walk, Die)
    ],
    Event.JUMP: [
        Transition(Idle, Jump),
        Transition(Walk, Jump)
    ]
}

class Agent(pygame.sprite.Sprite):
    def __init__(self, name, width, height, scale):
        super().__init__()
        self.name = name
        self.sheet = SpriteSheet("sprites/spritesheet_full.png")
        self.SCALE = scale
        self.control_keys = {}
        self.dead = False
        
        # state machine responsible for tux in big or mini
        self.fsm_main = FSM(STATES, TRANSITIONS)
        
        # state machine when tux is mini
        self.fsm_mini = FSM(STATES_MINI, TRANSITIONS_MINI)
        
        # state machine when tux is big
        self.fsm_max = FSM(STATES_BIG, TRANSITIONS_BIG)

        self.walking_pointer = 0
        self.direction = Directions.RIGHT
        
        frameX, frameY = (0, 3) # idle coords
        self.image = self.sheet.image_at((frameX * CELL_SIZE, frameY * CELL_SIZE, CELL_SIZE, CELL_SIZE), colorkey=ALPHA)
        self.rect = self.image.get_rect()
        self.HEIGHT = height*scale
        self.WIDTH = width*scale
 
        self.rect = self.image.get_rect()
        self.prev_body = (340, height - self.rect.height)
 
        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0
 
        # List of level sprites
        self.level = None

    def controls(self, up, left, down, right):
        self.control_keys = {
            up: Up, 
            left: Left, 
            down: Down, 
            right: Right}

    def commands(self, control):
        c_event = Event.IDLE
        if control in self.control_keys.keys():
            cmd = self.control_keys[control]()
            
            if isinstance(cmd,Right):
                c_event = Event.WALK
                self.direction = Directions.RIGHT
                self.fsm_mini.update(c_event, self, dir=Directions.RIGHT)   
                return
            elif isinstance(cmd,Left):
                c_event = Event.WALK
                self.direction = Directions.LEFT
                self.fsm_mini.update(c_event, self, dir=Directions.LEFT)
                return
            elif isinstance(cmd,Up):
                c_event = Event.JUMP

        self.fsm_mini.update(c_event, self)
        return None
 
    def update(self):
        # Get body
        x, y = self.rect.x, self.rect.y
        
        current_state = self.fsm_mini.get_cstate()()
        
        if isinstance(current_state,Jump):
            #tux is jumping
            frameX, frameY = Jump().get_xy(self.direction)
        elif isinstance(current_state, Walk):
            #tux is walking
            frameX, frameY, self.walking_pointer = current_state.get_xy(self.direction, self.walking_pointer)
        #if tux is not jumping nor walking (he could be falling), render idle sprite
        elif isinstance(current_state, Idle):
            #tux is idle
            frameX, frameY, self.walking_pointer = current_state.get_xy(self.direction, self.walking_pointer)
        else:
            print("ERROR")
        
        # Gravity
        self.calc_grav()
 
        # Move left/right
        self.rect.x += self.change_x
 
        # verify collisions
        frameX, frameY = self.collisions(frameX, frameY)

        self.image = self.sheet.image_at((frameX * CELL_SIZE, frameY * CELL_SIZE, CELL_SIZE, CELL_SIZE), colorkey=ALPHA)
        self.prev_body = x, y
 
    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35
 
        # See if we are on the ground
        if self.rect.y >= self.HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = self.HEIGHT - self.rect.height
 
    def jump(self, previous):
        """ Called when user hits 'jump' button. """
        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down 1
        # when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2
 
        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= self.HEIGHT:
            self.change_y = -10
 
    # Player-controlled movement:
    def move(self, direction):
        self.direction = direction
        if direction == Directions.LEFT:
            self.change_x = -6
        elif direction == Directions.RIGHT:
            self.change_x = 6

    def collisions(self, frameX, frameY):
        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite
                self.rect.left = block.rect.right
 
        # Move up/down
        self.rect.y += self.change_y
 
        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
 
            # Reset our position based on the top/bottom of the object
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
 
            # Stop our vertical movement
            self.change_y = 0

        #making sure that tux changes to idle when he lands on the ground and does not move
        if self.change_y == 0 and self.change_x == 0:
            self.fsm_mini.update(Event.IDLE, self)
                
        return frameX, frameY
 
    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0

    def kill(self):
        logging.info("Agent died")
        self.dead = True