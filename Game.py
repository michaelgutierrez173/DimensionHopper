import pygame
import time
import math
import random
import numpy as np
from UfoAI import NeuralNetwork
from UfoAI import NeuralNetworkTrainer



class Portal(object):

    def __init__(self, currx, curry):
        self.px = random.randint(0, 545)
        self.py = random.randint(0, 345)



class Rock(object):

    def __init__(self, lvl, currx, curry):

        self.lvl = lvl
        if self.lvl <= 2:
            self.movement = 'rand'
        elif self.lvl == 3 or self.lvl == 4:
            self.movement = 'follow'
        else:
            decider = random.randint(0,1)
            if decider == 0:
                self.movement = 'rand'
            else:
                self.movement = 'follow'

        #change speed to lvl
        self.rock_speed = lvl-2
        if lvl == 1 or lvl == 2:
            self.rock_speed = lvl * 2
        self.rock_width = 25
        self.rock_height = 25
        # changing rock speed to 1 for ai
        #self.rock_speed = 1

        direction = random.randint(0,1)
        if direction == 0:
            self.growX = self.rock_speed
        else:
            self.growX = self.rock_speed*-1
        direction = random.randint(0, 1)
        if direction == 0:
            self.growY = self.rock_speed
        else:
            self.growY = self.rock_speed * -1

        corner = random.randint(1, 4)
        if self.movement == 'follow':
            if corner == 1:
                self.rock_startx = 0
                self.rock_starty = 0
            if corner == 2:
                self.rock_startx = 775
                self.rock_starty = 0
            if corner == 3:
                self.rock_startx = 0
                self.rock_starty = 575
            if corner == 4:
                self.rock_startx = 775
                self.rock_starty = 575
        else:
            """
            # spawn rocks in corners for AI
            if corner == 1:
                self.rock_startx = 0
                self.rock_starty = 0
            if corner == 2:
                self.rock_startx = 775
                self.rock_starty = 0
            if corner == 3:
                self.rock_startx = 0
                self.rock_starty = 575
            if corner == 4:
                self.rock_startx = 775
                self.rock_starty = 575
            """
            self.rock_startx = random.randint(0, 775)
            self.rock_starty = random.randint(0, 575)
            while (self.rock_startx < currx+80 and self.rock_starty < curry+80) and (currx < self.rock_startx + 80 and curry < self.rock_starty + 80):
                self.rock_startx = random.randint(0, 775)
                self.rock_starty = random.randint(0, 575)


    def __str__(self):
        return "x: " + str(self.rock_startx) + " y: " + str(self.rock_starty)

    def update(self, xcoord, ycoord):
        if self.movement == 'rand':
            self.rock_startx = self.rock_startx + self.growX
            if self.rock_startx >= 775:
                self.growX = self.rock_speed * -1
            elif self.rock_startx <= 0:
                self.growX = self.rock_speed

            self.rock_starty = self.rock_starty + self.growY
            if self.rock_starty >= 575:
                self.growY = self.rock_speed * -1
            elif self.rock_starty <= 0:
                self.growY = self.rock_speed
        else:
            if self.rock_startx > xcoord:
                self.rock_startx -= self.rock_speed
            else:
                self.rock_startx += self.rock_speed
            if self.rock_starty > ycoord:
                self.rock_starty -= self.rock_speed
            else:
                self.rock_starty += self.rock_speed


#from Obj import Rock
#from Portal import Portal

pygame.init()

display_width = 800
display_height = 600
ufo_width = 51
ufo_height = 53
black = (0, 0, 0)
white = (255, 255, 255)
red = (180, 0, 0)
red_light = (255, 0, 0)
blue = (0, 0, 180)
blue_light = (0, 0, 255)
green = (0, 180, 0)
green_light = (0, 255, 0)
yellow = (180, 180, 0)
yellow_light = (255, 255, 0)
level = 1
pause = False
highscore = 0
highscore_ai = 0
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Dimension Hopper')
clock = pygame.time.Clock()
NNTrainer = NeuralNetworkTrainer(100)


ufoImg = pygame.image.load('ufotran.png')
def ufo(x, y):
    gameDisplay.blit(ufoImg, (x, y))


