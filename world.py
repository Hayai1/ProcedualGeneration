from os import getrandom
import pygame
import random
from copy import deepcopy
BLACK = (0, 0, 0)

class SpriteSheet:
    


    def image_at(self, rectangle, colorkey = None):
        """Load a specific image from a specific rectangle."""
        # Loads image from x, y, x+offset, y+offset.
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    def images_at(self, rects, colorkey = None):
        """Load a whole bunch of images and return them as a list."""
        return [self.image_at(rect, colorkey) for rect in rects]

    def load_strip(self, rect, image_count, colorkey = None):
        """Load a whole strip of images, and return them as a list."""
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)

    



class Room(SpriteSheet):
    def __init__(self, RoomFile,spriteSheetFile,hasBottomExit,hasTopExit):
        """Load the sheet."""
        try:
            self.sheet = pygame.image.load(spriteSheetFile).convert()
        except pygame.error as e:
            print(f"Unable to load spritesheet image: {spriteSheetFile}")
            raise SystemExit(e)
        self.room = self.getRoom(RoomFile)
        self.hasBottomExit = hasBottomExit
        self.hasTopExit = hasTopExit

    def getRoomData(self,RoomFile):
        with open(RoomFile) as data:
            return data.read()


    def getRoom(self,roomFile):
        room = []
        data = self.getRoomData(roomFile)
        xCounter = -1
        yCounter = 0
        surfaceX = 0
        for tile in data:
            xCounter += 1
            if tile == '0':
                room.append([self.image_at((0,0,16,16),BLACK),(xCounter*16,yCounter*16)])
            elif tile == '1':
                room.append([self.image_at((32,0,16,16),BLACK),(xCounter*16,yCounter*16)])
            elif tile == '2':
                room.append([self.image_at((64,0,16,16),BLACK),(xCounter*16,yCounter*16)])
            elif tile == '3':
                room.append([self.image_at((0,32,16,16),BLACK), (xCounter*16,yCounter*16)])
            elif tile == '4':
                room.append([self.image_at((32,32,16,16),BLACK), (xCounter*16,yCounter*16)])
            elif tile == '5':
                room.append([self.image_at((64,32,16,16),BLACK), (xCounter*16,yCounter*16)])
            elif tile == '6':
                room.append([self.image_at((0,64,16,16),BLACK), (xCounter*16,yCounter*16)])
            elif tile == '7':
                room.append([self.image_at((32,64,16,16),BLACK), (xCounter*16,yCounter*16)])
            elif tile == '8':
                room.append([self.image_at((64,64,16,16),BLACK), (xCounter*16,yCounter*16)])
            elif tile == '9':
                room.append([self.image_at((128,32,16,16),BLACK), (xCounter*16,yCounter*16)])     
            elif tile == '\n':
                if surfaceX < xCounter:
                    surfaceX = xCounter
                yCounter +=1
                xCounter =-1

        surface = pygame.Surface((surfaceX*16,yCounter*16+16))
        return self.drawRoom(surface,room)
            
    def drawRoom(self, surface,room):
        for i in room:
            surface.blit(i[0], i[1])
        return surface
    
class mapGenerator:
    level = []
    currentPos = []
    MAPWIDTH = 4
    MAPHEIGHT = 4
    def __init__(self, spriteSheet,Room1='1.txt', Room2WithTop='2Top.txt', Room2WithNoTop='2NoTop.txt', Room3='3.txt'):
        self.Room1          = Room(Room1          ,spriteSheet ,False ,False)
        self.Room2WithTop   = Room(Room2WithTop   ,spriteSheet ,True  ,True )
        self.Room2WithNoTop = Room(Room2WithNoTop ,spriteSheet ,True  ,False)
        self.Room3          = Room(Room3          ,spriteSheet ,False ,False)
        self.generateNewLevel()


    def getRandomNumber(self,a,b):
        return random.randint(a,b)


    def generateNewLevel(self):
        StartRoomNum = self.getRandomNumber(1,2)
        if StartRoomNum == 1:
            startRoom = deepcopy(self.Room1)
        elif StartRoomNum == 2:
            startRoom = deepcopy(self.Room2WithNoTop)
        self.currentPos = [StartRoomNum,0]
        self.level.append(currentLevel)
        nextLoc = self.getRandomNumber(1,5)
        moveLeft = False
        moveRight = False
        moveDown = False
        if (nextLoc == 1 or nextLoc == 2):  
            if self.currentPos[0] > 3:
                moveRight = True
                moveDown = True
            else:
                moveLeft = True
        elif (nextLoc == 3 or nextLoc == 4):
            if self.currentPos[0] > 3:
                moveDown = True
                moveLeft=True
            else:
                moveRight = True
        elif (nextLoc == 5):
            if self.currentPos[1] > 3:
                pass
            else:
                moveDown = True
        if (moveRight):
            newCurrentPos = [self.currentPos[0]+1,self.currentPos[1]]
        if (moveLeft):
            newCurrentPos = [self.currentPos[0]-1,self.currentPos[1]]
        if (moveDown):
            if (not currentLevel.hasBottomExit):#change the room so that it has a bottom exit
                if (currentLevel.hasTopExit):
                    currentLevel = deepcopy(self.Room2WithTop)
                else: 
                    currentLevel = deepcopy(self.Room2WithNoTop)
            newCurrentPos = [self.currentPos[0],self.currentPos[1]-1]
        self.level.append([currentLevel, self.currentPos])
        self.currentPos = newCurrentPos
        '''
        TODO test this
        then work more from http://tinysubversions.com/spelunkyGen/
        '''

