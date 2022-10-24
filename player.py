from turtle import left
import pygame

class Player:
    left = False
    right = False
    up = False
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.velocity = [0,0]
        self.acceleration = [0,0]
        self.rect = pygame.Rect(self.x,self.y,16,16)
    def drawPlayer(self,surface,scroll):
        pygame.draw.rect(surface,(0,0,255),pygame.Rect(self.rect.x-scroll[0],self.rect.y-scroll[1],self.rect.width,self.rect.height))
    def getCollisions(self,tiles):
        collisions = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                collisions.append(tile)
        return collisions

    def updateVelocity(self):
        self.velocity = [0,0]
        if self.acceleration[1] < 3:
            self.acceleration[1] += 0.2
        self.velocity[0] += self.acceleration[0]
        self.velocity[1] += self.acceleration[1]
        if self.left:
            self.velocity[0] -= 2
        if self.right:
            self.velocity[0] += 2
        
    def move(self,tiles):
        collision_types = {'top':False,'bottom':False,'right':False,'left':False}
        self.updateVelocity()
        self.rect.x += self.velocity[0]
        collisions = self.getCollisions(tiles)
        for tile in collisions:
            if self.velocity[0] > 0:
                self.rect.right = tile.left
                collision_types['right'] = True
            elif self.velocity[0] < 0:
                self.rect.left = tile.right
                collision_types['left'] = True

        self.rect.y += self.velocity[1]
        collisions = self.getCollisions(tiles)
        for tile in collisions:
            if self.velocity[1] > 0:
                self.rect.bottom = tile.top
                collision_types['bottom'] = True
                self.acceleration = [0,0]
            elif self.velocity[1] < 0:
                self.rect.top = tile.bottom
                collision_types['top'] = True
        
        