rockImg = pygame.image.load('roid.png')
def rocks(x, y):
    gameDisplay.blit(rockImg, (x, y))


portalImg = pygame.image.load('newport.png')
def portals(x, y):
    gameDisplay.blit(portalImg, (x, y))


def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()


def message_display(text):
    largeText = pygame.font.SysFont("Arial", 115)
    textSurf, textRect = text_objects(text, largeText)
    textRect.center = (display_width/2, display_height/2)
    gameDisplay.blit(textSurf, textRect)
    pygame.display.update()
    time.sleep(2)
    if text == "YOU WON!!!":
        time.sleep(3)
        game_intro()
    else:
        story_loop()


def message_displayarcade(text):
    largeText = pygame.font.SysFont("Arial", 115)
    textSurf, textRect = text_objects(text, largeText)
    textRect.center = (display_width/2, display_height/2)
    gameDisplay.blit(textSurf, textRect)
    pygame.display.update()
    time.sleep(2)
    arcade_loop()

def message_displayarcade_ai(text):
    largeText = pygame.font.SysFont("Arial", 115)
    textSurf, textRect = text_objects(text, largeText)
    textRect.center = (display_width/2, display_height/2)
    gameDisplay.blit(textSurf, textRect)
    pygame.display.update()
    time.sleep(3)
    arcade_loop_ai()

def score_display(num, lvl):
    global highscore
    font = pygame.font.SysFont("Arial", 25)
    if lvl != 0:
        text = font.render("Score: " + str(num) + " Dimension: " + str(lvl), True, white)
    else:
        text = font.render("Score: " + str(num) + " High Score: " + str(highscore), True, white)
    gameDisplay.blit(text, (0,0))

def score_display_ai(num, lvl):
    global highscore_ai
    font = pygame.font.SysFont("Arial", 25)
    if lvl != 0:
        text = font.render("Score: " + str(num) + " Dimension: " + str(lvl), True, white)
    else:
        text = font.render("Score: " + str(num) + " High Score: " + str(highscore_ai), True, white)
    gameDisplay.blit(text, (0,0))

def collision(ax, ay, ar, bx, by, br):
    return math.sqrt( ((ax-bx)**2) + ((ay-by)**2) ) < br + ar


def crash():
    message_display('You Crashed')


def crasharcade(s):
    global highscore
    if s > highscore:
        highscore = s
    message_displayarcade('You Crashed')

def crasharcade_ai(s):
    global highscore_ai
    if s > highscore_ai:
        highscore_ai = s
    message_displayarcade_ai('You Crashed')

def passed():
    global level
    level += 1
    if level < 6:
        message_display('You Passed')
    else:
        message_display('YOU WON!!!')


