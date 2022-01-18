import pygame
from pygame.locals import *
pygame.font.init()
myfont = pygame.font.SysFont('Source Pro', 20)

class Screen:
    """A screen object renders a boards state"""
    def __init__(self, game=None, scale=100, padding=40, node_size=20, caravan_size=15):
        self.game = game
        self.scale = scale
        self.padding = padding
        self.node_size = node_size

        pos = [[], []] # x, y
        for node in self.game.nodes: # Store the positions of all the nodes
            pos[0].append(node.x)
            pos[1].append(node.y)

        table_size = ((max(pos[0])-min(pos[0]))*self.scale+2*self.padding, (max(pos[1])-min(pos[1]))*self.scale+2*self.padding) # Minimum size needed to show all nodes

        self.screen = pygame.display.set_mode(table_size)

    def draw(self):
        self.screen.fill((0, 0, 0))
        for n in self.game.nodes:
            t = f"{n.units}, {n.size}"

            text = myfont.render(t, False, (255, 255, 255))
            self.screen.blit(text, (n.x*self.scale+self.padding-len(t)*3, n.y*self.scale+self.padding-7))

            pygame.draw.circle(self.screen,
                               n.owner.color if n.owner else (100, 100, 100),
                               (n.x*self.scale+self.padding, n.y*self.scale+self.padding),
                               self.node_size,
                               2)

        for c in self.game.caravans:
            t = str(c.size)

            text = myfont.render(t, False, (255, 255, 255))
            self.screen.blit(text, (c.x*self.scale+self.padding-len(t)*3, c.y*self.scale+self.padding-7))

            pygame.draw.circle(self.screen,
                               c.owner.color if c.owner else (100, 100, 100),
                               (c.x*self.scale+self.padding, c.y*self.scale+self.padding),
                               self.caravan_size,
                               2)

        pygame.display.flip() # Display the changes

    def clear(self):
        self.screen.fill((0, 0, 0))