import pygame
import time
import json
import random
import time
import threading
from pygame.locals import*
from time import sleep
from seeker import Seeker

class Sprite():
	def __init__(self, x, y, w, h):          ##python constructor
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.alive = True
		self.quadrant = []
		self.static = False
	
	def marshal(self):
		ob = {}
		ob.update({"x": self.x, "y": self.y, "w": self.w, "h": self.h})
		return ob
	
	def collides(self, otherSprite):
		if self.x + self.w < otherSprite.x:
			self.status = False
		elif self.x > otherSprite.x + otherSprite.w:
			self.status = False
		elif self.y > otherSprite.y + otherSprite.h:
			self.status = False
		elif self.y + self.h < otherSprite.y:
			self.status = False
		else:
			self.status = True
		return self.status
	
	def to_string(self):
		print("x: " + self.x + "   y: " + self.y)


	def clicked(self, mouseX, mouseY):
		if(mouseX >= self.x and mouseX < self.x + self.w  and mouseY >= self.y and mouseY <= self.y + self.h):
			return True
		else:
			return False

		


	def is_wall(self):
		return False
	def is_fruit(self):
		return False
	def is_ghost(self):
		return False
	def is_pacman(self):
		return False
	def is_pellet(self):
		return False
	def is_node(self):
		return False

	def update(self):
		pass

	def draw_yourself(self,size, location, scroll):
		pass
###########################
class Pacman(Sprite):
	
	def __init__(self, x, y):
		super().__init__(x, y, 35, 35)
		self.direction = "right"
		self.active = False
		self.bottom = self.y + self.h
		self.right = self.x + self.w
		self.image_num = 1
		self.currentImage = 0
		self.prev_x = self.x
		self.prev_y = self.y
		self.previous_node = Node(0,0)
		self.next_node = Node(0,0)
		self.movement_options = {}
		self.node_collision = False
		self.dead = False

		
		self.pacmanImages = []
		for i in range(4):
			row = []
			for j in range(3):
				picNum = self.image_num
				source = ("images/pacman" + str(picNum) + ".png")
				pacimage = pygame.image.load(source)
				row.append(pacimage)
				self.image_num += 1
			self.pacmanImages.append(row)
				
	def to_string(self):
		print("x: " + self.x + "   y: " + self.y)

	def update(self):
		return True
	
	# def can_move_to(self):
	def die(self):
		pass
	
	def move(self, direction_):
		self.prev_x = self.x
		self.prev_y = self.y
		if self.node_collision:							## currently colliding with node, can move to any neighbors of current node
			self.count = 1
			if direction_ == "right":
				if (self.movement_options[direction_] == "none") and self.x + self.w < self.next_node.right :
					self.x += 10
				elif not(self.movement_options[direction_] == "none"):
					self.x +=10
			if direction_ == "left":
				if (self.movement_options[direction_] == "none") and  self.x > self.next_node.x - 10:
					self.x -= 10
				elif not(self.movement_options[direction_] == "none"):
					self.x -= 10
			if direction_ == "up":
				if (self.movement_options[direction_] == "none") and  self.y > self.next_node.y - 10:
					self.y -= 10
				elif not(self.movement_options[direction_] == "none"):
					self.y -= 10
			if direction_ == "down":
				if (self.movement_options[direction_] == "none") and  self.y + self.h < self.next_node.y + 10:
					self.y += 10
				elif not(self.movement_options[direction_] == "none"):
					self.y += 10
		elif not(self.node_collision):                        #### not colliding, can only move between node it was just at and whatever node it is moving in the direction of
			if direction_ in self.movement_options:
				self.next_node = self.movement_options[direction_]

			if self.count == 1 :
				self.movement_options = {direction_: self.next_node, self.opposite_direction(direction_): self.previous_node }
				self.count += 1
			if  self.next_node != ("none"):
				if self.previous_node.x == self.next_node.x or self.previous_node == self.next_node:
					if direction_ == "down" and direction_ in self.movement_options:
						self.y += 10
					if direction_ == "up" and direction_ in self.movement_options:
						self.y -= 10
				if self.previous_node.y == self.next_node.y or self.previous_node == self.next_node:
					if direction_ == "right" and direction_ in self.movement_options:
						self.x += 10
					if direction_ =="left" and direction_ in self.movement_options:
						self.x -= 10 


	def opposite_direction(self, dir):
		if dir == "right":
			return "left"
		elif dir == "left":
			return "right"
		elif dir == "up":
			return "down"
		elif dir == "down":
			return "up"
	


	def draw_yourself(self, canv, size, location, scroll):
		if self.x >= 900:
			self.x = 1
		if self.x < 0:
			self.x = 900
		if self.direction == "left" and self.active:
			canv.blit(pygame.transform.scale(self.pacmanImages[0][self.currentImage], size ), [location[0],location[1]])
			self.currentImage += 1
		elif self.direction == "left" and not(self.active):
			canv.blit(pygame.transform.scale(self.pacmanImages[0][0], size ), [location[0],location[1]])
		if self.direction == "up" and self.active:
			canv.blit(pygame.transform.scale(self.pacmanImages[1][self.currentImage], size ), [location[0],location[1]])
			self.currentImage += 1
		elif self.direction == "up" and not(self.active):
			canv.blit(pygame.transform.scale(self.pacmanImages[1][0], size ), [location[0],location[1]])
		if self.direction == "right" and self.active:
			canv.blit(pygame.transform.scale(self.pacmanImages[2][self.currentImage], size ), [location[0],location[1]])
			self.currentImage += 1
		elif self.direction == "right" and not(self.active):
			canv.blit(pygame.transform.scale(self.pacmanImages[2][0], size ), [location[0],location[1]])
		if self.direction =="down" and self.active:
			canv.blit(pygame.transform.scale(self.pacmanImages[3][self.currentImage], size ), [location[0],location[1]])
			self.currentImage += 1
		elif self.direction == "down" and not(self.active):
			canv.blit(pygame.transform.scale(self.pacmanImages[3][0], size ), [location[0],location[1]])
		if self.currentImage == 2:
			self.currentImage = 0

	def set_direction(self, dir):
		self.direction = dir        

	def set_active(self, status):
		self.active = status

	def is_pacman(self):
		return True
