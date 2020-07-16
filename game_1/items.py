import pygame
import random


class Triangle():
    
    def __init__(self, screen, size, speed):
        self.screen = screen
        self.size = size
        self.position = [random.randint(0,600), random.randrange(-100,0,5)]
        self.speed = speed
        self.ACTIVE = True
        self.top_vertex = (self.position[0]+(self.size//1.5), self.position[1])
        self.left_vertex = (self.position[0], self.position[1]+self.size)
        self.right_vertex = (self.position[0]+self.size, self.position[1]+self.size)
        self.points = [self.top_vertex, self.left_vertex, self.right_vertex]
        self.RED = (255,000,000)
        self.PURPLE = (125,75,150)
        self.BLUE = (000,000,255)
        self.GREEN = (000,255,000)
        self.BLACK = (000,000,000)
        self.WHITE = (255,255,255)
        self.GOLD = (255,215,000)
                       
    def drawSelf(self):
        pygame.draw.polygon(self.screen, self.GOLD, self.points)

    def updateTriangle(self):
        self.position[1] += self.speed 
        self.top_vertex = (self.position[0]+(self.size//2), self.position[1])
        self.left_vertex = (self.position[0], self.position[1]+self.size)
        self.right_vertex = (self.position[0]+self.size, self.position[1]+self.size)
        self.points = [self.top_vertex, self.left_vertex, self.right_vertex]
        if self.right_vertex[1] > self.screen.get_height() - self.size or self.left_vertex[1] > self.screen.get_height() - self.size:
            self.ACTIVE = False
           
    def dropTriangle(self):
        pygame.draw.polygon(self.screen, self.PURPLE, self.points)
        self.updateTriangle()
        pygame.draw.polygon(self.screen, self.GOLD, self.points) 

    def detectCollision(self, player):
        if player.shape == 'triangle':
            if (player.top_vertex[0] >= self.position[0] and player.top_vertex[0] <= self.position[0]+self.size):
                if (player.top_vertex[1] >= self.position[1] and player.top_vertex[1] <= self.position[1]+self.size):
                    self.ACTIVE = False
                    return True
        if ((self.position[0] >= player.position[0] and self.position[0] <= player.position[0]+player.size) or (player.position[0] >= self.position[0] and player.position[0] <= self.position[0]+self.size)):
            if(self.position[1] >= player.position[1] and self.position[1] <= player.position[1]+player.size or (player.position[1] >= self.position[1] and player.position[1] <= self.position[1]+self.size)):
                self.ACTIVE = False
                return True
        return False

    
    