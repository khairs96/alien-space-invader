import pygame, sys, random
from game import Game
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, OFFSET, GREY, COLOR, FONT_PATH, FONT_SIZE, ALIEN_SHOOT_DELAY, MYSTERY_SHIP_SPAWN_MIN, MYSTERY_SHIP_SPAWN_MAX, EXTRA_LIFE_SPAWN_MIN, EXTRA_LIFE_SPAWN_MAX, SHIELD_SPAWN_MIN, SHIELD_SPAWN_MAX, SHIELD_COLOR, SHIELD_THICKNESS, SHIELD_V_OFFSET_TOP, SHIELD_V_WIDTH, SHIELD_V_HEIGHT

class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH + OFFSET, SCREEN_HEIGHT + 2 * OFFSET))
        pygame.display.set_caption("Python Space Invaders by Khair")
        self.clock = pygame.time.Clock()
        self.game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, OFFSET)
        self.font = pygame.font.Font(FONT_PATH, FONT_SIZE)
        self.score_text_surface = self.font.render("SCORE", False, COLOR)
        self.highscore_text_surface = self.font.render("HIGH-SCORE", False, COLOR)

        self.shoot_laser = pygame.USEREVENT
        pygame.time.set_timer(self.shoot_laser, ALIEN_SHOOT_DELAY)

        self.mystery_ship = pygame.USEREVENT + 1
        pygame.time.set_timer(self.mystery_ship, random.randint(MYSTERY_SHIP_SPAWN_MIN, MYSTERY_SHIP_SPAWN_MAX))

        self.spawn_extra_life = pygame.USEREVENT + 2
        pygame.time.set_timer(self.spawn_extra_life, random.randint(EXTRA_LIFE_SPAWN_MIN, EXTRA_LIFE_SPAWN_MAX))

        self.spawn_shield = pygame.USEREVENT + 3
        pygame.time.set_timer(self.spawn_shield, random.randint(SHIELD_SPAWN_MIN, SHIELD_SPAWN_MAX))

    def run(self):
        while True:
            self._handle_events()
            self._update()
            self._draw()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == self.shoot_laser and self.game.run:
                self.game.alien_shoot_laser()

            if event.type == self.mystery_ship and self.game.run:
                self.game.create_mystery_ship()
                pygame.time.set_timer(self.mystery_ship, random.randint(MYSTERY_SHIP_SPAWN_MIN, MYSTERY_SHIP_SPAWN_MAX))

            if event.type == self.spawn_extra_life and self.game.run:
                self.game.create_extra_life()
                pygame.time.set_timer(self.spawn_extra_life, random.randint(EXTRA_LIFE_SPAWN_MIN, EXTRA_LIFE_SPAWN_MAX))

            if event.type == self.spawn_shield and self.game.run:
                self.game.create_shield()
                pygame.time.set_timer(self.spawn_shield, random.randint(SHIELD_SPAWN_MIN, SHIELD_SPAWN_MAX))

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] and not self.game.run:
                self.game.reset()

    def _update(self):
        if self.game.run:
            self.game.spaceship_group.update()
            self.game.move_aliens()
            self.game.alien_lasers_group.update()
            self.game.mystery_ship_group.update()
            self.game.extra_life_group.update()
            self.game.shield_group.update()
            self.game.check_for_collisions()
            self.game.update_shield()

    def _draw(self):
        self.screen.fill(GREY)

        # UI
        pygame.draw.rect(self.screen, COLOR, (10, 10, SCREEN_WIDTH + OFFSET - 20, SCREEN_HEIGHT + 2 * OFFSET - 20), 2, 0, 60, 60, 60, 60)
        pygame.draw.line(self.screen, COLOR, (25, SCREEN_HEIGHT + 2 * OFFSET - 70), (SCREEN_WIDTH + OFFSET - 25, SCREEN_HEIGHT + 2 * OFFSET - 70), 3)

        level_surface = self.font.render(f"LEVEL {self.game.level:02}", False, COLOR)
        if self.game.run:
            self.screen.blit(level_surface, (570, SCREEN_HEIGHT + 2 * OFFSET - 60, 50, 50))
        else:
            game_over_surface = self.font.render("GAME OVER", False, COLOR)
            self.screen.blit(game_over_surface, (570, SCREEN_HEIGHT + 2 * OFFSET - 60, 50, 50))

        x = 50
        for life in range(self.game.lives):
            self.screen.blit(self.game.spaceship_group.sprite.image, (x, SCREEN_HEIGHT + 2 * OFFSET - 55))
            x += 50

        self.screen.blit(self.score_text_surface, (50, 15, 50, 50))
        formatted_score = str(self.game.score).zfill(5)
        score_surface = self.font.render(formatted_score, False, COLOR)
        self.screen.blit(score_surface, (50, 40, 50, 50))
        self.screen.blit(self.highscore_text_surface, (550, 15, 50, 50))
        formatted_highscore = str(self.game.highscore).zfill(5)
        highscore_surface = self.font.render(formatted_highscore, False, COLOR)
        self.screen.blit(highscore_surface, (625, 40, 50, 50))

        self.game.spaceship_group.draw(self.screen)
        self.game.spaceship_group.sprite.lasers_group.draw(self.screen)
        for obstacle in self.game.obstacles:
            obstacle.blocks_group.draw(self.screen)
        self.game.aliens_group.draw(self.screen)
        self.game.alien_lasers_group.draw(self.screen)
        self.game.mystery_ship_group.draw(self.screen)
        self.game.extra_life_group.draw(self.screen)
        self.game.shield_group.draw(self.screen)

        if self.game.shield_active and self.game.run:
            spaceship = self.game.spaceship_group.sprite
            center_x = spaceship.rect.centerx
            top_y = spaceship.rect.top

            # Define the points for the inverted "V" shape
            point1 = (center_x, top_y - SHIELD_V_OFFSET_TOP)  # Tip of the "V"
            point2 = (center_x - SHIELD_V_WIDTH // 2, top_y - SHIELD_V_OFFSET_TOP + SHIELD_V_HEIGHT) # Bottom-left
            point3 = (center_x + SHIELD_V_WIDTH // 2, top_y - SHIELD_V_OFFSET_TOP + SHIELD_V_HEIGHT) # Bottom-right

            pygame.draw.polygon(self.screen, SHIELD_COLOR, [point1, point2, point3], SHIELD_THICKNESS)

        pygame.display.update()
        self.clock.tick(60)

if __name__ == '__main__':
    main = Main()
    main.run()