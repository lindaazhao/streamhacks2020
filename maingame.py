import pygame
import random

#Initialize game elements
pygame.init()
size = (960, 540)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("My Game")
done = False
clock = pygame.time.Clock()

#Defines general colours
SKY = (150, 240, 255)
GRASS = (126, 200, 80)
IVORY = (255, 255, 240)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

#Sets general variables
key = 0
start = 0
level = 0
paused = 0

#Sets graphics
#lockscreen = pygame.image.load('Lock Screen.png')

#Sets variables related to the player
binpositionx = 320
binpositiony = 410
binvelocityx = 0
binjump = 0
bintype = "garbage"
lidOpen = False
binSucc = False


#-----EVERYTHING WASTE-----
class Waste:
    # Type --> garbage, recycling or compost
    # Name --> exact name of piece of waste
    def __init__(self, wasteID, wasteX, wasteY, wasteSpeed, wasteWidth, wasteHeight):
        self.ID = wasteID
        self.x = wasteX
        self.y = wasteY
        self.speed = wasteSpeed
        self.width = wasteWidth
        self.height = wasteHeight

    def draw(self):
      if self.ID == 1:
        wasteType = wasteGraphics[self.ID - 1]
      if self.ID == 2:
        wasteType = wasteGraphics[self.ID - 1]
      screen.blit(wasteType, (int(self.x), int(self.y)))


waste_list = []
remove_waste = []
waste_widths = [35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35]
waste_heights = [35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35]
waste_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
wasteGraphics = [pygame.transform.scale(pygame.image.load('img/garb1.jpg'), (waste_widths[0], waste_heights[0]))]
                 #pygame.transform.scale(pygame.image.load('img/garb2.jpg'), (waste_widths[1], waste_heights[1])),
                 #pygame.transform.scale(pygame.image.load('img/garb3.jpg'), (waste_widths[2], waste_heights[2])),
                 #pygame.transform.scale(pygame.image.load('img/garb4.jpg'), (waste_widths[3], waste_heights[3])),
                 #pygame.transform.scale(pygame.image.load('img/garb5.jpg'), (waste_widths[4], waste_heights[4])),
                 #pygame.transform.scale(pygame.image.load('img/garb6.jpg'), (waste_widths[5], waste_heights[5])),
                 #pygame.transform.scale(pygame.image.load('img/garb7.jpg'), (waste_widths[6], waste_heights[6])),
                 #pygame.transform.scale(pygame.image.load('img/garb8.jpg'), (waste_widths[7], waste_heights[7])),
                 #pygame.transform.scale(pygame.image.load('img/garb9.jpg'), (waste_widths[8, waste_heights[8])),
                 #pygame.transform.scale(pygame.image.load('img/garb10.jpg'), (waste_widths[9], waste_heights[9])),
                 #pygame.transform.scale(pygame.image.load('img/garb11.jpg'), (waste_widths[10], waste_heights[10])),
                 #pygame.transform.scale(pygame.image.load('img/garb12.jpg'), (waste_widths[11], waste_heights[11])),
                 #pygame.transform.scale(pygame.image.load('img/garb13.jpg'), (waste_widths[12], waste_heights[12])),
                 #pygame.transform.scale(pygame.image.load('img/garb14.jpg'), (waste_widths[13], waste_heights[13])),
                 #pygame.transform.scale(pygame.image.load('img/garb15.jpg'), (waste_widths[14], waste_heights[14])),
                 #pygame.transform.scale(pygame.image.load('img/garb16.jpg'), (waste_widths[15], waste_heights[15])),
                 #pygame.transform.scale(pygame.image.load('img/garb17.jpg'), (waste_widths[16], waste_heights[16])),
                 #pygame.transform.scale(pygame.image.load('img/garb18.jpg'), (waste_widths[17], waste_heights[17]))]

#-------Title Screen-------
while not done and start == 0:

    #Tracks user events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("User has quit the game.")
            done = True
        if event.type == pygame.KEYDOWN:
            start = 1

    #Displays graphics
    screen.fill(IVORY)
    # screen.blit(lockscreen, (0, 0))
    pygame.display.flip()
    clock.tick(60)