def button(msg,x,y,w,h,ic,ac, action):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))
        if click[0] == 1 and action == "story":
            story_loop()
        elif click[0] == 1 and action == "arcade":
            arcade_loop()
        elif click[0] == 1 and action == "arcade_ai":
            arcade_loop_ai()
        elif click[0] == 1 and action == "cont":
            unpause()
        elif click[0] == 1 and action == "back":
            game_intro()
        elif click[0] == 1 and action == "instruct":
            instruct()
        elif click[0] == 1 and action == "quit":
            pygame.quit()
            quit()
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))

    smallText = pygame.font.SysFont("Arial", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    gameDisplay.blit(textSurf, textRect)


def unpause():
    global pause
    pause = False


def paused():
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(black)
        largeText = pygame.font.SysFont("Arial", 80)
        textSurf, textRect = text_objects("Paused", largeText)
        textRect.center = (display_width / 2, display_height / 2.5)
        gameDisplay.blit(textSurf, textRect)

        button("Continue",125,400,150,40,green,green_light, "cont")
        button("Back",525,400,150,40,red, red_light, "back")

        pygame.display.update()
        clock.tick(15)


def instruct():
    global pause
    pause = True
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(black)
        largeText = pygame.font.SysFont("Arial", 20)
        gameDisplay.blit(largeText.render('Goal: Avoid being hit by asteroids.', True, (255,255,255)), (10,60))
        gameDisplay.blit(largeText.render('Control: Use your arrow keys to control your spaceship. Hit p to pause.', True, (255,255,255)), (10,100))
        gameDisplay.blit(largeText.render('Story Mode: Reaching 1000 points on each dimension will open up a portal.', True, (255,255,255)), (10,150))
        gameDisplay.blit(largeText.render('Go through the portal to reach the next dimension.', True, (255, 255, 255)), (10, 170))
        gameDisplay.blit(largeText.render('Complete all 5 dimensions to win.', True, (255,255,255)), (10,190))
        gameDisplay.blit(largeText.render('Arcade: Survive as long as possible.', True, (255,255,255)), (10,240))


        button("Back",0,0,150,40,red, red_light, "back")

        pygame.display.update()
        clock.tick(15)


def game_intro():
    global level
    level = 1
    intro = True;
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(black)
        largeText = pygame.font.SysFont("Arial", 80)
        textSurf, textRect = text_objects("Dimension Hopper", largeText)
        textRect.center = (display_width / 2, display_height / 2.5)
        gameDisplay.blit(textSurf, textRect)

        button("Story Mode",300,300,200,40,green,green_light, "story")
        button("Arcade",300,350,200,40,blue,blue_light, "arcade")
        button("Arcade AI", 300, 400, 200, 40, blue, blue_light, "arcade_ai")
        button("How to Play",300,450,200,40,yellow,yellow_light, "instruct")
        button("Quit",300,500,200,40,red, red_light, "quit")

        pygame.display.update()
        clock.tick(15)




def arcade_loop():
    global pause
    global level
    level = 0
    x = (display_width * 0.45)
    y = (display_height * 0.45)
    x_change = 0
    y_change = 0

    rock_count = 1
    my_rocks = []
    for i in range(rock_count):
        my_rocks.append(Rock(2, x, y))
    score = 0
    gameExit = False
    while not gameExit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -8
                if event.key == pygame.K_RIGHT:
                    x_change = 8
                if event.key == pygame.K_UP:
                    y_change = -8
                if event.key == pygame.K_DOWN:
                    y_change = 8
                if event.key == pygame.K_p:
                    pause = True
                    paused()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_change = 0

        # update and make ufo
        gameDisplay.fill(black)
        if (x + x_change) <= display_width - ufo_width and (x + x_change) > 0:
            x += x_change
        if (y + y_change) <= display_height - ufo_height and (y + y_change) > 0:
            y += y_change
        ufo(x, y)

        # increase score
        score += 1
        score_display(score, level)
        if score % 45 == 0:
            my_rocks.append(Rock(2, x, y))

        # update rocks and check for crash
        for r in my_rocks:
            rocks(r.rock_startx, r.rock_starty)
            r.update(x, y)
            if collision(x + 25, y + 27, 19, r.rock_startx + 16, r.rock_starty + 16, 16):
                crasharcade(score)

        pygame.display.update()
        clock.tick(30)

#returns: x,y where x is the change in x position and y is the change in y position
def move_ai(rocks, ufoX, ufoY, neural_network):
    # Find the closest rock
    closest_rock_x = rocks[0].rock_startx
    closest_rock_y = rocks[0].rock_starty
    closest_distance = int(round(distance(ufoX, ufoY, rocks[0].rock_startx, rocks[0].rock_starty)))
    for rock in rocks:
        if closest_distance > int(round(distance(ufoX, ufoY, rock.rock_startx, rock.rock_starty))):
            closest_rock_x = rock.rock_startx
            closest_rock_y = rock.rock_starty
            closest_distance = int(round(distance(ufoX, ufoY, rock.rock_startx, rock.rock_starty)))

    # Define direction of the closest rock with respect to UFO
    if ufoX-closest_rock_x > 0:
        x_direction = 1
    else:
        x_direction = -1
    if ufoY - closest_rock_y > 0:
        y_direction = 1
    else:
        y_direction = -1

    distToWall = []
    distToWall.append(ufoY)
    distToWall.append(display_height-ufoY)
    distToWall.append(ufoX)
    distToWall.append(display_width-ufoX)
    distToWall.sort()

    # Get neural network output
    outputs = neural_network.think(np.array([distToWall[0], x_direction, y_direction]))
    x_change = 2 * outputs[0][0] - 1
    y_change = 2 * outputs[0][1] - 1

    # Return the direction multiplied by 8 so it moves faster
    return x_change*8, y_change*8

def distance(x1, y1, x2, y2):
    dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return dist

def arcade_loop_ai():
    global pause
    global level
    global NNTrainer
    level = 0

    # create a list of x y coordinates for multiple UFOs and neural nets for each one
    UFOsX = [display_width * 0.45]*100
    UFOsY = [display_height * 0.45]*100
    # Ten neural networks are defined in global vars
    neural_networks = NNTrainer.NNList
    diedNeural_networks = []

    rock_count = 1
    my_rocks = []
    for i in range(rock_count):
        my_rocks.append(Rock(2, 0, 0))
    score = 0
    gameExit = False
    while not gameExit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = True
                    paused()

        gameDisplay.fill(black)

        # update and make ufo
        for i in range(len(UFOsX)):
            x_change, y_change = move_ai(my_rocks, UFOsX[i], UFOsY[i], neural_networks[i])
            if display_width - ufo_width >= (UFOsX[i] + x_change) > 0:
                UFOsX[i] += x_change
            if display_height - ufo_height >= (UFOsY[i] + y_change) > 0:
                UFOsY[i] += y_change
            ufo(UFOsX[i], UFOsY[i])

        # increase score
        score += 1
        score_display_ai(score, level)
        if score % 100 == 0 and score < 2000:
            my_rocks.append(Rock(2, 0, 0))

        # update rocks and check for crash
        for r in my_rocks:
            rocks(r.rock_startx, r.rock_starty)
            r.update(0, 0)
            if len(UFOsX) > 0:
                keepUFOsX = []
                keepUFOsY = []
                keepneural_networks = []
                for i in range(len(UFOsX)):
                    if collision(UFOsX[i] + 25, UFOsY[i] + 27, 19, r.rock_startx + 16, r.rock_starty + 16, 16):
                        # Keep list of dead ufo (ordered by who died first)
                        diedNeural_networks.append((neural_networks[i], score))
                    else:
                        keepUFOsX.append(UFOsX[i])
                        keepUFOsY.append(UFOsY[i])
                        keepneural_networks.append(neural_networks[i])

                UFOsX = keepUFOsX
                UFOsY = keepUFOsY
                neural_networks = keepneural_networks
            else:
                # train network here
                NNTrainer.train(diedNeural_networks)
                crasharcade_ai(score)

        pygame.display.update()
        clock.tick(144)





def story_loop():
    global pause
    global level
    x = (display_width * 0.45)
    y = (display_height * 0.45)
    x_change = 0
    y_change = 0

    rock_count = 1
    my_rocks = []
    for i in range (rock_count):
        my_rocks.append(Rock(level, x, y))
    score = 0
    gameExit = False
    while not gameExit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -8
                if event.key == pygame.K_RIGHT:
                    x_change = 8
                if event.key == pygame.K_UP:
                    y_change = -8
                if event.key == pygame.K_DOWN:
                    y_change = 8
                if event.key == pygame.K_p:
                    pause = True
                    paused()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_change = 0

        #update and make ufo
        gameDisplay.fill(black)
        if (x+x_change) <= display_width - ufo_width and (x+x_change) > 0:
            x += x_change
        if (y + y_change) <= display_height - ufo_height and (y + y_change) > 0:
            y += y_change
        ufo(x, y)


        #increase score and increase difficulty
        score += 1
        score_display(score, level)
        if score%1000 == 0:
            my_portal = Portal(x, y)
        if score > 1000:
            portals(my_portal.px, my_portal.py)
            if collision(x + 25, y + 27, 20, my_portal.px+125, my_portal.py+125, 100):
                passed()
        if score%45 == 0:
            my_rocks.append(Rock(level, x, y))
        if score%250 == 0:
            for r in my_rocks:
                if r.rock_speed < 6:
                    r.rock_speed += 1

        # update rocks and check for crash
        for r in my_rocks:
            rocks(r.rock_startx, r.rock_starty)
            r.update(x, y)
            if collision(x + 25, y + 27, 19, r.rock_startx + 16, r.rock_starty + 16, 16):
                crash()

        pygame.display.update()
        clock.tick(30)


game_intro()
pygame.quit()
quit()