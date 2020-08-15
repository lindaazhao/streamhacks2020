import pygame
import random
from pygame import mixer

# Initialize game elements
pygame.init()
size = (960, 540)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("My Game")
done = False
clock = pygame.time.Clock()

# Defines general colours
SKY = (150, 240, 255)
GRASS = (126, 200, 80)
IVORY = (255, 255, 240)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Sets general variables
key = 0
start = 0
level = 1
paused = 0
wasteSpawnTimer = 0
cloudSpawnTimer = 0
score = 0
score_threshold = 15
font = pygame.font.SysFont('Arial', 25)

# Gameplay music
mixer.music.load('sound/fallguys.mp3')
mixer.music.play(-1)

# Sound effect
succ_sound = mixer.Sound("sound/laserbeam.wav")
switch_sound = mixer.Sound("sound/switch.wav")
levelup_sound = mixer.Sound("sound/levelup.wav")
negative_sound = mixer.Sound("sound/negative.wav")
intake_sound = mixer.Sound("sound/intake.wav")
move_sound = mixer.Sound("sound/grass.wav")

# Sets graphics for bins

garbagebot = pygame.transform.scale(pygame.image.load('img/bins/garbagebot.png'), (60, 80))
garbagetopclose = pygame.transform.scale(pygame.image.load('img/bins/garbagetopclose.png'), (60, 13))
garbagetopopen = pygame.transform.scale(pygame.image.load('img/bins/garbagetopopen.png'), (60, 50))
compostbot = pygame.transform.scale(pygame.image.load('img/bins/compostbot.png'), (60, 80))
composttopclose = pygame.transform.scale(pygame.image.load('img/bins/composttopclose.png'), (60, 13))
composttopopen = pygame.transform.scale(pygame.image.load('img/bins/composttopopen.png'), (60, 50))
recyclebot = pygame.transform.scale(pygame.image.load('img/bins/recyclebot.png'), (60, 80))
recycletopclose = pygame.transform.scale(pygame.image.load('img/bins/recycletopclose.png'), (60, 13))
recycletopopen = pygame.transform.scale(pygame.image.load('img/bins/recycletopopen.png'), (60, 50))

# Sets graphics for screens
lockscreen = pygame.image.load('img/screens/Lock Screen.png')
level1 = pygame.image.load('img/screens/Level 1.png')
level2 = pygame.image.load('img/screens/Level 2.png')
level3 = pygame.image.load('img/screens/Level 3.png')
level4 = pygame.image.load('img/screens/Level 4.png')
level5 = pygame.image.load('img/screens/Level 5.png')
endscreen = pygame.image.load('img/screens/End Screen.png')

# Sets variables related to the player
binpositionx = 320
binpositiony = 410
binvelocityx = 0
bintype = "garbage"
binSucc = False


# -----EVERYTHING WASTE-----
class Waste:
    def __init__(self, wasteID, wasteX, wasteY, wasteSpeed, wasteWidth, wasteHeight):
        self.ID = wasteID
        self.x = wasteX
        self.y = wasteY
        self.speed = wasteSpeed
        self.width = wasteWidth
        self.height = wasteHeight

    def draw(self):
        wasteType = wasteGraphics[self.ID - 1]
        screen.blit(wasteType, (int(self.x), int(self.y)))


