import pygame
from settings import LASER_COLOR, LASER_WIDTH, LASER_HEIGHT

class Laser(pygame.sprite.Sprite):
	def __init__(self, position, speed, screen_height):
		super().__init__()
		self.image = pygame.Surface((LASER_WIDTH, LASER_HEIGHT))
		self.image.fill(LASER_COLOR)
		self.rect = self.image.get_rect(center = position)
		self.speed = speed
		self.screen_height = screen_height

	def update(self):
		self.rect.y -= self.speed
		if self.rect.y > self.screen_height + LASER_HEIGHT or self.rect.y < 0:
			self.kill()