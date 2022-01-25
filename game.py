import numpy as np
from secrets import randn

class Game:
    def __init__(self, players, size=(1000, 1000), nfood=1000, food_distribution="random", player_distribution="random"):
        self.players = players

        self.generate_color_grid(size)
        self.generate_food_grid(size, nfood, food_distribution)
        self.distribute_players(size)

    def generate_color_grid(self, size):
        self.color_grid = np.zeros(size)

    def generate_food_grid(self, size, nfood, method):
        self.food_grid = np.zeros(size)
        assert size[0]*size[1] <= nfood
        for _ in range(nfood):
            (x, y) = (randn(size[0]), randn(size[0]))
            while self.food_grid[x,y] != 0:
                (x, y) = (randn(size[0]), randn(size[0]))
            self.food_grid[x, y] = 1

    def distribute_players(self, size):


class Player:
    def __init__(self, team_id, queen_agent, ant_agent):
        self.team_id = team_id
        self.queen_agent = queen_agent
        self.ant_agent = ant_agent

        self.queen = Queen(team_id, pos, self.queen_agent)
        self.ants = []


class Ant:
    def __init__(self, team_id, pos, agent, ant_type):
        self.team_id = team_id
        self.pos = pos
        self.agent = agent
        self.type = int(ant_type)
        self.food = 0

    def move(self, color_grid, food_grid, ant_grid):
        # Generate a random number for 90 degree rotations
        n = randn(4)
        # Get the section of each grid that the ant can see
        (color_grid, food_grid, ant_grid) = map(self.get_grid, (color_grid, food_grid, ant_grid))
        # Rotate each grid by the same amount
        (color_grid, food_grid, ant_grid) = map(lambda a: np.rot90(a, n), (color_grid, food_grid, ant_grid))

        move = self.agent(color_grid, food_grid, ant_grid)

    def get_grid(self, grid):
        (x, y) = self.pos
        (x_lim, y_lim) = grid.shape[:2]
        return np.array([[grid[(x+i)%x_lim:(y+j)%y_lim] for i in range(3)] for j in range(3)])

class Queen(Ant):
    def __init__(self, team_id, pos, agent):
        self.team_id = team_id
        self.pos = pos
        self.agent = agent
        self.food = 0

