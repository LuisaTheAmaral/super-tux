import pygame 
from spritesheet import SpriteSheet
from common import Directions, Up, Left, Down, Right, Size_Up, ALPHA
import logging
from fsm import FSM, State, Transition
from enum import Enum
from agent import Agent

# Global constants
CELL_SIZE = 50
CELL_SIZE_w = 64
CELL_SIZE_h = 80

ENEMY_KILLED = pygame.event.custom_type()
TUX_DEAD = pygame.event.custom_type()

# TUX STATES  
class Event(Enum):
    IDLE = 1,
    WALK = 2,
    JUMP = 3,
    GROW = 4,
    SHRINK = 5,
    DIE = 6
    
# | TUX IDLE STATE
class Idle(State):
    def __init__(self) -> None:
        super().__init__(self.__class__.__name__)

    # stop tux
    def update(self, object, dir, previous):
        object.stop()
        
    # getting idle coords
    def get_xy(self, dir, walking_pointer):
        walking_pointer = 0
        if dir == Directions.LEFT:
            frameX, frameY = (0, 3)
        elif dir == Directions.RIGHT:
            # idle sprite
            frameX, frameY = (0, 0)
        return frameX, frameY, walking_pointer
    
# | TUX WALK STATE
class Walk(State):
    # walking sprite coords
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
        super().__init__(self.__class__.__name__)

    # move tux
    def update(self, object, dir, previous):
        if dir==Directions.LEFT:
            object.move(Directions.LEFT, change_x = 6)
        else:
            object.move(Directions.RIGHT, change_x = 6)
    
    # getting walking sprite      
    def get_xy(self, dir, walking_pointer):
        if dir == Directions.LEFT:
            frameX, frameY = self.WALKING_R[int(walking_pointer)]
        elif dir == Directions.RIGHT:
            frameX, frameY = self.WALKING[int(walking_pointer)]
        walking_pointer = (walking_pointer + 0.2) % len(self.WALKING)
        return frameX, frameY, walking_pointer

# | TUX JUMP STATE
class Jump(State):
    def __init__(self) -> None:
        super().__init__(self.__class__.__name__)

    # make tux jump
    def update(self, object, dir, previous):
        object.jump(previous)
        
    # getting jumping sprite
    def get_xy(self, dir):
        if dir == Directions.LEFT:
            frameX, frameY = (3, 4)
        if dir == Directions.RIGHT:
            frameX, frameY = (3, 1)
        return frameX, frameY
    
# | TUX GROW STATE
class Grow(State):
    def __init__(self) -> None:
        super().__init__(self.__class__.__name__)

    # change active state machine to big tux
    def update(self, object, dir, previous):
        object.grow_toggle(previous)
    
# | TUX DIE STATE
class Die(State):
    # dead sprite coords
    DEAD = (3,2)
    
    def __init__(self) -> None:
        super().__init__(self.__class__.__name__)

    # kill tux
    def update(self, object, dir, previous):
        return object.kill()
    
    # getting dead sprite
    def get_xy(self):
        return self.DEAD
 
# | TUX SHRINK STATE   
class Shrink(State):
    def __init__(self) -> None:
        super().__init__(self.__class__.__name__)

    # change active state machine to mini tux
    def update(self, object, dir, previous):
        object.grow_toggle(previous)
        

STATES_MINI = [Idle, Walk, Jump, Grow, Die]

