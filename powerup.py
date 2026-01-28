import pygame
import random
from settings import EXTRA_LIFE_IMAGE_PATH, SHIELD_POWERUP_IMAGE_PATH, SCREEN_WIDTH

class ExtraLife(pygame.sprite.Sprite):
    def __init__(self, screen_width, offset):
        super().__init__()
        original_image = pygame.image.load(EXTRA_LIFE_IMAGE_PATH)
        self.image = pygame.transform.scale(original_image, (30, 24))
        self.rect = self.image.get_rect(center=(random.randint(offset, screen_width), -50))
        self.speed = 2

    def update(self):
        from settings import SCREEN_HEIGHT
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

class Shield(pygame.sprite.Sprite):
    def __init__(self, screen_width, offset):
        super().__init__()
        original_image = pygame.image.load(SHIELD_POWERUP_IMAGE_PATH)
        self.image = pygame.transform.scale(original_image, (30, 38.65))
        self.rect = self.image.get_rect(center=(random.randint(offset, screen_width), -50))
        self.speed = 3

    def update(self):
        from settings import SCREEN_HEIGHT
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()