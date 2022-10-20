

import pygame
import random


from world import Room
# Define some colors
pygame.init()
 
# Set the width and height of the screen [width, height]
size = (700, 500)
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("My Game")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates

clock = pygame.time.Clock()
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ROOMPATHS = {
    '1' : Room('ProcedualGeneration/rooms/1.txt','ProcedualGeneration/SpriteSheet.png',hasBottomExit=False,hasTopExit=False),
    '2NoTop' : Room('ProcedualGeneration/rooms/2NoTop.txt','ProcedualGeneration/SpriteSheet.png',hasBottomExit=False,hasTopExit=False),
    '2Top' : Room('ProcedualGeneration/rooms/2Top.txt','ProcedualGeneration/SpriteSheet.png',hasBottomExit=False,hasTopExit=False),
    '3' : Room('ProcedualGeneration/rooms/3.txt','ProcedualGeneration/SpriteSheet.png',hasBottomExit=False,hasTopExit=False),
} 
Surface = pygame.Surface((50*320,50*96))


class worldGeneration:
    rooms = []
    roomsToBlit = []
    currentPosition = [1,0]
    def __init__(self,roomAmount):
        self.roomAmount = roomAmount
        
    def genWorld(self):
        for i in range(0,self.roomAmount):
            a = 96
            b = 320
            rndNum = random.randint(1,5)
            #rndNumDown = random.randint(1,2)
            #rndNumup = random.randint(1,5)
            findingEmptySpace = True
            if rndNum == 1 or rndNum == 2:#left
                newPos = [self.currentPosition[0]-1,self.currentPosition[1]]
                while findingEmptySpace:
                    while findingEmptySpace:
                        findingEmptySpace = False
                        if self.rooms == []:
                            break
                        for room in self.rooms:
                            room = [room[0]/b,room[1]/a]
                            if newPos == room:
                                print("dfs")
                                newPos = [newPos[0]-1,newPos[1]]
                                findingEmptySpace = True
                                break
                        
                
                if newPos[0] >= 0 and newPos[1] >= 0:
                    self.currentPosition = newPos
                    self.rooms.append([newPos[0]*b,newPos[1]*a])
                    self.roomsToBlit.append([ROOMPATHS['1'].room,(newPos[0]*b,newPos[1]*a)])
            
            elif rndNum == 3 or rndNum ==4 :#right
                newPos = [self.currentPosition[0]+1,self.currentPosition[1]]
                while findingEmptySpace:
                    findingEmptySpace = False
                    if self.rooms == []:
                        break
                    for room in self.rooms:
                        room = [room[0]/b,room[1]/a]
                        if newPos == room:
                            print("dfs")

                            newPos = [newPos[0]+1,newPos[1]]
                            findingEmptySpace = True
                            break
   
                if newPos[0] >= 0 and newPos[1] >= 0:
                    self.currentPosition = newPos
                    self.rooms.append([newPos[0]*b,newPos[1]*a])
                    self.roomsToBlit.append([ROOMPATHS['1'].room,(newPos[0]*b,newPos[1]*a)])
            elif rndNum == 5:#down
                newPos = [self.currentPosition[0],self.currentPosition[1]+1]
                while findingEmptySpace:
                    findingEmptySpace = False
                    if self.rooms == []:
                        break
                    for room in self.rooms:
                        if newPos == room:
                            newPos = [newPos[0],newPos[1]+1]
                            findingEmptySpace = True
                            break
                        
                if newPos[0] >= 0 and newPos[1] >= 0:
                    if len(self.roomsToBlit)-2 > 0:
                        aboveRoom = self.roomsToBlit[len(self.roomsToBlit)-1]
                        if aboveRoom[0] == ROOMPATHS['1'].room:
                            self.roomsToBlit[len(self.roomsToBlit)-1][0] = ROOMPATHS['2NoTop'].room
                        elif aboveRoom[0] == ROOMPATHS['3'].room:
                            self.roomsToBlit[len(self.roomsToBlit)-1][0] = ROOMPATHS['2Top'].room
                    self.currentPosition = newPos
                    self.rooms.append([newPos[0]*b,newPos[1]*a])
                    self.roomsToBlit.append([ROOMPATHS['3'].room,(newPos[0]*b,newPos[1]*a)])
            print(newPos)
            '''
            elif rndNum == 10 and rndNumup == 2:#up
                newPos = [self.currentPosition[0],self.currentPosition[1]-1]
                while findingEmptySpace:
                    if self.rooms == []:
                        break
                    for room in self.rooms:
                        if newPos == room:
                            newPos = [newPos[0],newPos[1]-1]
                        else:
                            findingEmptySpace = False
                            break
                if newPos[0] >= 0 and newPos[1] >= 0:
                    self.currentPosition = newPos
                    self.rooms.append([newPos[0]*b,newPos[1]*a])
                    self.roomsToBlit.append([ROOMPATHS['2NoTop'].room,(newPos[0]*b,newPos[1]*a)])
            '''


worldgen = worldGeneration(50)
worldgen.genWorld()
frame = 0
WorldGenDone = False
counter = 1
x = 0
y = 0
left = False
Right= False
Up = False
down = False
# -------- Main Program Loop -----------
while not done:
    screen.fill(BLACK)
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                left = True
            if event.key == pygame.K_RIGHT:
                Right = True
            if event.key == pygame.K_DOWN:
                down = True
            if event.key == pygame.K_UP:
                Up = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                left = False

            if event.key == pygame.K_RIGHT:
                Right= False

            if event.key == pygame.K_DOWN:
                down = False

            if event.key == pygame.K_UP:
                Up = False

    if left:
        x=x+50
    if Right:
        x = x - 50
    if down:
        y = y -50
    if Up:
        y = y + 50
    Surface.fill(WHITE)
    frame += 1

    
    for room in worldgen.roomsToBlit:
        Surface.blit(room[0],room[1])
    pygame.draw.lines(Surface,RED,False,worldgen.rooms)
    
    for i in worldgen.rooms:
        pygame.draw.rect(Surface, GREEN,pygame.Rect(i[0],i[1],5,5))

    #y=y-1
    screen.blit(Surface,(x,y))
    # --- Limit to 60 frames per second
    pygame.display.update()
    clock.tick(60)
    
# Close the window and quit.
pygame.quit()