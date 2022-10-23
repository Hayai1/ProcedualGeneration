import pygame
from world import World
from player import Player
WINDOW_SIZE = (1920,1080)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
Surface = pygame.Surface((300,200))
worldgen = World(50)
player = Player(0,0)
 
done = False
x = 0
y = 0
left = False
Right= False
Up = False
down = False
true_scroll = [0,0]

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
                
    true_scroll[0] += (x-true_scroll[0])
    true_scroll[1] += (y-true_scroll[1])
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    if left:
        x=x-10
    if Right:
        x = x + 10
    if down:
        y = y +10
    if Up:
        y = y - 10
    Surface.fill(WHITE)
    

    for room in worldgen.rooms:
        Surface.blit(room.roomImg,(room.x-scroll[0],room.y-scroll[1]))
        for rect in room.rects:
           pygame.draw.rect(Surface,RED,pygame.Rect(rect.x-scroll[0],rect.y-scroll[1],rect.width,rect.height))
    
    pygame.draw.rect(Surface,(0,0,255),player.rect)

    screen.blit(pygame.transform.scale(Surface,WINDOW_SIZE),(0,0))
    
    # --- Limit to 60 frames per second
    pygame.display.update()
    clock.tick(60)
    
# Close the window and quit.
pygame.quit()