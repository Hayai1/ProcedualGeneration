from contextlib import nullcontext
import pygame
import random
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
 
pygame.init()
 
# Set the width and height of the screen [width, height]
size = (700, 500)
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("My Game")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
class Room:
    def __init__(self,position) -> None:
        self.position = position


class worldGeneration:
    rooms = []
    currentPosition = [400,0]
    def __init__(self,roomAmount):
        self.roomAmount = roomAmount
        
    def genWorld(self):
            rndNum = random.randint(1,10)
            rndNumDown = random.randint(1,2)
            rndNumup = random.randint(1,5)
            findingEmptySpace = True
            if rndNum == 1 or rndNum == 2 or rndNum == 3 or rndNum == 4:#left
                newPos = [self.currentPosition[0]-10,self.currentPosition[1]]
                while findingEmptySpace:
                    if self.rooms == []:
                        break
                    for room in self.rooms:
                        if newPos == room:
                            newPos = [newPos[0]-10,newPos[1]]
                        else:
                            findingEmptySpace = False
                            break
                self.currentPosition = newPos
                self.rooms.append(newPos)
            elif rndNum == 5 or rndNum == 6 or rndNum == 7 or rndNum == 8:#right
                newPos = [self.currentPosition[0]+10,self.currentPosition[1]]
                while findingEmptySpace:
                    if self.rooms == []:
                        break
                    for room in self.rooms:
                        if newPos == room:
                            newPos = [newPos[0]+10,newPos[1]]
                        else:
                            findingEmptySpace = False
                            break
                self.currentPosition = newPos
                self.rooms.append(newPos)
            elif rndNum == 9 and rndNumDown == 1:#down
                newPos = [self.currentPosition[0],self.currentPosition[1]+10]
                while findingEmptySpace:
                    if self.rooms == []:
                        break
                    for room in self.rooms:
                        if newPos == room:
                            newPos = [newPos[0],newPos[1]+10]
                        else:
                            findingEmptySpace = False
                            break
                self.currentPosition = newPos
                self.rooms.append(newPos)
            
            elif rndNum == 10 and rndNumup == 2:#up
                newPos = [self.currentPosition[0],self.currentPosition[1]-10]
                while findingEmptySpace:
                    if self.rooms == []:
                        break
                    for room in self.rooms:
                        if newPos == room:
                            newPos = [newPos[0],newPos[1]-10]
                        else:
                            findingEmptySpace = False
                            break
                self.currentPosition = newPos
                self.rooms.append(newPos)
                


worldgen = worldGeneration(300)
worldgen.genWorld()
worldgen.genWorld()
print(worldgen.rooms)
# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
 
    screen.fill(WHITE)
    pygame.draw.lines(screen,RED,False,worldgen.rooms)
    worldgen.genWorld()
    print(len(worldgen.rooms))
    '''if len(worldgen.rooms) > 500:
        worldgen.rooms = []
        worldgen.currentPosition = [400,0]
        worldgen.genWorld()
        worldgen.genWorld()'''
    pygame.display.flip()
    
    # --- Limit to 60 frames per second
    clock.tick(60)
 
# Close the window and quit.
pygame.quit()