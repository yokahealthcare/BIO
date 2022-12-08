# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 11:23:38 2022

SNAKE AI GAME
@author: Erwin
"""

import pygame
import random
import numpy as np
import os

pygame.init()
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 14)

# SNAKE CONFIGURATION
BLOCK_SIZE = 10
SPEED = 10

# DISPLAY
w = 300
h = 300
display = pygame.display.set_mode((w, h))
pygame.display.set_caption("SNAKE GAME")

# RGB
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (0, 0, 0)

# HEAD COORDINATE
x = w/2
y = h/2

# TAIL COORDINATE
tail_length = 1
tail = [[x,y]]

# CHANGES
x_c = BLOCK_SIZE
y_c = 0

# APPLE
is_there_apple = False
x_apple = 70
y_apple = 150

# POINT
point = 0

# CLOCK
clock = pygame.time.Clock()

# MESSAGE
def gameOverText():
    value = font_style.render("GAME OVER", True, RED)
    display.blit(value, [w/6, h/3])

def scoreText():
    value = score_font.render("Your Score : " + str(point), True, YELLOW)
    display.blit(value, [0, 0])

def stateText(state):
    # os.system("cls")
    state  = np.array(state, dtype=str)
    text = "Danger: S = " + state[0] + " ;R = " + state[1] + " ;L = "+state[2] + "\n" + "Direction: L = " + state[3] + " ;R = " + state[4] + " ;U = " + state[5] + " ;D = " + state[6] + "\n" + "Food: L = " + state[7] + " ;R = " + state[8] + " ;U = " + state[9] + " ;D = " + state[10] + "\n\n"
    print(text)
    

# DIRECTION
LEFT = False
RIGHT = True
UP = False
DOWN = False

# AI
"""
YOUTUBE
https://www.youtube.com/watch?v=L8ypSXwyBds

-------------------- ACTION
[1, 0, 0]       : straight
[0, 1, 0]       : right turn
[0, 0, 1]       : left turn

-------------------- REWARD
Eat Food        : +10
Game Over       : -10
Else            : 0

-------------------- STATE (11 values)
[
    danger straight, danger right, danger left,
    
    direction left, direction right,
    direction up, direction down,
    
    food left, food right,
    food up, food down
]

