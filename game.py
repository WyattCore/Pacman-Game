# Name: Starter Code
# Description: Porting A5 to Python
# Date: Spring 2024
##This a pacman inspired game implement into Python.##
##You can move pacman around a window that has walls, fruits, pellets, and ghosts.##
##Pacman can interact with each one of these sprites, she will collide with walls##
##and not go through them, eat fruits, collide with ghosts and cause them to enter##
##a death animation sequence. You can press e to enter an edit mode, where you can##
##add fruits ('f'), ghosts ('g'), pellets ('p')##
##I made the ghost death sequence, blue-> white-> eyes-> remove##
import pygame
import time
import json
import random
import time
import threading

from sprites import *
from graph import *
from seeker import Seeker
from pygame.locals import*
from time import sleep


class Model():
	def __init__(self):
		self.last_spawn_time = time.time()
		self.spawn_interval = 5
		self.sprites = []				   ##list of all sprites
		self.nodes = []						##list of all nodes
		self.walls_and_nodes = []            ##list of the walls and nodes for graph
		self.ghosts = []
		self.pacman = Pacman(430,640)   
		self.sprites.append(self.pacman)
		self.load()								##unmarshals all of the sprites and nodes
		self.maze_graph = Graph()				##the graph
		for sprite in self.sprites:				##puts walls into walls and nodes
			if sprite.is_wall():				
				self.walls_and_nodes.append(sprite)
		for node in self.nodes:	
			self.maze_graph.add_node(node)				##puts in graph
			self.walls_and_nodes.append(node)			##puts nodes in walls and nodes
			self.sprites.append(node)
		#############################
		self.maze_graph.connect_neighbors(self.walls_and_nodes)						##connects the neighbors 
		# for node in self.maze_graph.nodes:
			
	def update(self):
		current_time = time.time()
		if current_time - self.last_spawn_time >= self.spawn_interval:
			self.pellet_spawner()
			self.ghost_spawner()
			self.last_spawn_time = current_time
		for sprite in self.sprites:
			if sprite.is_pacman():
				print(f"Ghosts: {self.ghosts}")
				print(f"Pac next:  {sprite.next_node}")
				for ghost in self.ghosts:
					ghost.pacman_next_node = sprite.next_node
				collided_with_node = False
			if sprite.is_ghost():
				collided_with_node = False
			if sprite.is_fruit():
				sprite.update(False)
				if not(sprite.update(False)):
					self.sprites.remove(sprite)
			elif sprite.update() == False:
				self.sprites.remove(sprite)
			elif sprite.is_fruit() and sprite.alive == False:
				self.sprites.remove(sprite)
			else:
				sprite.update()
			for sprite2 in self.sprites:
				if(sprite2 != sprite):
					if sprite.collides(sprite2):
						if sprite.is_ghost() and sprite2.is_node():
							sprite.movement_options = sprite2.neighbors
							sprite.node_collision = True
							sprite.previous_node = sprite2
							collided_with_node = True
							sprite.pacman_node = self.pacman.previous_node
						if sprite.is_pacman() and sprite2.is_node():
							sprite.movement_options = sprite2.neighbors
							sprite.node_collision = True
							sprite.previous_node = sprite2
							
							collided_with_node = True
						if sprite.is_pacman() and sprite2.is_wall():
							self.fix_collision(sprite, sprite2)
						if sprite.is_pacman() and sprite2.is_fruit():
							sprite2.get_eaten()
						if sprite.is_pacman() and sprite2.is_ghost():
							if sprite2.eatable:
								sprite2.get_eaten()
							elif not(sprite2.eatable):
								sprite.dead = True
								print("Game over")
						if sprite.is_pacman() and sprite2.is_pellet():
							self.ghost_eatable()
							sprite2.get_eaten()
						if sprite.is_fruit() and sprite2.is_wall():
							sprite.update(True)
			sprite.node_collision = collided_with_node

	def fix_collision(self, sprite1, sprite2):
		if sprite1.x + sprite1.w >= sprite2.x and sprite1.prev_x + sprite1.w <= sprite2.x:
			sprite1.x = sprite2.x -sprite1.w

		if sprite1.x <= sprite2.x + sprite2.w and sprite1.prev_x >= sprite2.x + sprite2.w:
			sprite1.x = sprite2.x + sprite2.w

		if sprite1.y + sprite1.h >= sprite2.y and sprite1.prev_y + sprite1.h <= sprite2.y:
			sprite1.y = sprite2.y - sprite1.h	

		if sprite1.y <= sprite2.y + sprite2.h and sprite1.prev_y >= sprite2.y + sprite2.h:
			sprite1.y = sprite2.y + sprite2.h


	def add(self, add, location, scroll, wallSize):
		if(add == 'f'):
			self.sprites.append(Fruit(location[0], location[1], 30, 30))
		elif(add == 'g'):
			new_ghost = Ghost(location[0], location[1], 35, 35)
			self.sprites.append(new_ghost)
			self.ghosts.append(new_ghost)
		elif(add == 'p'):
			self.sprites.append(Pellet(location[0], location[1], 30, 30))
		elif(add == 'w'):
			self.sprites.append(Wall(location[0]-wallSize[0], location[1]-wallSize[1], wallSize[0],wallSize[1]))
		elif(add == 'n'):
			self.nodes.append(Node(location[0], location[1]))
	
	def ghost_spawner(self):
		new_ghost = Ghost(498,346,25,25)
		if self.check_eatable() == True:
			new_ghost.eatable = True
		else:
			new_ghost.eatable = False
		self.ghosts.append(new_ghost)
		self.sprites.append(new_ghost)
		
	def check_eatable(self):
		for ghost in self.ghosts:
			if ghost.eatable == True:
				return True
			else:
				return False
			
	def pellet_spawner(self):
		spawn_node = random.choice(self.nodes)
		new_pellet = Pellet(spawn_node.x, spawn_node.y, 30,30)
		self.sprites.append(new_pellet)

	def clear_map(self):
		for sprite in self.sprites:
			if not(sprite.is_pacman()):
				sprite.get_eaten()

	def movePacman(self, direction):
		self.pacman.move(direction)

	def marshal(self):
		ob = {}
		tmpList_nodes = []
		tmpList_walls = []
		tmpList_fruit = []
		tmpList_pellets = []
		tmpList_Ghosts = []
		ob["nodes"] = tmpList_nodes
		ob["walls"] = tmpList_walls
		ob["pellets"] = tmpList_pellets
		ob["fruits"] = tmpList_fruit
		ob["ghosts"] = tmpList_Ghosts
		for sprite in self.sprites:
			if sprite.is_wall():
				tmpList_walls.append(sprite.marshal())
			if sprite.is_pellet():
				tmpList_pellets.append(sprite.marshal())
			if sprite.is_fruit():
				tmpList_fruit.append(sprite.marshal())
			if sprite.is_ghost():
				tmpList_Ghosts.append(sprite.marshal())
		for node in self.nodes:
			tmpList_nodes.append(node.marshal())

		with open('map.json', 'w') as outfile:
			json.dump(ob, outfile, indent=4);
		return ob
        


	def load(self):
		#open the json map and pull out the individual lists of sprite objects
		self.sprites = []
		with open("map.json") as file:
			data = json.load(file)
			#get the list labeled as "walls" from the map.json file
			nodes = data["nodes"]
			walls = data["walls"]
			fruits = data["fruits"]
			pellets = data["pellets"]
			ghosts_ = data["ghosts"]
		file.close()

		
		#for each entry inside the walls list, pull the key:value pair out and create 
		#a new wall object with (x,y,w,h)
		self.sprites.append(self.pacman)
		for entry in walls:
			self.sprites.append(Wall(entry["x"], entry["y"], entry["w"], entry["h"]))
		for entry in fruits:
			self.sprites.append(Fruit(entry["x"], entry["y"], entry["w"], entry["h"]))
		for entry in ghosts_:
			new_ghost = Ghost(entry["x"], entry["y"], entry["w"], entry["h"])
			self.ghosts.append(new_ghost)
			self.sprites.append(new_ghost)
		for entry in pellets:
			self.sprites.append(Pellet(entry["x"], entry["y"], entry["w"], entry["h"]))
		for entry in nodes:
			self.nodes.append(Node(entry["x"], entry["y"]))

	def delete_sprite(self, mouse_x, mouse_y):
		for sprite in self.sprites:
			if sprite.clicked(mouse_x, mouse_y):
				sprite.get_eaten()


	def ghost_eatable(self):
		for ghost in self.ghosts:
			ghost.eatable = True
		
		timer = threading.Timer(10, self.set_not_eatable, args=(self.ghosts,))
		timer.start()
		
	def set_not_eatable(self, ghosts):
		for ghost in ghosts:
			ghost.eatable = False

