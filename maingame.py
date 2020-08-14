import pygame
import random

# Starts pygame
pygame.init()

# Defines general colours
SKY = (150, 240, 255)
GRASS = (126, 200, 80)
IVORY = (255, 255, 240)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Essentials for pygame
size = (960, 540)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("My Game")
done = False
clock = pygame.time.Clock()

# Sets general variables
key = 0

# Sets variables related to the player
binpositionx = 440
binpositiony = 410
binvelocityx = 0
binjump = 0
bintype = "garbage"

# Sets variables related to the item
wastepositionx = 0
wastepositiony = 0
wastehitbox = 20

wastespeed = 5

# -----Main Program-----
while not done:

    # Tracks user events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("User has quit the game.")
            done = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:  # Bin movement controls
                key = "Left"
            if event.key == pygame.K_RIGHT:
                key = "Right"
            if event.key == pygame.K_SPACE:
                key = "Space"
            if event.key == pygame.K_UP and binjump == 0:
                binjump = 32  # Sets binjump variable to 32, which times the jump
            if event.key == pygame.K_a:  # Bin swap controls
                bintype = "garbage"
            if event.key == pygame.K_s:
                bintype = "compost"
            if event.key == pygame.K_d:
                bintype = "recycling"

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:  # Bin movement controls
                if key == "Left":
                    key = 0
            if event.key == pygame.K_RIGHT:
                if key == "Right":
                    key = 0
            if event.key == pygame.K_SPACE:
                if key == "Space":
                    key = 0

    # Bin sucking ---
    # if key == "Space":
    # if |binpositionx - wastepositionx + wastehitbox/2| <= 10:
    # binpositiony -= stuff

    # Bin movement ---
    if key == "Left":  # Adds velocity leftward
        binvelocityx += -1.2
    if key == "Right":  # Adds velocity rightward
        binvelocityx += 1.2

    if binvelocityx >= -1 and binvelocityx <= 1:  # Velocity decays if already cloe to 0
        binvelocityx = 0
    if binvelocityx > 0:  # Velocity decays if positive
        binvelocityx -= 0.8
    if binvelocityx < 0:  # Velocity decays if negative
        binvelocityx += 0.8

    binpositionx += binvelocityx  # Move the bin sprite by the current velocity value
    if binpositionx < 10 and binvelocityx < 0:  # Bin sprite does not move past the left edge of the screen
        binpositionx = 10
    if binpositionx > 630 and binvelocityx > 0:  # Bin sprite does not move past the right edge of the screen
        binpositionx = 630

    # Bin jumps
    if binjump <= 32 and binjump >= 29:
        binpositiony -= 12
        binjump -= 1
    if binjump <= 28 and binjump >= 25:
        binpositiony -= 8
        binjump -= 1
    if binjump <= 24 and binjump >= 21:
        binpositiony -= 5
        binjump -= 1
    if binjump <= 20 and binjump >= 17:
        binpositiony -= 3
        binjump -= 1

    # Bin falls down after jump
    if binjump <= 16 and binjump >= 13:
        binpositiony += 3
        binjump -= 1
    if binjump <= 12 and binjump >= 9:
        binpositiony += 5
        binjump -= 1
    if binjump <= 8 and binjump >= 5:
        binpositiony += 8
        binjump -= 1
    if binjump <= 4 and binjump >= 1:
        binpositiony += 12
        binjump -= 1

    # Bin swap –––
    if key == "Garbage":  # Swaps bin to garbage
        bintype = "garbage"
    if key == "Compost":  # Swaps bin to garbage
        bintype = "compost"

    # Draws in the background sky and grass
    screen.fill(SKY)
    pygame.draw.rect(screen, GRASS, (0, 490, 960, 50), 0)
    pygame.draw.rect(screen, IVORY, (700, 0, 260, 960))

    # Draw bin sprite –––
    if bintype == "garbage":
        pygame.draw.rect(screen, RED, [binpositionx, binpositiony, 60, 80], 0)
    if bintype == "compost":
        pygame.draw.rect(screen, GREEN, [binpositionx, binpositiony, 60, 80], 0)
    if bintype == "recycling":
        pygame.draw.rect(screen, BLUE, [binpositionx, binpositiony, 60, 80], 0)

    # Updates screen
    pygame.display.flip()

    # 60 fps
    clock.tick(60)

# Quit
pygame.quit()
