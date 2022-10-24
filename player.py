import pygame

class Player:
    left = False
    right = False
    up = False
    down = False
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x,self.y,16,16)
    def drawPlayer(self,surface,scroll):
        pygame.draw.rect(surface,(0,0,255),pygame.Rect(self.rect.x-scroll[0],self.rect.y-scroll[1],self.rect.width,self.rect.height))
    def move(self):
        if self.left:
            self.rect.x = self.rect.x-3
        if self.right:
            self.rect.x = self.rect.x+3
        if self.down:
            self.rect.y = self.rect.y+3
        if self.up:
            self.rect.y = self.rect.y-3
    
        