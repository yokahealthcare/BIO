# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 11:23:38 2022

SNAKE AI GAME
@author: Erwin
"""

import pygame
import random

pygame.init()
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 14)

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
x_c = 10
y_c = 0

# APPLE
is_there_apple = False
x_apple = random.randint(0, 29)*10
y_apple = random.randint(0, 29)*10

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

# DIRECTION
LEFT = False
RIGHT = True
UP = False
DOWN = False

over = False
while not over:
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
                x_c = -10
                y_c = 0
            if event.key == pygame.K_RIGHT and not LEFT:
                LEFT = False
                RIGHT = True
                UP = False
                DOWN = False
                x_c = +10
                y_c = 0
            if event.key == pygame.K_UP and not DOWN:
                LEFT = False
                RIGHT = False
                UP = True
                DOWN = False
                x_c = 0
                y_c = -10
            if event.key == pygame.K_DOWN and not UP:
                LEFT = False
                RIGHT = False
                UP = False
                DOWN = True
                x_c = 0
                y_c = +10
    
    # MOVING
    x += x_c
    y += y_c

    
    # MOVING TAIL
    tail.append([x,y])
    if len(tail) > tail_length:
        del tail[0]
        
    # TAIL COLLISION    
    for i in tail[:-1]:
        if i == [x,y]:
            over = True
    
    # WALL COLLISION
    if x < 0 or x >= w or y < 0 or y >= h:
        over = True
    
    # EAT
    if x == x_apple and y == y_apple:
        is_there_apple = False
        point += 1
        
        tail.append([x,y])
        
    
    # WIPE THE SCREEN FIRST BEFORE PLOTTING
    display.fill(WHITE)
    
    # APPLE
    if is_there_apple == False:
        x_apple = random.randint(0, 29)*10
        y_apple = random.randint(0, 29)*10
        is_there_apple = True
    pygame.draw.rect(display, RED, [x_apple, y_apple, 10, 10])
    
    # SNAKE 
    for j in tail:
        pygame.draw.rect(display, YELLOW, [j[0], j[1], 10, 10], width=1)
    
    # SCORE
    scoreText()
    
    # DEBUG
    # print("X : {}".format(x))
    # print("Y : {}".format(x))
    # print("Point : {}".format(point))
        
    pygame.display.update()
    clock.tick(10)
    
gameOverText()
pygame.display.update()
# time.sleep(1)

pygame.quit()


