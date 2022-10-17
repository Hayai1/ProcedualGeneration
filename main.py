
 

import pygame
from world import Room
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


Room1 = Room('rooms/1.txt','SpriteSheet.png',hasBottomExit=False,hasTopExit=False)
Room2Top = Room('rooms/2Top.txt','SpriteSheet.png',hasBottomExit=True,hasTopExit=True)
Room2NoTop = Room('rooms/2NoTop.txt','SpriteSheet.png',hasBottomExit=True,hasTopExit=False)
Room3 = Room('rooms/3.txt','SpriteSheet.png',hasBottomExit=False,hasTopExit=True)
# -------- Main Program Loop -----------
d1 = True
d2=False
d3=False
d4=False
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                d1= True
                d2=False
                d3=False
                d4=False
            if event.key == pygame.K_2:
                d1 = False
                d2=True
                d3=False
                d4=False
            if event.key == pygame.K_3:
                d1= False
                d2=False
                d3=True
                d4=False
            if event.key == pygame.K_4:
                d1= False
                d2=False
                d3=False
                d4=True
    screen.fill(WHITE)
    
    x,y = pygame.mouse.get_pos()
    # --- Limit to 60 frames per second
    if d1:
        screen.blit(Room1.room,(x,y))
    elif d2:
        screen.blit(Room2Top.room,(x,y))
    elif d3:
        screen.blit(Room2NoTop.room,(x,y))
    elif d4:
        screen.blit(Room3.room,(x,y))
    pygame.display.update()
    clock.tick(60)

# Close the window and quit.
pygame.quit()