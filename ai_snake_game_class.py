import pygame
import random
import numpy as np
import os

class Snake:
	def __init__(self, width, height):
		pygame.init()
		self.font_style = pygame.font.SysFont("bahnschrift", 25)
		self.score_font = pygame.font.SysFont("comicsansms", 14)
        
		# DISPLAY
		self.w = width
		self.h = height
		self.display = pygame.display.set_mode((self.w, self.h))
		pygame.display.set_caption("SNAKE GAME")

		# SNAKE CONFIGURATION
		self.BLOCK_SIZE = 10
		self.SPEED = 10
        
        # COLOR
        # RGB
		self.RED = (255, 0, 0)
		self.GREEN = (0, 255, 0)
		self.BLUE = (0, 0, 255)
		self.YELLOW = (255, 255, 0)
		self.WHITE = (0, 0, 0)

		# COORDINATE
		# HEAD
		self.x = self.w/2
		self.y = self.h/2

		# TAIL
		self.tail_length = 1
		self.tail = [[self.x, self.y]]

		# CHANGES
		self.x_c = self.BLOCK_SIZE
		self.y_c = 0

		# APPLE
		self.is_there_apple = False
		self.x_apple = random.randint(0, self.w/10-1)*self.BLOCK_SIZE
		self.y_apple = random.randint(0, self.y/10-1)*self.BLOCK_SIZE

		# POINT (XP) OF GAME
		self.point = 0

		# CLOCK
		self.clock = pygame.time.Clock()

		# DIRECTION
		self.LEFT = False
		self.RIGHT = True
		self.UP = False
		self.DOWN = False
        
    
	def playStep(self):
		self.over = False
		# 1 - LISTEN TO AN EVENT
	    # EVENTS
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.over = True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT and not self.RIGHT:
					self.LEFT = True
					self.RIGHT = False
					self.UP = False
					self.DOWN = False
					self.x_c = -self.BLOCK_SIZE
					self.y_c = 0
				if event.key == pygame.K_RIGHT and not self.LEFT:
					self.LEFT = False
					self.RIGHT = True
					self.UP = False
					self.DOWN = False
					self.x_c = +self.BLOCK_SIZE
					self.y_c = 0
				if event.key == pygame.K_UP and not self.DOWN:
					self.LEFT = False
					self.RIGHT = False
					self.UP = True
					self.DOWN = False
					self.x_c = 0
					self.y_c = -self.BLOCK_SIZE
				if event.key == pygame.K_DOWN and not self.UP:
					self.LEFT = False
					self.RIGHT = False
					self.UP = False
					self.DOWN = True
					self.x_c = 0
					self.y_c = +self.BLOCK_SIZE

	    # 2 - UPDATE THE COORDINATE X,Y
	    # MOVING
		self.x += self.x_c
		self.y += self.y_c
	    
		# 3 - UPDATE ALL VARIABLES
		# EAT
		if self.x == self.x_apple and self.y == self.y_apple:
			self.is_there_apple = False
			self.point += 1

			self.tail_length += 1

	    # MOVING TAIL
		self.tail.append([self.x, self.y])
		if len(self.tail) > self.tail_length:
			del self.tail[0]
		"""
	        -- inital    
	        [[150, 150]]
	        
	        -- move 1 
	        [[150, 150], [160, 150]]
	        
	        -- pop 1 at front
	        [[160, 150]]
	    
		"""
	    
	    # 4 - PLOTTING 
	    # WIPE THE SCREEN FIRST BEFORE PLOTTING
		self.display.fill(self.WHITE)
		# APPLE
		if self.is_there_apple == False:
			self.x_apple = random.randint(0, self.w/10-1)*self.BLOCK_SIZE
			self.y_apple = random.randint(0, self.h/10-1)*self.BLOCK_SIZE
			self.is_there_apple = True
		pygame.draw.rect(self.display, self.RED, [self.x_apple, self.y_apple, self.BLOCK_SIZE, self.BLOCK_SIZE])
	    # SNAKE 
		for j in self.tail:
			pygame.draw.rect(self.display, self.YELLOW, [j[0], j[1], self.BLOCK_SIZE, self.BLOCK_SIZE], width=1)
	    # SCORE
		self.scoreText()
	    # UPDATE SCREEN
		pygame.display.update()
	    
	    # 5 - CHECK CONDITION
	    # TAIL COLLISION    
		for i in self.tail[:-1]:
			if i == [self.x, self.y]:
				self.over = True
	    
	    # WALL COLLISION
		if self.x < 0 or self.x >= self.w or self.y < 0 or self.y >= self.h:
			self.over = True
	    
	    # 6 - GET DATA STATE
	    # STATE
		self.state = self.get_state()
	    # STATE STATUS - PLOTTING DEBUGGING
	    # stateText(state)
	    
	    # 7 DEEP LEARNING Q
	    


	    # DEBUG
	    # print("X : {}".format(x))
	    # print("Y : {}".format(x))
	    # print("Point : {}".format(point))
	        
	    
		self.clock.tick(self.SPEED)
		return self.over, self.point

	def get_state(self):
	    self.head = [self.x, self.y]
	 
	    self.dir_l = self.LEFT
	    self.dir_r = self.RIGHT
	    self.dir_u = self.UP
	    self.dir_d = self.DOWN
	    
	    # CUSTOME DANGER DETECTION
	    self.danger_s = False
	    self.danger_l = False
	    self.danger_r = False
	    

	    if self.dir_u:
	        self.point_l = [self.head[0] - self.BLOCK_SIZE, self.head[1]]
	        self.point_r = [self.head[0] + self.BLOCK_SIZE, self.head[1]]
	        self.point_s = [self.head[0], self.head[1] - self.BLOCK_SIZE]
	        
	        if self.point_l[0] < 0 or self.point_l in self.tail[:-1]:
	            self.danger_l = True
	        if self.point_r[0] > self.w-self.BLOCK_SIZE or self.point_r in self.tail[:-1]:
	            self.danger_r = True
	        if self.point_s[1] < 0 or self.point_s in self.tail[:-1]:
	            self.danger_s = True
	        
	    
	    if self.dir_d:
	        self.point_r = [self.head[0] - self.BLOCK_SIZE, self.head[1]]
	        self.point_l = [self.head[0] + self.BLOCK_SIZE, self.head[1]]
	        self.point_s = [self.head[0], self.head[1] + self.BLOCK_SIZE]
	        
	        if self.point_r[0] < 0 or self.point_r in self.tail[:-1]:
	            self.danger_r = True
	        if self.point_l[0] > self.w-self.BLOCK_SIZE or self.point_l in self.tail[:-1]:
	            self.danger_l = True
	        if self.point_s[1] > self.h-self.BLOCK_SIZE or self.point_s in self.tail[:-1]:
	            self.danger_s = True
	    
	    if self.dir_r:
	        self.point_r = [self.head[0], self.head[1] + self.BLOCK_SIZE]
	        self.point_l = [self.head[0], self.head[1] - self.BLOCK_SIZE]
	        self.point_s = [self.head[0] + self.BLOCK_SIZE, self.head[1]]
	        
	        if self.point_r[1] > self.h-self.BLOCK_SIZE or self.point_r in self.tail[:-1]:
	            self.danger_r = True
	        if self.point_l[1] < 0 or self.point_l in self.tail[:-1]:
	            self.danger_l = True
	        if self.point_s[0] > self.w-self.BLOCK_SIZE or self.point_s in self.tail[:-1]:
	            self.danger_s = True
	    
	    if self.dir_l:
	        self.point_r = [self.head[0], self.head[1] - self.BLOCK_SIZE]
	        self.point_l = [self.head[0], self.head[1] + self.BLOCK_SIZE]
	        self.point_s = [self.head[0] - self.BLOCK_SIZE, self.head[1]]
	        
	        if self.point_r[1] < 0 or self.point_r in self.tail[:-1]:
	            self.danger_r = True
	        if self.point_l[1] > self.h-self.BLOCK_SIZE or self.point_l in self.tail[:-1]:
	            self.danger_l = True
	        if self.point_s[0] < 0 or self.point_s in self.tail[:-1]:
	            self.danger_s = True
	            
	    self.state = [
	        # Danger
	        self.danger_s,
	        self.danger_r,
	        self.danger_l,
	 
	        # Move Direction
	        self.dir_l,
	        self.dir_r,
	        self.dir_u,
	        self.dir_d,
	 
	        # Food Location
	        self.x_apple < self.x,  # food is in left
	        self.x_apple > self.x,  # food is in right
	        self.y_apple < self.y,  # food is up
	        self.y_apple > self.y  # food is down
	    ]
	    return np.array(self.state, dtype=int)


	# MESSAGE FUNCTIONS
	def gameOverText(self):
	    self.value = self.font_style.render("GAME OVER", True, self.RED)
	    self.display.blit(self.value, [self.w/6, self.h/3])

	def scoreText(self):
	    self.value = self.score_font.render("Your Score : " + str(self.point), True, self.YELLOW)
	    self.display.blit(self.value, [0, 0])

	def stateText(self, state):
	    # os.system("cls")
	    self.state  = np.array(self.state, dtype=str)
	    self.text = "Danger: S = " + self.state[0] + " ;R = " + self.state[1] + " ;L = "+self.state[2] + "\n" + "Direction: L = " + self.state[3] + " ;R = " + self.state[4] + " ;U = " + self.state[5] + " ;D = " + self.state[6] + "\n" + "Food: L = " + self.state[7] + " ;R = " + state[8] + " ;U = " + self.state[9] + " ;D = " + self.state[10] + "\n\n"
	    print(self.text)


if __name__ == '__main__':
	game = Snake(width=300, height=300)

	while True:
		game_over, score = game.playStep()

		if game_over == True:
			break

	print("Final Score : {}".format(score))
	pygame.quit()