from enum import Enum
from datetime import datetime

ALPHA = (0, 255, 0)

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
    

