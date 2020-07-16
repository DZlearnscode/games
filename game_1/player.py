import pygame

class Player():
    def __init__(self, screen, size, position, speed):
        self.screen = screen
        self.size = size
        self.position = position
        self.speed = speed
        self.shape = 'rect'
        self.transformCounter = 0
        self.top_vertex = (self.position[0]+(self.size//1.5), self.position[1])
        self.left_vertex = (self.position[0], self.position[1]+self.size)
        self.right_vertex = (self.position[0]+self.size, self.position[1]+self.size)
        #colours
        self.RED = (255,0,0)
        self.PURPLE = (125,75,150)
        self.BLUE = (0,0,255)
        self.GREEN = (0,255,0)
        self.BLACK = (0,0,0)
        self.WHITE = (255,255,255)

    def drawSelf(self):
        if self.shape == 'triangle':
            pygame.draw.polygon(self.screen, self.BLACK, [self.top_vertex, self.left_vertex, self.right_vertex])
        elif self.shape == 'rect':
            pygame.draw.rect(self.screen, self.BLACK, (self.position[0], self.position[1], self.size,self.size))
            
    def updateTriangle(self):
        self.top_vertex = (self.position[0]+(self.size//2), self.position[1])
        self.left_vertex = (self.position[0], self.position[1]+self.size)
        self.right_vertex = (self.position[0]+self.size, self.position[1]+self.size)
        
    def LEFT(self):
        self.drawSelf()
        if not(self.position[0] <= 0):
            self.position[0] -= self.speed
            self.updateTriangle()
        pygame.display.flip()
    
    def RIGHT(self):
        self.drawSelf()
        if not(self.position[0] >= self.screen.get_width() - self.size):
            self.position[0] += self.speed
            self.updateTriangle()
        pygame.display.flip()

    def UP(self):
        if not(self.position[1] <= 0 + self.size):
            self.drawSelf()
            self.position[1] -= self.speed
            self.updateTriangle()
        pygame.display.flip()

    def DOWN(self):
        if not(self.position[1] >= 800 - self.size):
            self.drawSelf()
            self.position[1] += self.speed
            self.updateTriangle()
        pygame.display.flip()



























    """
        pygame.draw.lines(self.screen, self.WHITE, closed=False,points=[ 
                    (self.position[0],self.position[1]), 
                    (self.position[0]+self.size, self.position[1]),
                    (self.position[0],self.position[1]+self.size),
                    (self.position[0]+self.size, self.position[1]+ self.size),
                    (self.position[0],self.position[1]),
                    (self.position[0],self.position[1]+self.size),
                    (self.position[0]+self.size, self.position[1]),
                    (self.position[0]+self.size, self.position[1]+ self.size)]
                    , width=2)
    """