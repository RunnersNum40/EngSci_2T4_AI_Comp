import numpy as np
import asyncio
import pygame
import time
from pygame.locals import *
from math import *
from render import Screen

clock = pygame.time.Clock()

class Game:
    """A game object facilitates a game. It handles game state change, querying agents, and drawing the board."""
    def __init__(self, agents=[]):
        self.players = [Player(a, n) for n, a in enumerate(agents)]
        self.nodes = []
        self.caravans = []

        self.generate_board(square_generator, 4)

        if game_options["render_game"]:
            self.screen = Screen(self)
        self.tick_count = 0

    def generate_board(self, method, seed=0):
        self.nodes = method(self.players, seed)

    def tick(self):
        state = self.sanitize()
        for p in self.players:
            action = p.tick(state)
        for n in self.nodes:
            n.tick()
        for c in self.caravans:
            c.tick()

        if game_options["render_game"]:
            self.screen.draw()

        tick_count += 1

    def check_winner(self):
        pass

    def game_loop(self):
        while self.check_winner() is None:
            self.tick()
            self.clock.tick(game_options["tps"])

class VoidGame(Game):
    """A VoidGame is a copy of a Game that does not allow players to change the game state"""

class Node:
    """A Node is a single part of the game. Each Node has an owner, a position and a size.
    Nodes start with no owner and require a sacrifice of n units where n=size to become owned.
    Once a node is owned it generates a size number of units every size_max ticks.
    To capture a node a player must send more units to the node than it contains.
    The owner of a node can send up to all the units in the node to any other node."""

    def __init__(self, pos, size=None, owner=None):
        """Inialize the node and generate attributes as needed"""
        self.pos = pos
        self.size = size if size else int(np.random.rand()*game_options["size_max"]) # If not given a size: generate one
        self.owner = owner

        self.units = self.size # The integer number of units
        self._units = 0 # The number of units as a floating point

    def tick(self):
        """Generate self.size units every size_max ticks."""
        if owner is not None: # While owned
            self._units += self.size/game_options["size_max"] # Add the number of units per tick
        if self._units >= 1: # When new units are generated
            self.units += floor(self._units) # Add them to the unit count
            self._units -= floor(self._units) # And subtract them from the unit generation

    @property
    def x(self):
        """Return the x position of the node"""
        return self.pos[0]

    @property
    def y(self):
        """Return the y position of the node"""
        return self.pos[1]

    def __str__(self):
        return f"Size {self.size} Node at {self.pos} owned by {self.owner}"

    def __repr__(self):
        return f"Node({self.pos}, {self.size}, {repr(self.owner)})"

class Caravan:
    """A Caravan is a group of units traveling from one node to another.
    A Caravan is generated when a player sends units and handles the travel time.
    When a Caravan reaches it's target it is destroyed."""

    def __init__(self, owner, size, origin, destination):
        self.owner = owner
        self.size = size
        self.origin = origin
        self.destination = destination

        self.distance = sqrt((origin.pos[0]-destination.pos[0])**2+(origin.pos[1]-destination.pos[1])**2) # Calculate the distance that needs to be traveled

    @property
    def x(self):
        """Return the x position of the caravan"""
        return self.pos[0]

    @property
    def y(self):
        """Return the y position of the caravan"""
        return self.pos[1]

    def tick(self):
        pass

class Player:
    """A Player is an interface for the game and a controller agent"""

    def __init__(self, game, agent, code):
        self.game = game
        self.agent = agent
        self.code = code

        self.color = self._random_color()

    def tick(self, state):
        return agent(state)

    @staticmethod
    def _random_color():
        """Return a random color"""
        return list(np.random.choice(range(255),size=3))

def square_generator(players, n):
    """Return a square grid of Nodes with balanced sizes for the top right and bottom left corner.
    This is good for a standard two player game."""
    grid = [[int(np.random.rand()*game_options["size_max"]) for x in range(y+1)] for y in range(n)] # Generate a lower triangular of sizes

    board = []
    for y in range(n):
        for x in range(y+1):
            board.append(Node((x, y), grid[y][x]))
            if x != y:
                board.append(Node((y, x), grid[y][x]))

            if y == n-1 and x == 0:
                board[-2].owner = players[0]
                board[-1].owner = players[1]

    return board

def layer_generator(layers, n, m):
    nums = np.random.randint(n, m, size=layers//2) # Number of nodes per layer

game_options = {"tps":60, # ticks per second
                "tpr":1, # ticks per render
                "size_max":100,
                "render_game":True}

if __name__ == '__main__':
    b = Game([None, None])
    b.screen.draw()
    time.sleep(10)