"""
# AI - State
def get_state():
    head = [x,y]
 
    dir_l = LEFT
    dir_r = RIGHT
    dir_u = UP
    dir_d = DOWN
    
    # CUSTOME DANGER DETECTION
    danger_s = False
    danger_l = False
    danger_r = False
    

    if dir_u:
        point_l = [head[0] - BLOCK_SIZE, head[1]]
        point_r = [head[0] + BLOCK_SIZE, head[1]]
        point_s = [head[0], head[1] - BLOCK_SIZE]
        
        if point_l[0] < 0 or point_l in tail[:-1]:
            danger_l = True
        if point_r[0] > w-BLOCK_SIZE or point_r in tail[:-1]:
            danger_r = True
        if point_s[1] < 0 or point_s in tail[:-1]:
            danger_s = True
        
    
    if dir_d:
        point_r = [head[0] - BLOCK_SIZE, head[1]]
        point_l = [head[0] + BLOCK_SIZE, head[1]]
        point_s = [head[0], head[1] + BLOCK_SIZE]
        
        if point_r[0] < 0 or point_r in tail[:-1]:
            danger_r = True
        if point_l[0] > w-BLOCK_SIZE or point_l in tail[:-1]:
            danger_l = True
        if point_s[1] > h-BLOCK_SIZE or point_s in tail[:-1]:
            danger_s = True
    
    if dir_r:
        point_r = [head[0], head[1] + BLOCK_SIZE]
        point_l = [head[0], head[1] - BLOCK_SIZE]
        point_s = [head[0] + BLOCK_SIZE, head[1]]
        
        if point_r[1] > h-BLOCK_SIZE or point_r in tail[:-1]:
            danger_r = True
        if point_l[1] < 0 or point_l in tail[:-1]:
            danger_l = True
        if point_s[0] > w-BLOCK_SIZE or point_s in tail[:-1]:
            danger_s = True
    
    if dir_l:
        point_r = [head[0], head[1] - BLOCK_SIZE]
        point_l = [head[0], head[1] + BLOCK_SIZE]
        point_s = [head[0] - BLOCK_SIZE, head[1]]
        
        if point_r[1] < 0 or point_r in tail[:-1]:
            danger_r = True
        if point_l[1] > h-BLOCK_SIZE or point_l in tail[:-1]:
            danger_l = True
        if point_s[0] < 0 or point_s in tail[:-1]:
            danger_s = True
            
    state = [
        # Danger
        danger_s,
        danger_r,
        danger_l,
 
        # Move Direction
        dir_l,
        dir_r,
        dir_u,
        dir_d,
 
        # Food Location
        x_apple < x,  # food is in left
        x_apple > x,  # food is in right
        y_apple < y,  # food is up
        y_apple > y  # food is down
    ]
    return np.array(state, dtype=int)



over = False
while not over:
    
    """
    pygame.draw.rect(display, RED, [0, 0, 10, 10])
    pygame.draw.rect(display, RED, [290, 290, 10, 10])
    os.system("pause")
    """
    
    #1 - LISTEN TO AN EVENT
    # EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and not RIGHT:
                LEFT = True
                RIGHT = False
                UP = False
                DOWN = False
                x_c = -BLOCK_SIZE
                y_c = 0
            if event.key == pygame.K_RIGHT and not LEFT:
                LEFT = False
                RIGHT = True
                UP = False
                DOWN = False
                x_c = +BLOCK_SIZE
                y_c = 0
            if event.key == pygame.K_UP and not DOWN:
                LEFT = False
                RIGHT = False
                UP = True
                DOWN = False
                x_c = 0
                y_c = -BLOCK_SIZE
            if event.key == pygame.K_DOWN and not UP:
                LEFT = False
                RIGHT = False
                UP = False
                DOWN = True
                x_c = 0
                y_c = +BLOCK_SIZE
    
    #2 - UPDATE THE COORDINATE X,Y
    # MOVING
    x += x_c
    y += y_c
    
    #3 - UPDATE ALL VARIABLES
    # EAT
    if x == x_apple and y == y_apple:
        is_there_apple = False
        point += 1
        
        tail_length += 1
        
    # MOVING TAIL
    tail.append([x,y])
    if len(tail) > tail_length:
        del tail[0]
    """s
        -- inital    
        [[150, 150]]
        
        -- move 1 
        [[150, 150], [160, 150]]
        
        -- pop 1 at front
        [[160, 150]]
    
    """
    
    #4 - PLOTTING 
    # WIPE THE SCREEN FIRST BEFORE PLOTTING
    display.fill(WHITE)
    # APPLE
    if is_there_apple == False:
        x_apple = random.randint(0, 29)*BLOCK_SIZE
        y_apple = random.randint(0, 29)*BLOCK_SIZE
        is_there_apple = True
    pygame.draw.rect(display, RED, [x_apple, y_apple, BLOCK_SIZE, BLOCK_SIZE])
    # SNAKE 
    for j in tail:
        pygame.draw.rect(display, YELLOW, [j[0], j[1], BLOCK_SIZE, BLOCK_SIZE], width=1)
    # SCORE
    scoreText()
    # UPDATE SCREEN
    pygame.display.update()
    
    #5 - CHECK CONDITION
    # TAIL COLLISION    
    for i in tail[:-1]:
        if i == [x,y]:
            over = True
    
    # WALL COLLISION
    if x < 0 or x >= w or y < 0 or y >= h:
        over = True
        break
    
    #6 - GET DATA STATE
    # STATE
    state = get_state()
    # STATE STATUS - PLOTTING DEBUGGING
    # stateText(state)
    
    #7 DEEP LEARNING Q
    
    
    
    

    # DEBUG
    # print("X : {}".format(x))
    # print("Y : {}".format(x))
    # print("Point : {}".format(point))
        
    
    clock.tick(SPEED)
    
gameOverText()
pygame.display.update()
# time.sleep(1)

pygame.quit()


