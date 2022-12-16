import pygame 
from spritesheet import SpriteSheet
from common import Directions, Up, Left, Down, Right, ALPHA
import logging
from fsm import FSM, State, Transition
from enum import Enum
from agent import Agent
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

class Tux(Agent):
    def __init__(self, name, width, height, scale):
        super().__init__(name, width, height, scale)
        self.sheet = SpriteSheet("sprites/spritesheet_full.png")
        
        self.rect.x = 0
        self.rect.y = 700
        
        self.prev_body = (540, self.rect.height + 10000)
        
        # state machine responsible for tux in big or mini
        self.fsm_main = FSM(STATES, TRANSITIONS)
        
        # state machine when tux is mini
        self.fsm_mini = FSM(STATES_MINI, TRANSITIONS_MINI)
        
        # state machine when tux is big
        self.fsm_max = FSM(STATES_BIG, TRANSITIONS_BIG)

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
            
        super().update(x,y,frameX,frameY)
        
 
    def collisions(self, frameX, frameY):
        # See if we hit anything
        frameX, frameY, idle = super().collisions(frameX,frameY)

        #making sure that tux changes to idle when he lands on the ground and does not move
        if idle:
            self.fsm_mini.update(Event.IDLE, self)
                
        return frameX, frameY
 