######################
class Fruit(Sprite):
	def __init__(self, x, y, w, h):
		super().__init__(x, y, w, h)
		# self.alive = True
		self.right = True
		self.start_dir = random.choice(["vertical", "horizontal"])

	def to_string(self):
		print("x: " + self.x + "   y: " + self.y)
	
	def draw_yourself(self, canv, size, location, scroll):
		if self.x >= 900:
			self.x = 1
		if self.x < 0:
			self.x = 900
		image = pygame.image.load("images/fruit1.png")
		canv.blit(pygame.transform.scale(image, size ), [location[0],location[1]])

	def get_eaten(self):
		self.alive = False

	def update(self, change):
		if change:
			self.right = not(self.right)
		if self.start_dir == "horizontal":
			if self.right:
				self.x += 3
			else:
				self.x -= 3
		if self.start_dir == "vertical":
			if self.right:
				self.y += 3
			else: 
				self.y -=3
		return self.alive
	
	def is_fruit(self):
		return True
##################
class Wall(Sprite):
	def __init__(self, x, y, w, h):
		super().__init__(x, y, w, h)
		self.static = True
  
	def __str__(self):
		return f"Wall at ({self.x}, {self.y})"

	def __repr__(self):
		return f"Wall(x={self.x}, y={self.y})"
	
	def draw_yourself(self, canv, size, location, scroll):
		# image = pygame.image.load("images/wall.png")
		# # canv.blit(pygame.transform.scale(image, size ), [location[0],location[1]])
		# return True
		pass

	def get_eaten(self):
		self.alive = False

	def update(self):
		return self.alive

	def is_wall(self):
		return True