TRANSITIONS_MINI = {
    Event.IDLE: [Transition(Walk, Idle), Transition(Jump, Idle), Transition(Grow, Idle)],
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

STATES_BIG = [Idle, Walk, Jump, Shrink]

TRANSITIONS_BIG = {
    Event.IDLE: [Transition(Walk, Idle), Transition(Jump, Idle), Transition(Shrink, Idle)],
    Event.WALK: [Transition(Idle, Walk), Transition(Jump, Walk)],
    Event.SHRINK: [
        Transition(Idle, Shrink),
        Transition(Walk, Shrink),
        Transition(Jump, Shrink),
    ],
    Event.JUMP: [
        Transition(Idle, Jump),
        Transition(Walk, Jump)
    ]
}

class Tux(Agent):
    def __init__(self, name, initial_x, initial_y, width, height, scale):
        super().__init__(name, width, height, scale, Directions.RIGHT)
        # load mini tux sheet
        self.sheet = SpriteSheet("sprites/spritesheet_full.png")
        
        frameX, frameY = (0, 3)
        
        self.cellsize = (CELL_SIZE,CELL_SIZE)
        
        self.image = self.sheet.image_at((frameX * CELL_SIZE, frameY * CELL_SIZE, CELL_SIZE, CELL_SIZE), colorkey=ALPHA)
        self.rect = self.image.get_rect()
        self.set_start_position(initial_x, initial_y) #set player initial  position 

        # start with mini tux
        self.tux_size = 0 # mini=0; big=1
        
        # state machine when tux is mini
        self.fsm_mini = FSM(STATES_MINI, TRANSITIONS_MINI)
        
        # state machine when tux is big
        self.fsm_max = FSM(STATES_BIG, TRANSITIONS_BIG)
        
        # main state machine
        self.fsm_main = self.fsm_mini
        
    def grow_toggle(self, previous):
        """ Changes tux size. """
        
        tmp = self.rect
        if not self.tux_size:
            # if tux is mini change to big tux
            self.fsm_main = self.fsm_max
            self.sheet = SpriteSheet("sprites/spritesheet_big_full.png")
            frameX, frameY = (0, 3)
            
            self.cellsize = (CELL_SIZE_w, CELL_SIZE_h)
            
            self.image = self.sheet.image_at((frameX * CELL_SIZE_w, frameY * CELL_SIZE_h, CELL_SIZE_w, CELL_SIZE_h), colorkey=ALPHA)
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = tmp.x, tmp.y
            self.tux_size = 1
        else:
            # if tux is big change to mini tux
            self.fsm_main = self.fsm_mini
            self.sheet = SpriteSheet("sprites/spritesheet_full.png")
            frameX, frameY = (0, 3)
            
            self.cellsize = (CELL_SIZE, CELL_SIZE)
            
            self.image = self.sheet.image_at((frameX * CELL_SIZE, frameY * CELL_SIZE, CELL_SIZE, CELL_SIZE), colorkey=ALPHA)
            self.rect = self.image.get_rect()
            
            self.rect.x, self.rect.y = tmp.x, tmp.y-60 # tux jumps after changing to mini
            self.tux_size = 0
            
        # change to IDLE state
        self.fsm_main.update(Event.IDLE, self)
        
    
    def commands(self, control):
        """ Receives commands from input and changes state of tux based on them. """
        c_event = Event.IDLE
        
        if control in self.control_keys.keys():
            cmd = self.control_keys[control]()
            
            if isinstance(cmd,Right):
                c_event = Event.WALK
                self.direction = Directions.RIGHT
                self.fsm_main.update(c_event, self, dir=Directions.RIGHT)   
                return
            elif isinstance(cmd,Left):
                c_event = Event.WALK
                self.direction = Directions.LEFT
                self.fsm_main.update(c_event, self, dir=Directions.LEFT)
                return
            elif isinstance(cmd,Up):
                c_event = Event.JUMP
            elif isinstance(cmd,Size_Up):
                if not self.tux_size:
                    c_event = Event.GROW
                else:
                    c_event = Event.SHRINK

        self.fsm_main.update(c_event, self)
        return None
 
    def update(self):
        # Get body
        x, y = self.rect.x, self.rect.y
        
        current_state = self.fsm_main.get_cstate()()
        
        if isinstance(current_state,Jump):
            #tux is jumping
            frameX, frameY = Jump().get_xy(self.direction)
        elif isinstance(current_state, Walk):
            #tux is walking
            frameX, frameY, self.walking_pointer = current_state.get_xy(self.direction, self.walking_pointer)
        elif isinstance(current_state, Idle):
            #tux is idle
            frameX, frameY, self.walking_pointer = current_state.get_xy(self.direction, self.walking_pointer)
        elif isinstance(current_state, Die):
            #tux is dead
            frameX, frameY = current_state.get_xy()
        else:
            print("ERROR")
          
        super().update(x,y,frameX,frameY,cell_size=self.cellsize)
        
        if self.dead:
            ev = pygame.event.Event(TUX_DEAD)
            pygame.event.post(ev)
            return
        
    
    def collisions(self, frameX, frameY):
        """ Verify collisions of tux with platforms and enemies. """
        
        # kill tux if he is on the bottom of the screen
        if not self.tux_size and self.rect.y == 550:
            self.fsm_main.update(Event.DIE, self)
            return frameX, frameY
        elif self.tux_size and self.rect.y == 520:
            self.fsm_main.update(Event.SHRINK, self)
            return frameX, frameY
        
        # verify if tux has colided with any enemy
        #block_hit_list = pygame.sprite.spritecollide(self, self.level.enemy_list, False)
        
        for enemy in self.level.enemy_list:
            if not enemy.dead:
                block_hit_list = pygame.sprite.spritecollide(self, [enemy], False)
                for block in block_hit_list:
                    if self.change_x < 10 and self.change_y > 0:
                        if (self.change_y==1 and self.tux_size) or (self.change_y<2 and not self.tux_size):
                            # tux has been hit
                            self.been_hit()
                        else:
                            # enemy has been killed - notify enemy
                            #ev = pygame.event.Event(ENEMY_KILLED)
                            print("enemy has been hit")
                            ev = pygame.event.Event(ENEMY_KILLED, {"enemy": enemy})
                            pygame.event.post(ev)
            
            
        # See tux hit anything (platforms)
        frameX, frameY, idle = super().collisions(frameX,frameY)

        #making sure that tux changes to idle when he lands on the ground and does not move
        if idle:
            self.fsm_main.update(Event.IDLE, self)
                
        return frameX, frameY
    
    def been_hit(self):
        """ Tux has been hit. """
        if not self.tux_size:
            print("TUX is dead")
            self.fsm_main.update(Event.DIE, self)
        else:
            self.fsm_main.update(Event.SHRINK, self)
 