from agent import Agent
from spritesheet import SpriteSheet
from enum import Enum
from fsm import State,Transition,FSM
from common import Directions, Up, Left, Down, Right, ALPHA

# TUX STATES  
class Event(Enum):
    IDLE = 1,
    WALK = 2,
    DIE = 3

class Idle(State):
    def __init__(self) -> None:
        super().__init__(self.__class__.__name__)

    def update(self, object, dir, previous):
        object.stop()
        
    def get_xy(self, dir, walking_pointer):
        walking_pointer = 0
        if dir == Directions.LEFT:
            frameX, frameY = (0, 1)
        elif dir == Directions.RIGHT:
            # idle sprite
            frameX, frameY = (0, 1)
        return frameX, frameY, walking_pointer

class Walk(State):
    WALKING =   [(0, 0), #walk-0
                (0, 1), #walk-1 
                (0, 2)] #walk-2
    WALKING_R = [(0, 0), #walk-0
                (0, 1), #walk-1 
                (0, 2)] #walk-2
    def __init__(self) -> None:
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
        return frameX, frameY, walking_pointer
    
class Die(State):
    def __init__(self) -> None:
        super().__init__(self.__class__.__name__)

    def update(self, object,dir):
        #print("Tux Growing")
        return super().update(object)

    def get_xy(self, dir, walking_pointer):
        walking_pointer = 0
        if dir == Directions.LEFT:
            frameX, frameY = (0, 3)
        elif dir == Directions.RIGHT:
            # idle sprite
            frameX, frameY = (0, 3)
        return frameX, frameY, walking_pointer

STATES = [Idle, Walk, Die]

TRANSITIONS = {
    Event.WALK: [Transition(Idle, Walk)],
    Event.DIE: [
        Transition(Idle, Die),
        Transition(Walk, Die)
    ]
}

class Monster(Agent):
    def __init__(self, x, y, name, width, height, scale) -> None:
        super().__init__(name, x, y, width, height, scale)
        self.name = name
        self.direction = Directions.LEFT
        self.direction_auto = Directions.LEFT
        
        # state machine responsible for tux in big or mini
        self.fsm = FSM(STATES, TRANSITIONS)
    
class Snowball(Monster):
    def __init__(self, x, y, width, height, scale) -> None:
        super().__init__("snowball", x, y, width, height, scale)
        self.rect.x = 400
        self.rect.y = 700
        self.sheet = SpriteSheet("sprites/spritesheet_enemy.png")
 
    def comandos(self):
        self.fsm.update(Event.WALK, self, dir=Directions.LEFT) 
        return None
 
    # update sprite based on state
    def update(self):        
        # Get body
        self.fsm.update(Event.WALK, self, dir=Directions.LEFT) 
        
        x, y = self.rect.x, self.rect.y
        
        current_state = self.fsm.get_cstate()()
        
        if self.direction != self.direction_auto:
            self.direction = self.direction_auto
  
        if isinstance(current_state, Walk):
            #tux is walking
            frameX, frameY, self.walking_pointer = current_state.get_xy(self.direction, self.walking_pointer)
        #if tux is not jumping nor walking (he could be falling), render idle sprite
        elif isinstance(current_state, Idle):
            #tux is idle
            frameX, frameY, self.walking_pointer = current_state.get_xy(self.direction, self.walking_pointer)
        elif isinstance(current_state, Die):
            #tux is idle
            frameX, frameY, self.walking_pointer = current_state.get_xy(self.direction, self.walking_pointer)
        else:
            print("ERROR")
            
        super().update(x,y,frameX,frameY)
        
 
    def collisions(self, frameX, frameY):
        # See if we hit anything
        frameX, frameY, idle = super().collisions(frameX,frameY)

        current_state = self.fsm.get_cstate()

        #making sure that tux changes to idle when he lands on the ground and does not move
        if idle and current_state!=Idle:
            self.fsm.update(Event.IDLE, self)
                
        return frameX, frameY
 