#-------Main Program-------
while not done and start == 1:

    #Tracks user events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("User has quit the game.")
            done = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: #Bin movement controls
                key = "Left"
            if event.key == pygame.K_RIGHT:
                key = "Right"
            if event.key == pygame.K_SPACE:
                binSucc = True
                velocityx = 0
                lidOpen = True
            if event.key == pygame.K_UP and binjump == 0:
                binjump = 32 #Sets binjump variable to 32, which times the jump
            if event.key == pygame.K_a: #Bin swap controls
                bintype = "garbage"
            if event.key == pygame.K_s:
                bintype = "compost"
            if event.key == pygame.K_d:
                bintype = "recycling"
            if event.key == pygame.K_w:
                newWaste = Waste(1, random.randint(250,665), 50, 2, 35, 35)
                waste_list.append(newWaste)
                print(waste_list)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT: #Bin movement controls
                if key == "Left":
                    key = 0
            if event.key == pygame.K_RIGHT:
                if key == "Right":
                    key = 0
            if event.key == pygame.K_SPACE:
                binSucc = False

    if binSucc:
      velocityx = 0
      for i in range(len(waste_list)):
        waste = waste_list[i]
        if abs(waste.x+(waste.width/2) - (binpositionx + 30)) <= 30:
          waste.y += 3
          if waste.y >= binpositiony:
            remove_waste.append(waste)
      for i in remove_waste:
        if i in waste_list:
          waste_list.remove(i)

    #Bin movement ---
    if key == "Left": #Adds velocity leftward
        binvelocityx += -1.2
    if key == "Right": #Adds velocity rightward
        binvelocityx += 1.2

    if binvelocityx >= -1 and binvelocityx <= 1: #Velocity decays if already cloe to 0
        binvelocityx = 0
    if binvelocityx > 0: #Velocity decays if positive
        binvelocityx -= 0.9
    if binvelocityx < 0: #Velocity decays if negative
        binvelocityx += 0.9

    binpositionx += binvelocityx #Move the bin sprite by the current velocity value
    if binpositionx < 10 and binvelocityx < 0: #Bin sprite does not move past the left edge of the screen
        binpositionx = 10
    if binpositionx > 630 and binvelocityx > 0: #Bin sprite does not move past the right edge of the screen
        binpositionx = 630

    if binjump <= 32 and binjump >= 29: #Bin jumps up
        binpositiony -= 13
        binjump -= 1
    if binjump <= 28 and binjump >= 25:
        binpositiony -= 9
        binjump -= 1
    if binjump <= 24 and binjump >= 21:
        binpositiony -= 6
        binjump -= 1
    if binjump <= 20 and binjump >= 17:
        binpositiony -= 4
        binjump -= 1

    if binjump <= 16 and binjump >= 13: #Bin falls down
        binpositiony += 4
        binjump -= 1
    if binjump <= 12 and binjump >= 9:
        binpositiony += 6
        binjump -= 1
    if binjump <= 8 and binjump >= 5:
        binpositiony += 9
        binjump -= 1
    if binjump <= 4 and binjump >= 1:
        binpositiony += 13
        binjump -= 1

    #Bin swap –––
    if key == "Garbage": #Swaps bin to garbage
        bintype = "garbage"
    if key == "Compost": #Swaps bin to garbage
        bintype = "compost"

    #Draws in the background sky and grass
    screen.fill(SKY)
    pygame.draw.rect(screen, GRASS, (0, 490, 960, 50), 0)
    pygame.draw.rect(screen, IVORY, (700, 0, 260, 960))

    #Draw bin sprite –––
    if bintype == "garbage":
        pygame.draw.rect(screen, RED, [binpositionx, binpositiony, int(60), int(80)], int(0))
    if bintype == "compost":
        pygame.draw.rect(screen, GREEN, [binpositionx, binpositiony, int(60), int(80)], int(0))
    if bintype == "recycling":
        pygame.draw.rect(screen, BLUE, [binpositionx, binpositiony, int(60), int(80)], int(0))
    
    for i in range(len(waste_list)):
      waste = waste_list[i]
      waste.y += waste.speed
      waste.draw()

    #Updates screen
    pygame.display.flip()

    #60 fps
    clock.tick(60)

#Quit
pygame.quit()
