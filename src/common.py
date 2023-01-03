import pygame
from enum import Enum

CATCH_COIN = pygame.event.custom_type()
ENEMY_KILLED = pygame.event.custom_type()
TUX_DEAD = pygame.event.custom_type()

ALPHA = (0, 255, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

class Subject:

    def __init__(self):
        self.events = {}

    def register(self, event, event_handler):
        if event not in self.events:
            self.events[event] = []
        self.events[event].append(event_handler)

    def notify(self, event):
        for event_handler in self.events[event]:
            event_handler()

class Directions(Enum):
    UP = (0,-1)
    DOWN = (0,1)
    LEFT = (-1,0)
    RIGHT = (1,0)

class Command:
    def __init__(self) -> None:
        pass

class Up(Command):
    def __init__(self) -> None:
        pass
    
class Left(Command):
    def __init__(self) -> None:
        pass

class Down(Command):
    def __init__(self) -> None:
        pass

class Right(Command):
    def __init__(self) -> None:
        pass
    
class Size_Up(Command):
    def __init__(self) -> None:
        pass 
    
class Stop(Command):
    def __init__(self) -> None:
        pass
    

