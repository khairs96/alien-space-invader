import pygame, random
from spaceship import Spaceship
from obstacle import Obstacle, grid
from alien import Alien, MysteryShip
from laser import Laser
from powerup import ExtraLife, Shield
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, OFFSET, ALIEN_MOVE_DOWN_DISTANCE, EXPLOSION_SOUND_PATH, MUSIC_PATH, HIGHSCORE_FILE, POWERUP_SOUND_PATH, ALIEN_START_X, ALIEN_START_Y, ALIEN_HORIZONTAL_SPACING, ALIEN_VERTICAL_SPACING

class Game:
    def __init__(self, screen_width, screen_height, offset):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.offset = offset
        self.spaceship_group = pygame.sprite.GroupSingle()
        self.spaceship_group.add(Spaceship(self.screen_width, self.screen_height, self.offset))
        self.obstacles = self.create_obstacles()
        self.aliens_group = pygame.sprite.Group()
        self.alien_start_x = ALIEN_START_X
        self.alien_start_y = ALIEN_START_Y
        self.alien_horizontal_spacing = ALIEN_HORIZONTAL_SPACING
        self.alien_vertical_spacing = ALIEN_VERTICAL_SPACING
        self.create_aliens()
        self.aliens_direction = 1
        self.alien_lasers_group = pygame.sprite.Group()
        self.mystery_ship_group = pygame.sprite.GroupSingle()
        self.extra_life_group = pygame.sprite.Group()
        self.shield_group = pygame.sprite.Group()
        self.lives = 3
        self.run = True
        self.score = 0
        self.highscore = 0
        self.explosion_sound = pygame.mixer.Sound(EXPLOSION_SOUND_PATH)
        self.powerup_sound = pygame.mixer.Sound(POWERUP_SOUND_PATH)
        self.load_highscore()
        pygame.mixer.music.load(MUSIC_PATH)
        pygame.mixer.music.play(-1)
        self.shield_active = False
        self.shield_timer = 0
        from settings import SHIELD_DURATION
        self.shield_duration = SHIELD_DURATION
        self.level = 1

    def create_obstacles(self):
        from obstacle import grid
        obstacle_width = len(grid[0]) * 3
        gap = (self.screen_width + self.offset - (4 * obstacle_width))/5
        obstacles = []
        for i in range(4):
            offset_x = (i + 1) * gap + i * obstacle_width
            obstacle = Obstacle(offset_x, self.screen_height - 100)
            obstacles.append(obstacle)
        return obstacles

    def create_aliens(self):
        for row in range(5):
            for column in range(11):
                x = self.alien_start_x + column * self.alien_horizontal_spacing
                y = self.alien_start_y + row * self.alien_vertical_spacing

                if row == 0:
                    alien_type = 3
                elif row in (1,2):
                    alien_type = 2
                else:
                    alien_type = 1

                alien = Alien(alien_type, x + self.offset/2, y)
                self.aliens_group.add(alien)

    def move_aliens(self):
        self.aliens_group.update(self.aliens_direction)

        alien_sprites = self.aliens_group.sprites()
        for alien in alien_sprites:
            if alien.rect.right >= self.screen_width + self.offset/2:
                self.aliens_direction = -1
                self.alien_move_down(ALIEN_MOVE_DOWN_DISTANCE)
            elif alien.rect.left <= self.offset/2:
                self.aliens_direction = 1
                self.alien_move_down(ALIEN_MOVE_DOWN_DISTANCE)

    def alien_move_down(self, distance):
        if self.aliens_group:
            for alien in self.aliens_group.sprites():
                alien.rect.y += distance

            # Check for game over if aliens reach the bottom
            for alien in self.aliens_group:
                if alien.rect.bottom >= self.spaceship_group.sprite.rect.top:
                    self.game_over()
                    break

    def alien_shoot_laser(self):
        if self.aliens_group.sprites():
            random_alien = random.choice(self.aliens_group.sprites())
            from settings import ALIEN_LASER_SPEED
            laser_sprite = Laser(random_alien.rect.center, ALIEN_LASER_SPEED, self.screen_height)
            self.alien_lasers_group.add(laser_sprite)

    def create_mystery_ship(self):
        self.mystery_ship_group.add(MysteryShip(self.screen_width, self.offset))

    def create_extra_life(self):
        self.extra_life_group.add(ExtraLife(self.screen_width, self.offset))

    def create_shield(self):
        self.shield_group.add(Shield(self.screen_width, self.offset))

    def check_for_collisions(self):
        # Spaceship Lasers
        if self.spaceship_group.sprite.lasers_group:
            for laser_sprite in self.spaceship_group.sprite.lasers_group:
                aliens_hit = pygame.sprite.spritecollide(laser_sprite, self.aliens_group, True)
                if aliens_hit:
                    self.explosion_sound.play()
                    for alien in aliens_hit:
                        self.score += alien.type * 100
                        self.check_for_highscore()
                        laser_sprite.kill()

                if pygame.sprite.spritecollide(laser_sprite, self.mystery_ship_group, True):
                    self.score += 500
                    self.explosion_sound.play()
                    self.check_for_highscore()
                    laser_sprite.kill()

                for obstacle in self.obstacles:
                    if pygame.sprite.spritecollide(laser_sprite, obstacle.blocks_group, True):
                        laser_sprite.kill()

        # Alien Lasers
        if self.alien_lasers_group:
            for laser_sprite in self.alien_lasers_group:
                if pygame.sprite.spritecollide(laser_sprite, self.spaceship_group, False):
                    if not self.shield_active:
                        laser_sprite.kill()
                        self.lives -= 1
                        if self.lives == 0:
                            self.game_over()
                    else:
                        self.explosion_sound.play() # Maybe a different sound for shield hit
                        laser_sprite.kill()

                for obstacle in self.obstacles:
                    if pygame.sprite.spritecollide(laser_sprite, obstacle.blocks_group, True):
                        laser_sprite.kill()

        # Alien Obstacle Collision
        if self.aliens_group:
            for alien in self.aliens_group:
                for obstacle in self.obstacles:
                    pygame.sprite.spritecollide(alien, obstacle.blocks_group, True)

                if pygame.sprite.spritecollide(alien, self.spaceship_group, False):
                    self.game_over()

        # Power-ups
        if self.extra_life_group:
            for extra_life in pygame.sprite.spritecollide(self.spaceship_group.sprite, self.extra_life_group, True):
                self.lives += 1
                self.powerup_sound.play()

        if self.shield_group:
            for shield in pygame.sprite.spritecollide(self.spaceship_group.sprite, self.shield_group, True):
                self.shield_active = True
                self.shield_timer = pygame.time.get_ticks()
                self.powerup_sound.play()

        # Check for level completion
        if not self.aliens_group.sprites() and self.run:
            self.level_complete()

    def level_complete(self):
        self.level += 1
        self.aliens_group.empty()
        self.alien_lasers_group.empty()
        self.mystery_ship_group.empty()
        self.extra_life_group.empty()
        self.shield_group.empty()
        self.create_aliens()  # Recreate aliens for the next level

    def game_over(self):
        self.run = False

    def reset(self):
        self.run = True
        self.lives = 3
        self.score = 0
        self.level = 1
        self.spaceship_group.sprite.reset()
        self.aliens_group.empty()
        self.alien_lasers_group.empty()
        self.mystery_ship_group.empty()
        self.extra_life_group.empty()
        self.shield_group.empty()
        self.obstacles = self.create_obstacles()
        self.create_aliens()
        self.shield_active = False

    def check_for_highscore(self):
        from settings import HIGHSCORE_FILE
        if self.score > self.highscore:
            self.highscore = self.score
            with open(HIGHSCORE_FILE, "w") as file:
                file.write(str(self.highscore))

    def load_highscore(self):
        from settings import HIGHSCORE_FILE
        try:
            with open(HIGHSCORE_FILE, "r") as file:
                self.highscore = int(file.read())
        except FileNotFoundError:
            self.highscore = 0

    def update_shield(self):
        if self.shield_active:
            if pygame.time.get_ticks() - self.shield_timer >= self.shield_duration:
                self.shield_active = False