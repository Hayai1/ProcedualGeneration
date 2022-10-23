import pygame

class Player:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x,self.y,16,16)
    
        