##########################
class Ghost(Sprite):
	def __init__(self, x, y, w, h):
		super().__init__(x, y, w, h)
		# self.alive = True
		self.direction = ""
		self.image_num = 1
		self.ghosts = []
		self.eaten = False
		self.countdown = 80
		self.previous_node = Node(0,0)
		self.next_node = Node(0,0)
		self.pacman_node = Node(0,0)
		self.pacman_next_node = Node(0,0)
		self.movement_options = {}
		self.node_collision = False
		self.direction_picked = False
		self.eatable = False

		self.image = pygame.image.load("images/blinky1.png")
		for i in range(3):
			picNum = self.image_num
			source = ("images/ghost" + str(picNum) + ".png")
			pacimage = pygame.image.load(source)
			self.ghosts.append(pacimage)
			self.image_num += 2

	def update(self):
		if self.eatable:
			self.image = pygame.image.load("images/ghost1.png")
		else:
			self.image = pygame.image.load("images/blinky1.png")
		self.move()
		if self.eaten:
			self.countdown -= 1
		if self.countdown <= 0:
			return False
		
	

	def next_step(self):   ##returns a list of directions to go, from most effictent to least
		step_options = []
		horizontal_distance = abs(self.x - self.pacman_node.x)
		vertical_distance = abs(self.y - self.pacman_node.y)
		
		if horizontal_distance >= vertical_distance:  ##pacman is further right or left than he is up or down from ghost
			if self.x < self.pacman_node.x:  ##left of pacman
				if not self.eatable:
					step_options.append("right")
				else: 
					step_options.append("left")
			else:                           ##right of pacman
				if not self.eatable:
					step_options.append("left")
				else: 
					step_options.append("right")
			if self.y > self.pacman_node.y: ##below pacman
				if not self.eatable:
					step_options.append("up")
				else: 
					step_options.append("down")
			else:                          ##above pacman
				if not self.eatable:
					step_options.append("down")
				else:
					step_options.append("up")
		else: 										  ##pacman is further up or down than he is left or right from ghost
			if self.y > self.pacman_node.y:   ##below pacman
				if not self.eatable:
					step_options.append("up")
				else:
					step_options.append("down")
			else:                                  ##above pacman
				if not self.eatable:
					step_options.append("down")
				else: 
					step_options.append("up")
			if self.x < self.pacman_node.x:        ##left of pacman
				if not self.eatable:
					step_options.append("right")
				else:
					step_options.append("left")
			else:                               ##right of pacman
				if not self.eatable:
					step_options.append("left")
				else:
					step_options.append("right")
		if not(self.movement_options[step_options[0]] == "none"):
			return step_options[0]
		elif not(self.movement_options[step_options[1]] == "none"):
			return step_options[1]
		elif not(self.movement_options[self.opposite_direction(step_options[0])] == "none"):
			return self.opposite_direction(step_options[0])
		elif not(self.movement_options[self.opposite_direction(step_options[1])] == "none"):
			return self.opposite_direction(step_options[1])

	def to_pacman(self):
		print (f"prev  {self.previous_node}   pac: {self.pacman_next_node}")
		if self.previous_node.y == self.pacman_next_node.y:
			if self.previous_node.x > self.pacman_next_node.x:
				return "left"
			if self.previous_node.x < self.pacman_next_node.x:
				return "right"
		if self.previous_node.x == self.pacman_next_node.x:
			if self.previous_node.y > self.pacman_next_node.y:
				return "up"
			if self.previous_node.y < self.pacman_next_node.y:
				return "down"

	def move(self):
		move_size = 4
		if self.node_collision:							## currently colliding with node, can move to any neighbors of current node		
			self.direction = self.next_step()
			if self.previous_node == self.pacman_node and not(self.eatable):  ##colliding with the node pacman touched last
				self.direction = self.to_pacman()
				print(f"Direction {self.direction} ")
			self.count = 1
			if self.direction == "right":
				if (self.movement_options[self.direction] == "none") and self.x + self.w < self.next_node.right :  ##still in node
					self.x += move_size
				elif not(self.movement_options[self.direction] == "none"):
					self.x +=move_size
			if self.direction == 'left':
				if (self.movement_options[self.direction] == "none") and  self.x > self.next_node.x - 10:  ##still in node
					self.x -= move_size
				elif not(self.movement_options[self.direction] == "none"):
					self.x -= move_size
			if self.direction == "up":
				if (self.movement_options[self.direction] == "none") and  self.y > self.next_node.y - 10:  ##still in node
					self.y -= move_size
				elif not(self.movement_options[self.direction] == "none"):
					self.y -= move_size
			if self.direction == "down":
				if (self.movement_options[self.direction] == "none") and  self.y + self.h < self.next_node.y + 10:  ##still in node
					self.y += move_size
				elif not(self.movement_options[self.direction] == "none"):
					self.y += move_size

		elif not(self.node_collision):                        #### not colliding, can only move between node it was just at and whatever node it is moving in the direction of
			self.count = 1
			if self.direction in self.movement_options:
				self.next_node = self.movement_options[self.direction]

			if self.count == 1 :
				self.movement_options = {self.direction: self.next_node, self.opposite_direction(self.direction): self.previous_node }
				self.count += 1
			if  self.next_node != ("none"):
				if self.previous_node.x == self.next_node.x or self.previous_node == self.next_node:
					if self.direction == "down" and self.direction in self.movement_options:
						self.y += move_size
					if self.direction == "up" and self.direction in self.movement_options:
						self.y -= move_size
				if self.previous_node.y == self.next_node.y or self.previous_node == self.next_node:
					if self.direction == "right" and self.direction in self.movement_options:
						self.x += move_size
					if self.direction =="left" and self.direction in self.movement_options:
						self.x -= move_size
		
	def opposite_direction(self, dir):
		if dir == "right":
			return "left"
		elif dir == "left":
			return "right"
		elif dir == "up":
			return "down"
		elif dir == "down":
			return "up"

	def __str__(self):
		return f"Ghost at ({self.x}, {self.y})"
	
	def __repr__(self):
		return f"Ghost(x={self.x}, y={self.y})"
	
	def draw_yourself(self, canv, size, location, scroll):
		if self.x >= 855:
			self.x = 1
		if self.x < 0:
			self.x = 855
		if self.eaten:
			if self.countdown > 60:
				canv.blit(pygame.transform.scale(self.ghosts[0], size ), [location[0],location[1]])
			elif self.countdown > 40:
				canv.blit(pygame.transform.scale(self.ghosts[1], size ), [location[0],location[1]])
			elif self.countdown > 20:
				canv.blit(pygame.transform.scale(self.ghosts[2], size ), [location[0],location[1]])
		else:
			canv.blit(pygame.transform.scale(self.image, size ), [location[0],location[1]])

		# image = pygame.image.load("images/ghost1.png")

	def get_eaten(self):
		self.eaten = True
		self.alive = False
		
	def is_ghost(self):
		return True
