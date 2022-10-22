import pygame
import random
BLACK = (0, 0, 0)

class SpriteSheet:
    def image_at(self, rectangle, colorkey = None):
        """Load a specific image from a specific rectangle."""
        # Loads image from x, y, x+offset, y+offset.
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey == -1:
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
    

class worldGeneration:
    
    rooms = []
    roomsToBlit = []
    currentPosition = [1,0]
    def __init__(self,roomAmount):
        self.roomAmount = roomAmount
        self.roomPaths = {
    '1' : Room('ProcedualGeneration/rooms/1.txt','ProcedualGeneration/SpriteSheet.png',hasBottomExit=False,hasTopExit=False),
    '2NoTop' : Room('ProcedualGeneration/rooms/2NoTop.txt','ProcedualGeneration/SpriteSheet.png',hasBottomExit=False,hasTopExit=False),
    '2Top' : Room('ProcedualGeneration/rooms/2Top.txt','ProcedualGeneration/SpriteSheet.png',hasBottomExit=False,hasTopExit=False),
    '3' : Room('ProcedualGeneration/rooms/3.txt','ProcedualGeneration/SpriteSheet.png',hasBottomExit=False,hasTopExit=False),
    } 
        
    def genWorld(self):
        for i in range(0,self.roomAmount):
            a = 96
            b = 320
            rndNum = random.randint(1,5)
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
                                newPos = [newPos[0]-1,newPos[1]]
                                findingEmptySpace = True
                                break
                if newPos[0] >= 0 and newPos[1] >= 0:
                    self.currentPosition = newPos
                    self.rooms.append([newPos[0]*b,newPos[1]*a])
                    self.roomsToBlit.append([self.roomPaths['1'].room,(newPos[0]*b,newPos[1]*a)])
            elif rndNum == 3 or rndNum ==4 :#right
                newPos = [self.currentPosition[0]+1,self.currentPosition[1]]
                while findingEmptySpace:
                    findingEmptySpace = False
                    if self.rooms == []:
                        break
                    for room in self.rooms:
                        room = [room[0]/b,room[1]/a]
                        if newPos == room:

                            newPos = [newPos[0]+1,newPos[1]]
                            findingEmptySpace = True
                            break
                if newPos[0] >= 0 and newPos[1] >= 0:
                    self.currentPosition = newPos
                    self.rooms.append([newPos[0]*b,newPos[1]*a])
                    self.roomsToBlit.append([self.roomPaths['1'].room,(newPos[0]*b,newPos[1]*a)])
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
                        if aboveRoom[0] == self.roomPaths['1'].room:
                            self.roomsToBlit[len(self.roomsToBlit)-1][0] = self.roomPaths['2NoTop'].room
                        elif aboveRoom[0] == self.roomPaths['3'].room:
                            self.roomsToBlit[len(self.roomsToBlit)-1][0] = self.roomPaths['2Top'].room
                    self.currentPosition = newPos
                    self.rooms.append([newPos[0]*b,newPos[1]*a])
                    self.roomsToBlit.append([self.roomPaths['3'].room,(newPos[0]*b,newPos[1]*a)])
        
        '''
        there is a bug rigth now with the first couple of rooms so that needs fixing
        '''