import pygame
import random
BLACK = (0, 0, 0)

class SpriteSheet:
    def __init__(self,spriteSheetFile):
        """Load the sheet."""
        try:
            self.sheet = pygame.image.load(spriteSheetFile).convert()
        except pygame.error as e:
            print(f"Unable to load spritesheet image: {spriteSheetFile}")
            raise SystemExit(e)
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

class Room:
    def __init__(self,RoomFile,hasBottomExit,hasTopExit):
        self.RoomSpriteSheet = SpriteSheet("ProcedualGeneration/roomSpriteSheet.png")
        self.hasBottomExit = hasBottomExit
        self.hasTopExit = hasTopExit
        self.room = self.getRoom(RoomFile)
        
    def getRoomData(self,RoomFile):
        with open(RoomFile) as data:
            return data.read()

    def addImageToArray(self,room,imglocInSpriteSheet,TileLocation):
        room.append([self.RoomSpriteSheet.image_at(imglocInSpriteSheet,BLACK),TileLocation])
        return room

    def GetCoordinatesInSpriteSheet(self,ifNum,Checker,loc):#this uses recusion to find the location of the tile in the spritesheet
        if ifNum == Checker:
            return loc
        else:
            ifNum = int(ifNum) + 1
            if loc[0] == 64:
                loc[0] = 0
                loc[1] += 32
            else:
                loc[0] += 32
            return self.GetCoordinatesInSpriteSheet(str(ifNum),Checker,loc)

    def getRoom(self,roomFile):
        data = self.getRoomData(roomFile)
        room = []
        xCounter = -1
        yCounter = 0
        surfaceX = 0
        for tile in data:
            xCounter += 1
            if tile == '\n':
                if surfaceX < xCounter:
                    surfaceX = xCounter
                yCounter +=1
                xCounter =-1
            else:
                loc = self.GetCoordinatesInSpriteSheet('0',tile,[0,0,16,16])
                self.addImageToArray(room,loc,(xCounter*16,yCounter*16))
        surface = pygame.Surface((surfaceX*16,yCounter*16+16))
        return self.drawRoom(surface,room)
    def drawRoom(self, surface,room):
        for i in room:
            surface.blit(i[0], i[1])
        return surface


'''
a 1 room = a room with a left and right exit
a 2NoTop = a room with a left, right and bottom exit
a 2Top = a room witha  a left, right bottom and top exit
a 3 = a room with a left, right and top exit
'''
class World:
    rooms = []
    roomsToBlit = []
    currentPosition = [1,0]
    def __init__(self,roomAmount):
        self.roomAmount = roomAmount
        self.roomPaths = {
                        '1' : Room('ProcedualGeneration/rooms/1.txt',hasBottomExit=False,hasTopExit=False),
                        '2NoTop' : Room('ProcedualGeneration/rooms/2NoTop.txt',hasBottomExit=False,hasTopExit=False),
                        '2Top' : Room('ProcedualGeneration/rooms/2Top.txt',hasBottomExit=False,hasTopExit=False),
                        '3' : Room('ProcedualGeneration/rooms/3.txt',hasBottomExit=False,hasTopExit=False),
                        } 
        self.genWorld()
        
    def genWorld(self):
        for i in range(0,self.roomAmount):
            roomLength = 20
            roomHeight = 8
            xMultiplier = roomLength*16
            yMultiplier = roomHeight*16
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
                            room = [room[0]/xMultiplier,room[1]/yMultiplier]
                            if newPos == room:
                                newPos = [newPos[0]-1,newPos[1]]
                                findingEmptySpace = True
                                break
                if newPos[0] >= 0 and newPos[1] >= 0:
                    self.currentPosition = newPos
                    self.rooms.append([newPos[0]*xMultiplier,newPos[1]*yMultiplier])
                    self.roomsToBlit.append([self.roomPaths['1'].room,(newPos[0]*xMultiplier,newPos[1]*yMultiplier)])
            elif rndNum == 3 or rndNum ==4 :#right
                newPos = [self.currentPosition[0]+1,self.currentPosition[1]]
                while findingEmptySpace:
                    findingEmptySpace = False
                    if self.rooms == []:
                        break
                    for room in self.rooms:
                        room = [room[0]/xMultiplier,room[1]/yMultiplier]
                        if newPos == room:
                            newPos = [newPos[0]+1,newPos[1]]
                            findingEmptySpace = True
                            break
                if newPos[0] >= 0 and newPos[1] >= 0:
                    self.currentPosition = newPos
                    self.rooms.append([newPos[0]*xMultiplier,newPos[1]*yMultiplier])
                    self.roomsToBlit.append([self.roomPaths['1'].room,(newPos[0]*xMultiplier,newPos[1]*yMultiplier)])
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
                    self.rooms.append([newPos[0]*xMultiplier,newPos[1]*yMultiplier])
                    self.roomsToBlit.append([self.roomPaths['3'].room,(newPos[0]*xMultiplier,newPos[1]*yMultiplier)])
        
        '''
        there is a bug rigth now with the first couple of rooms so that needs fixing
        '''