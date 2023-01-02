from agent import Agent
from spritesheet import SpriteSheet
from enum import Enum
from fsm import State,Transition,FSM
from common import Directions, Up, Left, Right, ALPHA
import pygame 

# MONSTER STATES  
class Event(Enum):
    IDLE = 1,
    WALK = 2,
    DIE = 3

# | MONSTER IDLE STATE
class Idle(State):
    def __init__(self) -> None:
        super().__init__(self.__class__.__name__)

    # stop monster
    def update(self, object, dir, previous):
        object.stop()
        
    # getting idle sprite
    def get_xy(self, dir, walking_pointer):
        walking_pointer = 0
        if dir == Directions.LEFT:
            frameX, frameY = (1, 0)
        elif dir == Directions.RIGHT:
            frameX, frameY = (1, 1)
        return frameX, frameY, walking_pointer
    
# | MONSTER WALK STATE
class Walk(State):
    # walking sprite coords
    WALKING =   [(0, 1), #walk-0
                (1, 1),  #walk-1 
                (2, 1),  #walk-2
                (1, 1)]  #walk-3
    WALKING_R = [(0, 0), #walk-0
                (1, 0),  #walk-1 
                (2, 0),  #walk-2
                (1, 0)]  #walk-3
    
    def __init__(self) -> None:
        super().__init__(self.__class__.__name__)

    # move monster
    def update(self, object, dir, previous):
        if dir==Directions.LEFT:
            object.move(Directions.LEFT)
        else:
            object.move(Directions.RIGHT)
            
    # getting walking sprite
    def get_xy(self, dir, walking_pointer):
        if dir == Directions.LEFT:
            frameX, frameY = self.WALKING_R[walking_pointer]
        elif dir == Directions.RIGHT:
            frameX, frameY = self.WALKING[walking_pointer]
        walking_pointer = (walking_pointer + 1) % len(self.WALKING)
        return frameX, frameY, walking_pointer
    
# | MONSTER DIE STATE
class Die(State):
    # dead sprite coords
    DEAD = (3,0)
    DEAD_R = (3,1)
    
    def __init__(self) -> None:
        super().__init__(self.__class__.__name__)

    # kill monster
    def update(self, object, dir, previous):
        if object.dead:
            return
        object.kill()
        return object.stop()

    # getting dead sprite
    def get_xy(self,dir):    
        if dir == Directions.LEFT:
            frameX, frameY = self.DEAD
        if dir == Directions.RIGHT:
            frameX, frameY = self.DEAD_R
        return frameX, frameY

STATES = [Idle, Walk, Die]

TRANSITIONS = {
    Event.IDLE: [
        Transition(Walk, Idle),
        Transition(Die, Idle)],
    Event.WALK: [Transition(Idle, Walk)],
    Event.DIE: [
        Transition(Idle, Die),
        Transition(Walk, Die)
    ]
}

class Monster(Agent):
    def __init__(self, name, width, height, scale) -> None:
        super().__init__(name, width, height, scale)
        self.name = name
        self.direction = Directions.LEFT
        self.direction_auto = Directions.LEFT
        
        # state machine responsible for tux in big or mini
        self.fsm = FSM(STATES, TRANSITIONS)
        
    # move enemy automatically
    def commands(self, dead=0):
        if dead:
            self.fsm.update(Event.DIE, self)
        else:
            self.fsm.update(Event.WALK, self, dir=self.direction) 
        return None
 
    # verify collisions and update sprite and state if needed
    def collisions(self, frameX, frameY):
        # See if we hit anything
        frameX, frameY, idle = super().collisions(frameX,frameY)
        
        #making sure that monsyter changes to idle when he lands on the ground and does not move
        if idle:
            self.fsm.update(Event.IDLE, self)
                
        return frameX, frameY
    
    # update sprite based on state
    def update(self):        
        # Get body
        x, y = self.rect.x, self.rect.y
        
        current_state = self.fsm.get_cstate()()
        
        # update direction
        if self.direction != self.direction_auto:
            self.direction = self.direction_auto
  
        if isinstance(current_state, Walk):
            #monster is walking
            frameX, frameY, self.walking_pointer = current_state.get_xy(self.direction, self.walking_pointer)
        elif isinstance(current_state, Idle):
            #monster is idle
            frameX, frameY, self.walking_pointer = current_state.get_xy(self.direction, self.walking_pointer)
        elif isinstance(current_state, Die):
            #monster is dead
            frameX, frameY= current_state.get_xy(dir=self.direction)
        else:
            print("ERROR")
            
        super().update(x,y,frameX,frameY,cell_size=(self.cellsize,self.cellsize))
        
    
class Snowball(Monster):
    def __init__(self, initial_x, initial_y, width, height, scale) -> None:
        super().__init__("snowball", width, height, scale)
        # load snowball spritesheet
        self.sheet = SpriteSheet("sprites/spritesheet_enemy.png")
        self.cellsize = 50
        frameX, frameY = (1, 0)
        self.image = self.sheet.image_at((frameX * self.cellsize, frameY * self.cellsize, self.cellsize, self.cellsize), colorkey=ALPHA)
        self.rect = self.image.get_rect()
        
        self.set_start_position(initial_x, initial_y) #set player initial  position 
        
 