waste_list = []
remove_waste = []
waste_pool = [1, 2]  # List of waste items eligible to be spawned in the round
waste_randomizer = 0  # A random number drawn from waste_pool
waste_widths = [40, 50, 50, 50, 50, 40, 50, 30, 50, 50, 50, 48, 40, 40, 20, 20, 40, 23]
waste_heights = [40, 25, 25, 25, 31, 40, 25, 45, 25, 30, 40, 45, 40, 40, 40, 40, 40, 40]
waste_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
wasteGraphics = [pygame.transform.scale(pygame.image.load('img/waste/garb1.png'), (waste_widths[0], waste_heights[0])),
                 pygame.transform.scale(pygame.image.load('img/waste/garb2.png'), (waste_widths[1], waste_heights[1])),
                 pygame.transform.scale(pygame.image.load('img/waste/garb3.png'), (waste_widths[2], waste_heights[2])),
                 pygame.transform.scale(pygame.image.load('img/waste/garb4.png'), (waste_widths[3], waste_heights[3])),
                 pygame.transform.scale(pygame.image.load('img/waste/garb5.png'), (waste_widths[4], waste_heights[4])),
                 pygame.transform.scale(pygame.image.load('img/waste/garb6.png'), (waste_widths[5], waste_heights[5])),
                 pygame.transform.scale(pygame.image.load('img/waste/garb7.png'), (waste_widths[6], waste_heights[6])),
                 pygame.transform.scale(pygame.image.load('img/waste/garb8.png'), (waste_widths[7], waste_heights[7])),
                 pygame.transform.scale(pygame.image.load('img/waste/garb9.png'), (waste_widths[8], waste_heights[8])),
                 pygame.transform.scale(pygame.image.load('img/waste/garb10.png'), (waste_widths[9], waste_heights[9])),
                 pygame.transform.scale(pygame.image.load('img/waste/garb11.png'),
                                        (waste_widths[10], waste_heights[10])),
                 pygame.transform.scale(pygame.image.load('img/waste/garb12.png'),
                                        (waste_widths[11], waste_heights[11])),
                 pygame.transform.scale(pygame.image.load('img/waste/garb13.png'),
                                        (waste_widths[12], waste_heights[12])),
                 pygame.transform.scale(pygame.image.load('img/waste/garb14.png'),
                                        (waste_widths[13], waste_heights[13])),
                 pygame.transform.scale(pygame.image.load('img/waste/garb15.png'),
                                        (waste_widths[14], waste_heights[14])),
                 pygame.transform.scale(pygame.image.load('img/waste/garb16.png'),
                                        (waste_widths[15], waste_heights[15])),
                 pygame.transform.scale(pygame.image.load('img/waste/garb17.png'),
                                        (waste_widths[16], waste_heights[16])),
                 pygame.transform.scale(pygame.image.load('img/waste/garb18.png'),
                                        (waste_widths[17], waste_heights[17]))]


# -----EVERYTHING CLOUDS-----
class Cloud:
    def __init__(self, cloudID, cloudX, cloudY, cloudSpeed):
        self.ID = cloudID
        self.x = cloudX
        self.y = cloudY
        self.speed = cloudSpeed

    def draw(self):
        screen.blit(cloudGraphics[self.ID], (int(self.x), int(self.y)))


cloud_list = []
cloud_widths = [70, 90, 120, 150]
cloud_heights = [70, 80, 100, 160]
remove_cloud = []
cloud_randomizer = 0  # A random number drawn from cloud pool
cloudGraphics = [pygame.transform.scale(pygame.image.load('img/cloud.png'), (cloud_widths[0], cloud_heights[0])),
                 pygame.transform.scale(pygame.image.load('img/cloud.png'), (cloud_widths[1], cloud_heights[1])),
                 pygame.transform.scale(pygame.image.load('img/cloud.png'), (cloud_widths[2], cloud_heights[2])),
                 pygame.transform.scale(pygame.image.load('img/cloud.png'), (cloud_widths[3], cloud_heights[3]))]

# -------Title Screen-------
while not done and start == 0:

    # Tracks user events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("User has quit the game.")
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                start = 1
                paused = 1

    # Displays graphics
    screen.fill(IVORY)
    screen.blit(lockscreen, (0, 0))
    pygame.display.flip()
    clock.tick(60)

# -------Main Program-------