#####################
class Node(Sprite):
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.w = 10
		self.h = 10
		self.right = self.x + self.w
		self.bottom = self.y + self.h
		self.neighbors = {
			"right": None,
			"left":  None,
			"up": None,
			"down": None
		}  ##[right, left, up, down]
		
	def draw_yourself(self, canv, size, location, scroll):
		pass
		# image = pygame.image.load("images/node.png")
		# canv.blit(pygame.transform.scale(image, size ), [location[0]-10,location[1]-10])

	def marshal(self):
		ob = {}
		ob.update({"x": self.x, "y": self.y})
		return ob

	def add_neighbor(self, neighbor, direction):
		if not (neighbor in self.neighbors):
			self.neighbors[direction] = neighbor

	def __str__(self):
		return f"Node at ({self.x}, {self.y})"

	def __repr__(self):
		return f"Node(x={self.x}, y={self.y}, neighbors={len(self.neighbors)})"
	
	def is_node(self):
		return True
	def is_wall(self):
		return False
##############################
class Pellet(Sprite):

	def __init__(self, x, y, w, h):
		super().__init__(x, y, w, h)
		self.static = True

	def to_string(self):
		print("x: " + self.x + "   y: " + self.y)
	
	
	def draw_yourself(self, canv, size, location, scroll):
		image = pygame.image.load("images/pellet.png")
		canv.blit(pygame.transform.scale(image, size ), [location[0],location[1]])

	def get_eaten(self):
		self.alive = False

	def update(self):
		return self.alive
	
	def is_pellet(self):
		return True
#############################
