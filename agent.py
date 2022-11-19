import logging
from common import Directions, Actor, Command, Up, Left, Down, Right

class Agent(Actor):
    def __init__(self, name, width, height):
        self.name = name
        self.control_keys = {}
        self.body = (width // 2, height // 4)
        self.length = len(self.body)
        self.direction = Directions.DOWN
        self.dead = False

    def controls(self, up, left, down, right):
        self.control_keys = {
            up: Up, 
            left: Left, 
            down: Down, 
            right: Right}

    def commands(self, control):
        if control in self.control_keys.keys():
            cmd = self.control_keys[control]()
            cmd.execute(self)
            return cmd
    
    def move(self, direction: Directions = None):
        if direction:
            self.direction = direction

        self.body = (self.body[0] + self.direction.value[0], self.body[1] + self.direction.value[1])
    
    def kill(self):
        logging.info("Agent died")
        self.dead = True