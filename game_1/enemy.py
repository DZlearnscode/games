import pygame
import random


class Enemy():
    def __init__(self, screen, size, speed, player):
        self.screen = screen
        self.size = size
        self.position = [random.randint(0,600), random.randrange(-100,0,5)]
        self.player = player
        self.speed = speed
        self.wave = 0
        self.DEACTIVE = False
        #colours
        self.RED = (255,0,0)
        self.PURPLE = (125,75,150)
        self.BLUE = (0,0,255)
        self.GREEN = (0,255,0)
        self.BLACK = (0,0,0)
        self.WHITE = (255,255,255)
    
    def dropEnemy(self):
        if self.position[1] >= 800:
            self.DEACTIVE = True
        pygame.draw.rect(self.screen, self.PURPLE, (self.position[0],self.position[1], self.size,self.size))
        self.position[1] += self.speed
        pygame.draw.rect(self.screen, self.RED, (self.position[0],self.position[1], self.size,self.size))
  
    def detectCollision(self, player):
        if player.shape == 'triangle':
            if (player.top_vertex[0] >= self.position[0] and player.top_vertex[0] <= self.position[0]+self.size):
                if (player.top_vertex[1] >= self.position[1] and player.top_vertex[1] <= self.position[1]+self.size):
                    return True
        if ((self.position[0] >= player.position[0] and self.position[0] <= player.position[0]+player.size) or (player.position[0] >= self.position[0] and player.position[0] <= self.position[0]+self.size)):
            if(self.position[1] >= player.position[1] and self.position[1] <= player.position[1]+player.size or (player.position[1] >= self.position[1] and player.position[1] <= self.position[1]+self.size)):
                return True
        return False

        