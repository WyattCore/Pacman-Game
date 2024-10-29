class Seeker():

	def __init__(self, x, y, direction):
		self.x = x
		self.y = y 
		self.w = 1
		self.h = 1
		self.direction = direction
		self.status = False
		self.move_size = 5
		self.found_neighbor = False
		
	def move(self):
		if self.direction == "right":
			self.x += self.move_size
		elif self.direction == "left":
			self.x -= self.move_size
		elif self.direction == "up":
			self.y -= self.move_size
		elif self.direction == "down":
			self.y += self.move_size
		
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
	