while not done and start == 1:

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
                binSucc = True
                succ_sound.play()
            if event.key == pygame.K_a:  # Bin swap controls
                if bintype != "garbage":
                    switch_sound.play()
                bintype = "garbage"
            if event.key == pygame.K_s and level >= 2:
                if bintype != "compost":
                    switch_sound.play()
                bintype = "compost"
            if event.key == pygame.K_d and level >= 3:
                if bintype != "recycling":
                    switch_sound.play()
                bintype = "recycling"

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:  # Bin movement controls
                if key == "Left":
                    key = 0
            if event.key == pygame.K_RIGHT:
                if key == "Right":
                    key = 0
            if event.key == pygame.K_SPACE:
                binSucc = False
                succ_sound.stop()

    # Bin succ ----
    if binSucc:
        for i in range(len(waste_list)):
            waste = waste_list[i]
            if abs(waste.x + (waste.width / 2) - (
                    binpositionx + 30)) <= 30:  # Checks if waste x-position is within range of the bin
                waste.y += 3
                if waste.y >= binpositiony and waste.y <= (
                        binpositiony + 40):  # Checks if waste y-position is within range of the bin
                    remove_waste.append(waste)
                    intake_sound.play()
                    if (bintype == "garbage" and waste.ID in range(1, 7)) or (
                            bintype == "compost" and waste.ID in range(7, 13)) or (
                            bintype == "recycling" and waste.ID in range(13,
                                                                         19)):  # Checks if waste type corresponds to bin type
                        score += 1
                    else:
                        if score > 0:
                            score -= 1
                            switch_sound.negative()
        for i in remove_waste:
            if i in waste_list:
                waste_list.remove(i)

    # Bin movement ---
    if key == "Left" and binSucc == False:  # Adds velocity leftward, normal speed
        binvelocityx += -1.2
    if key == "Right" and binSucc == False:  # Adds velocity rightward, normal speed
        binvelocityx += 1.2
    if key == "Left" and binSucc == True:  # Adds velocity leftward, succ speed
        binvelocityx += -0.935
    if key == "Right" and binSucc == True:  # Adds velocity rightward, succ speed
        binvelocityx += 0.935

    if binSucc == True and binvelocityx > 2.4:  # Sets a cap on rightward velocity at 2.4 while succing
        binvelocityx = 2.4
    if binSucc == True and binvelocityx < -2.4:  # Sets a cap on leftward velocity at 2.4 while succing
        binvelocityx = -2.4

    if binvelocityx >= -0.9 and binvelocityx <= 0.9:  # Velocity decays if already close to 0
        binvelocityx = 0
    if binvelocityx > 0:  # Velocity decays if positive
        binvelocityx -= 0.9
    if binvelocityx < 0:  # Velocity decays if negative
        binvelocityx += 0.9

    binpositionx += binvelocityx  # Move the bin sprite by the current velocity value
    if binpositionx < 10 and binvelocityx < 0:  # Bin sprite does not move past the left edge of the screen
        binpositionx = 10
    if binpositionx > 630 and binvelocityx > 0:  # Bin sprite does not move past the right edge of the screen
        binpositionx = 630

    # Bin swap –––
    if key == "Garbage":  # Swaps bin to garbage
        bintype = "garbage"
    if key == "Compost":  # Swaps bin to compost
        bintype = "compost"
    if key == "Recycling":  # Swaps bin to recycling
        bintype = "recycling"

    # Waste spawn ---
    if paused == 0:
        wasteSpawnTimer += 1
        if wasteSpawnTimer == 120:
            waste_randomizer = random.choice(waste_pool)
            newWaste = Waste(waste_randomizer, random.randint(10, 650), 0, random.randint(3, 3 + level) / 4, 35,
                             35)  # Change this later
            waste_list.append(newWaste)
            wasteSpawnTimer = 0

    # Cloud spawn
    cloudSpawnTimer += 1
    if cloudSpawnTimer == 480:
        cloud_randomizer = random.randint(0, 3)
        newCloud = Cloud(cloud_randomizer, 700, random.randint(0, 300), random.randint(2, 5) / 10)
        cloud_list.append(newCloud)
        cloudSpawnTimer = 0

    # Level up system
    if level == 1 and score >= 1:
        score = 0  # Resets the score for the next threshold
        level += 1  # Increments the level
        paused = 1  # Pauses the game
        score_threshold = 15  # Sets the new score threshold
        waste_pool.extend((7, 8))  # Adds in compost items
        levelup_sound.play()  # Sound effect for levelling up
        for i in range(len(waste_list)):  # Deletes all current trash items
            waste = waste_list[i]
            remove_waste.append(waste)
        for i in remove_waste:
            if i in waste_list:
                waste_list.remove(i)
    if level == 2 and score >= 2:  # Simile
        score = 0
        level += 1
        paused = 1
        score_threshold = 15
        waste_pool.extend((13, 14))  # Adds in recycling items
        levelup_sound.play()  # Sound effect for levelling up
        for i in range(len(waste_list)):
            waste = waste_list[i]
            remove_waste.append(waste)
        for i in remove_waste:
            if i in waste_list:
                waste_list.remove(i)
    if level == 3 and score >= 2:
        score = 0
        level += 1
        paused = 1
        score_threshold = 20
        waste_pool.extend((3, 4, 9, 10, 15, 16))  # Adds in general items
        levelup_sound.play()  # Sound effect for levelling up
        for i in range(len(waste_list)):
            waste = waste_list[i]
            remove_waste.append(waste)
        for i in remove_waste:
            if i in waste_list:
                waste_list.remove(i)
    if level == 4 and score >= 3:
        score = 0
        level += 1
        paused = 1
        score_threshold = 30
        waste_pool.extend((5, 6, 11, 12, 17, 18))  # Adds in general items
        levelup_sound.play()  # Sound effect for levelling up
        for i in range(len(waste_list)):
            waste = waste_list[i]
            remove_waste.append(waste)
        for i in remove_waste:
            if i in waste_list:
                waste_list.remove(i)
        print(waste_pool)
    if level == 5 and score >= 30:
        score = 0
        level += 1
        paused = 1
        levelup_sound.play()  # Sound effect for levelling up
        for i in range(len(waste_list)):
            waste = waste_list[i]
            remove_waste.append(waste)
        for i in remove_waste:
            if i in waste_list:
                waste_list.remove(i)

    # Increment paused timer as long as it is over 0
    if paused > 0:
        paused += 1

    # Unpause game after level increments when key is pressed. Does not work if level is at 6, which means that the infographic is displaying.
    if paused > 30 and event.type == pygame.KEYDOWN and level < 6:
        if event.key == pygame.K_RETURN:
            paused = 0

    # Draws in the background sky and grass
    screen.fill(SKY)
    pygame.draw.rect(screen, GRASS, (0, 490, 960, 50), 0)

    # Draw in and move the clouds
    for i in range(len(cloud_list)):
        cloud = cloud_list[i]
        cloud.x -= cloud.speed
        cloud.draw()
        if cloud.x < -50:
            remove_cloud.append(cloud)
    for i in remove_cloud:
        if i in cloud_list:
            cloud_list.remove(i)

    # Draw bin sprite layers that are behind the waste items
    if bintype == "garbage":
        if binSucc:
            screen.blit(garbagetopopen, (binpositionx, binpositiony - 50))
        else:
            screen.blit(garbagebot, (binpositionx, binpositiony))
            screen.blit(garbagetopclose, (binpositionx, binpositiony - 13))
    if bintype == "compost":
        if binSucc:
            screen.blit(composttopopen, (binpositionx, binpositiony - 50))
        else:
            screen.blit(compostbot, (binpositionx, binpositiony))
            screen.blit(composttopclose, (binpositionx, binpositiony - 13))
    if bintype == "recycling":
        if binSucc:
            screen.blit(recycletopopen, (binpositionx, binpositiony - 50))
        else:
            screen.blit(recyclebot, (binpositionx, binpositiony))
            screen.blit(recycletopclose, (binpositionx, binpositiony - 13))

    # Draw in and apply gravity to the waste items
    for i in range(len(waste_list)):
        waste = waste_list[i]
        waste.y += waste.speed
        waste.draw()

    # Draw bin sprite layers that are in front of the waste items
    if bintype == "garbage":
        if binSucc:
            screen.blit(garbagebot, (binpositionx, binpositiony))
    if bintype == "compost":
        if binSucc:
            screen.blit(compostbot, (binpositionx, binpositiony))
    if bintype == "recycling":
        if binSucc:
            screen.blit(recyclebot, (binpositionx, binpositiony))

    # Draw HUD
    pygame.draw.rect(screen, IVORY, (700, 0, 260, 960))
    tracker = font.render(str(score) + " / " + str(score_threshold), 1, BLACK)
    lvldisplay = font.render("Level: " + str(level), 1, BLACK)
    screen.blit(tracker, (840, 500))
    screen.blit(lvldisplay, (740, 500))

    # Draw pop-up screens between levels
    if level == 1 and paused > 0:
        screen.blit(level1, (0, 0))
    if level == 2 and paused > 0:
        screen.blit(level2, (0, 0))
    if level == 3 and paused > 0:
        screen.blit(level3, (0, 0))
    if level == 4 and paused > 0:
        screen.blit(level4, (0, 0))
    if level == 5 and paused > 0:
        screen.blit(level5, (0, 0))
    if level == 6:
        screen.blit(endscreen, (0, 0))

    # Updates screen
    pygame.display.flip()

    # 60 fps
    clock.tick(60)

# Quit
pygame.quit()
