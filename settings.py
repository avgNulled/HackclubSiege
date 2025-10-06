# Import Modules
import os, sys
import colorsys

import csv, json

import pygame
from pygame.locals import K_w, K_a, K_s, K_d, K_UP, K_LEFT, K_DOWN, K_RIGHT

import random

# Pygame Init
pygame.init()


# Hard-Coded Variables
WIDTH, HEIGHT = 800, 600
vsync = False

max_fps = 200

screen = pygame.display.set_mode((WIDTH, HEIGHT), vsync=vsync)
pygame.display.set_caption("HackclubSiege - Coins")

clock = pygame.time.Clock()


# Sprite Classes
class Player(pygame.sprite.Sprite):
    """PyGame Player Sprite"""

    def __init__(self) -> None:
        super().__init__()

        # Player Stats
        self.screen = screen

        self.speed = 5.0

        # Player Surface
        player_image_path = "player.png"
        self.surf = pygame.image.load(player_image_path)
        self.rect = self.surf.get_rect()

        # Player Score
        self.score = 0

    def update(self) -> None:
        # Player I/O Update
        pressed_keys = pygame.key.get_pressed()

        # WASD/Arrows
        if pressed_keys[K_w] or pressed_keys[K_UP]:
            self.rect.y -= self.speed

        if pressed_keys[K_a] or pressed_keys[K_LEFT]:
            self.rect.x -= self.speed

        if pressed_keys[K_s] or pressed_keys[K_DOWN]:
            self.rect.y += self.speed

        if pressed_keys[K_d] or pressed_keys[K_RIGHT]:
            self.rect.x += self.speed

        # Lock to Screen
        if self.rect.x < 0:
            self.rect.x = 0

        if WIDTH - self.surf.get_width() < self.rect.x:
            self.rect.x = WIDTH - self.surf.get_width()

        if self.rect.y < 0:
            self.rect.y = 0

        if HEIGHT - self.surf.get_height() < self.rect.y:
            self.rect.y = HEIGHT - self.surf.get_height()

        # Blit Player to Screen
        self.screen.blit(self.surf, self.rect)


class Coin(pygame.sprite.Sprite):
    """PyGame Coin/Currency Class"""

    def __init__(self) -> None:
        super().__init__()

        # Screen Surface
        self.screen = screen

        # Coin Surface
        coin_image_path = "coin.png"
        self.surf = pygame.image.load(coin_image_path)
        self.rect = self.surf.get_rect()

        # Random X, Y coordinate
        self.rect.x = random.randint(0, WIDTH - self.surf.get_width())
        self.rect.y = random.randint(0, HEIGHT - self.surf.get_height())

    def update(self) -> None:
        self.screen.blit(self.surf, self.rect)


class Background(pygame.sprite.Sprite):
    """PyGame Background Class"""

    def __init__(self) -> None:
        super().__init__()

        # Current Hue
        self.current_hue = 0.0

        # Background Surface
        self.surf = get_rotating_gradient(self.current_hue)
        self.rect = self.surf.get_rect()

        # Scoreboard Surface
        self.renderer = pygame.font.SysFont("Sans Comic", 100)
        self.text = self.renderer.render("", False, 30)

        # Screen Surface
        self.screen = screen

    def update(self) -> None:
        # Rotates Colour
        self.surf = get_rotating_gradient(self.current_hue)

        self.current_hue += 1.0 / ((clock.get_fps() + 1**-5) * 5.0)

        if 1.0 < self.current_hue:
            self.current_hue = 0.0

        self.screen.blit(self.surf, self.rect)

    def score_update(self, score: int) -> None:
        self.text = self.renderer.render(f"Score: {score}", False, (255, 255, 255))
        self.text_rect = self.text.get_rect()

        self.screen.blit(self.text, self.text_rect)


def get_rotating_gradient(hue_offset: int | float) -> pygame.Surface:
    """Rotating Gradient"""
    global WIDTH, HEIGHT
    gradient = pygame.Surface((WIDTH, HEIGHT))

    for x in range(WIDTH):
        # Calculate Hue Shift
        hue = ((x / WIDTH) + hue_offset) % 1.0
        r, g, b = colorsys.hsv_to_rgb(hue, 1, 1)
        colour = tuple(map(lambda c: int(c * 255), [r, g, b]))
        pygame.draw.line(gradient, colour, (x, 0), (x, HEIGHT))

    return gradient
