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
        self.WIDTH = width

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
        # If the player gets near the right side, stop it
        if self.body[0] + self.direction.value[0] > self.WIDTH-2:
            self.body = (self.WIDTH-2, self.body[1])
        # If the player gets near the left side, stop it
        elif self.body[0] + self.direction.value[0] < 0:
            self.body = (0, self.body[1])
        else:
            self.body = (self.body[0] + self.direction.value[0], self.body[1] + self.direction.value[1])

    def kill(self):
        logging.info("Agent died")
        self.dead = True