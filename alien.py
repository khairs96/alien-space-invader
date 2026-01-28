import pygame, random
from settings import ALIEN1_IMAGE_PATH, ALIEN2_IMAGE_PATH, ALIEN3_IMAGE_PATH, MYSTERY_SHIP_IMAGE_PATH, SCREEN_WIDTH, OFFSET, MYSTERY_SHIP_SPEED

class Alien(pygame.sprite.Sprite):
	def __init__(self, type, x, y):
		super().__init__()
		self.type = type
		if type == 1:
			path = ALIEN1_IMAGE_PATH
		elif type == 2:
			path = ALIEN2_IMAGE_PATH
		elif type == 3:
			path = ALIEN3_IMAGE_PATH
		self.image = pygame.image.load(path)
		self.rect = self.image.get_rect(topleft = (x, y))

	def update(self, direction):
		self.rect.x += direction

class MysteryShip(pygame.sprite.Sprite):
	def __init__(self, screen_width, offset):
		super().__init__()
		self.screen_width = screen_width
		self.offset = offset
		self.image = pygame.image.load(MYSTERY_SHIP_IMAGE_PATH)

		x = random.choice([self.offset/2, self.screen_width + self.offset - self.image.get_width()])
		if x == self.offset/2:
			self.speed = MYSTERY_SHIP_SPEED
		else:
			self.speed = -MYSTERY_SHIP_SPEED

		self.rect = self.image.get_rect(topleft = (x, 90))

	def update(self):
		self.rect.x += self.speed
		if self.rect.right > self.screen_width + self.offset/2:
			self.kill()
		elif self.rect.left < self.offset/2:
			self.kill()