######################################################################################

class Start_Screen_View():
	def __init__(self):
		screen_size = (900,900)
		self.screen = pygame.display.set_mode(screen_size, 32)
		self.font = pygame.font.Font(None, 60)
		self.title_text = self.font.render("Pac-man Survival", True, (255,255,255))
		self.start_button_text = pygame.font.Font(None, 40).render("Start Game", True, (255,255,255))
		self.start_button_rect = self.start_button_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))

	def update(self):
		self.screen.fill((0,0,0))
		self.screen.blit(self.title_text, (self.screen.get_width() // 2 - self.title_text.get_width() // 2,100))
		pygame.draw.rect(self.screen, (50, 150, 255), self.start_button_rect.inflate(20,20))
		self.screen.blit(self.start_button_text, self.start_button_rect)
		pygame.display.flip()

class View():
	def __init__(self, model):
		screen_size = (900,900)
		self.screen = pygame.display.set_mode(screen_size, 32)

		self.background_image = pygame.image.load("images/background.png").convert()
		self.background_image = pygame.transform.scale(self.background_image, (900,800))


		self.model = model
		self.scroll_pos = 0

	def update(self):
		self.screen.blit(self.background_image, (0, 50))###############################
		self.model.maze_graph.draw_graph(self.screen)
		# self.screen.fill([0,0,0])
		for sprite in self.model.sprites:
			LOCATION = (sprite.x, sprite.y)
			SIZE = (sprite.w, sprite.h)      ##still make sprites draw themselves in their classess
			sprite.draw_yourself(self.screen, SIZE, LOCATION, self.scroll_pos)
		for node in self.model.nodes:
			LOCATION = (node.x, node.y)
			node.draw_yourself(self.screen, (20,20), LOCATION, self.scroll_pos)
			# self.screen.blit(pygame.transform.scale(sprite.image, SIZE), LOCATION)
		pygame.display.flip()

class End_Screen_View():
	def __init__(self):
		screen_size = (900,900)
		self.screen = pygame.display.set_mode(screen_size, 32)
		self.font = pygame.font.Font(None, 60)
		self.title_text = self.font.render("GAME OVER", True, (255,255,255))

	def end(self):
		start_time = time.time()
		while time.time() - start_time < 5:
			self.screen.fill((0,0,0))
			self.screen.blit(self.title_text, (self.screen.get_width() // 2 - self.title_text.get_width() // 2,100))
			pygame.display.flip()
		pygame.quit()

#######################################################################################
class Controller():
	def __init__(self, model, view, start_screen_view, end_screen_view):
		self.model = model
		self.view = view
		self.start_view = start_screen_view
		self.end_view = end_screen_view
		self.showing_start_screen = True
		self.showing_end_screen = False
		self.keep_going = True
		self.edit = False
		self.add = ''
		self.wall = None
		self.delete = False

	def calculateSize(self, wallStart_, wallEnd_):
		if wallStart_ [0] < wallEnd_ [0] and wallStart_[1] < wallEnd_[1]:  ##dragging right and down
			width = wallEnd_[0] - wallStart_[0]
			height = wallEnd_[1] - wallStart_[1]
			drag_direction = 'rd'
		elif wallStart_[0] < wallEnd_ [0] and wallStart_[1] > wallEnd_[1]:  ##dragging right and up
			width = wallEnd_[0] - wallStart_[0]
			height = wallStart_[1] - wallEnd_[1]
			drag_direction = 'ru'
		elif wallStart_[0] > wallEnd_[0] and wallStart_[1] < wallEnd_[1]: ##dragging left and down
			width = wallStart_[0] - wallEnd_[0]
			height = wallEnd_[1] - wallStart_[1]
			drag_direction = 'ld'
		elif wallStart_[0] > wallEnd_[0] and wallStart_[1] > wallEnd_[1]:  ##dragging left and up
			width = wallStart_[0] - wallEnd_[0]
			height = wallStart_[1] - wallEnd_[1]
			drag_direction = 'lu'
		elif wallStart_[0] == wallEnd_[0] or wallStart_[1] == wallEnd_[1]:
			return (0,0, 'ru')

		return [width, height, drag_direction]

	def update(self):
		if self.model.pacman.dead:
			self.showing_end_screen = True
		for event in pygame.event.get():
			if event.type == QUIT:
				self.showing_end_screen = True
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE or event.key == K_q:
					self.showing_end_screen = True
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if self.showing_start_screen and self.start_view.start_button_rect.collidepoint(event.pos):
					print("Starting game...")
					self.showing_start_screen = False
			elif event.type == KEYUP: #this is keyReleased!
				if event.key == K_l:
					self.model.load()
				if event.key == K_e:
					self.edit = not(self.edit)
				# if event.key == K_s:
				# 	self.model.marshal()
				if self.edit:
					if event.key == K_w:
						self.add = 'w'
						self.delete = False
					if event.key == K_f:
						self.add = 'f'
						self.delete = False
					if event.key == K_g:
						self.add = 'g'
						self.delete = False
					if event.key == K_p:
						self.add = 'p'
						self.delete = False
					if event.key == K_d:
						self.delete = not(self.delete)
						self.add = ''
					if event.key == K_c:
						self.model.clear_map()
					if event.key == K_l:
						self.model.load()
					if event.key == K_n:
						self.add = "n"

			elif event.type == pygame.MOUSEBUTTONDOWN and self.edit:
				if self.add == 'w':
					self.wallStart = pygame.mouse.get_pos()
				if self.delete:
					mouse_x = pygame.mouse.get_pos()[0]
					mouse_y = pygame.mouse.get_pos()[1]
					self.model.delete_sprite(mouse_x, mouse_y+self.view.scroll_pos)
				

			elif event.type == pygame.MOUSEBUTTONUP and self.edit:
				if self.add == 'w' and self.wallStart:
					wallEnd = pygame.mouse.get_pos()
					
					wallWidth = self.calculateSize(self.wallStart, wallEnd)[0]
					wallHeight = self.calculateSize(self.wallStart, wallEnd)[1]
					direction = self.calculateSize(self.wallStart, wallEnd)[2]
					if direction == 'ru':
						wall_start = (pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]+wallHeight)
					elif direction == 'rd':
						wall_start = (pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])
					elif direction == 'lu':
						wall_start = (pygame.mouse.get_pos()[0]+wallWidth,pygame.mouse.get_pos()[1]+wallHeight)
					elif direction == "ld":
						wall_start = (pygame.mouse.get_pos()[0]+wallWidth,pygame.mouse.get_pos()[1])
					print(f"Width = {wallWidth}   Height =  {wallHeight}")

					self.model.add(self.add, wall_start, self.view.scroll_pos, (wallWidth, wallHeight))
				else:
					self.model.add(self.add, pygame.mouse.get_pos(), self.view.scroll_pos, 0)
				
		keys = pygame.key.get_pressed()
		if keys[K_LEFT]:
			self.model.pacman.set_active(True)
			self.model.movePacman("left")
			self.model.pacman.set_direction("left")
		elif keys[K_RIGHT]:
			self.model.pacman.set_active(True)
			self.model.movePacman("right")
			self.model.pacman.set_direction("right")
		elif keys[K_UP]:
			self.model.pacman.set_active(True)
			self.model.movePacman("up")
			self.model.pacman.set_direction("up")
		elif keys[K_DOWN]:
			self.model.pacman.set_active(True)
			self.model.movePacman("down")
			self.model.pacman.set_direction("down")
		else:
			self.model.pacman.set_active(False)

		if self.showing_start_screen:
			self.start_view.update()
		elif self.showing_end_screen:
			self.end_view.end()
		else:
			self.model.update()
			self.view.update()
###########################################################################
print("Use the arrow keys to move. Press Esc to quit.")
pygame.init()


m = Model()
v = View(m)
sv = Start_Screen_View()
ev = End_Screen_View()
c = Controller(m, v, sv, ev)
while c.keep_going:
	c.update()
	# m.update()
	# v.update()
	sleep(0.04)
print("Goodbye")