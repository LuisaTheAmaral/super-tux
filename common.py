from enum import Enum
from datetime import datetime

ALPHA = (0, 255, 0)

class Directions(Enum):
    UP = (0,-1)
    DOWN = (0,1)
    LEFT = (-1,0)
    RIGHT = (1,0)

class Actor:
    def __init__(self):
        self.name = "Unknown"

    def move(self, direction: Directions):
        raise NotImplemented

class Command:
    def __init__(self) -> None:
        self.actor = None
        self.dt = datetime.now()

    def execute(self, actor):
        raise NotImplemented

    def __str__(self):
        return f"[{self.dt}] {self.actor.name}: {self.__class__.__name__}"

class Up(Command):
    def execute(self, actor):
        self.actor = actor
        actor.jump()

class Left(Command):
    def execute(self, actor):
        self.actor = actor
        actor.move(Directions.LEFT)

class Down(Command):
    def execute(self, actor):
        #not used yet
        self.actor = actor
        actor.move(Directions.DOWN)

class Right(Command):
    def execute(self, actor):
        self.actor = actor
        actor.move(Directions.RIGHT)
    

