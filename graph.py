import pygame
import time
import json
import random
import time
import threading
from pygame.locals import*
from time import sleep
from sprites import *
from seeker import Seeker

NODE_COLOR = (0, 255, 0)
EDGE_COLOR = (0, 0,0) # Yellow for edges (connections)
NODE_RADIUS = 5            # Radius of node circles
EDGE_WIDTH = 2             # Thickness of edge lines

class Graph():
	def __init__(self):
		self.nodes = []
	
	def add_node(self, node):
		if not node in self.nodes:
			self.nodes.append(node)

	def draw_graph(self, screen):
		pass
		# for node in self.nodes:
		# 	pygame.draw.circle(screen, NODE_COLOR, (node.x, node.y), NODE_RADIUS)
		# 	for neighbor in node.neighbors.values():
		# 		if not(neighbor == "none"):
		# 			pygame.draw.line(screen, EDGE_COLOR, (node.x,node.y), (neighbor.x, neighbor.y), EDGE_WIDTH)
	

	def connect_neighbors(self, walls_and_nodes):
		# print(self.maze_graph.nodes)
		for node in self.nodes:
			seeker_right = Seeker(node.x+21, node.y+10, "right")              ####directional seekers to find neighbor nodes
			seeker_left	= Seeker(node.x-1, node.y+10, "left")				######all use collision detect to detect the nodes
			seeker_up = Seeker(node.x+10, node.y-1, "up")					##offset positions so doesnt detect itself
			seeker_down = Seeker(node.x+10, node.y+21, "down")
			seekers = [seeker_right, seeker_left, seeker_up, seeker_down]		## list of the seekers
			count = 0
			for seeker in seekers:
				while not(seeker.found_neighbor):								##seeker has yet to find neighbor
					if seeker.direction == "right":
						seeker.x += 5
					if seeker.direction == "left":
						seeker.x -= 5
					if seeker.direction == "up":
						seeker.y -= 5
					if seeker.direction == "down":
						seeker.y += 5
					count += 5
					for obj in walls_and_nodes:								##checks list of all other nodes and walls
						if count > 400 or count < -100:
							count = 0
							seeker.x = node.x
							seeker.y = node.y
							continue
						if seeker.collides(obj):
							if obj.is_wall():
								node.add_neighbor("none", seeker.direction)
								seeker.found_neighbor = True
								
							if obj.is_node():
								node.add_neighbor(obj, seeker.direction)	
								seeker.found_neighbor = True

	def connect_nodes(self, nodeA, nodeB):  ##bidirectional connections
		if not(nodeB == "None"):
			nodeA.add_neighbor(nodeB)
			nodeB.add_neighbor(nodeA)
		else: 
			nodeA.add_neighbor(nodeB)