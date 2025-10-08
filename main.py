#!/bin/python
import os, sys
import colorsys

import pygame

from settings import *


# Mainloop
if __name__ == "__main__":
    # PyGame Init
    pygame.init()
    pygame.font.init()

    # Player Sprite
    player = Player()

    # Coins Sprites
    max_coins = 10
    coins = pygame.sprite.Group(*[Coin() for _ in range(max_coins)])

    # Background Sprite
    background = Background()

    # Running Loop
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update Sprites
        background.update()
        coins.update()

        background.score_update(player.score)
        player.update()

        # Coin Collection
        for coin in iter(coins):
            if pygame.sprite.collide_rect(coin, player):
                player.score += 1

                coins.add(Coin())
                coin.kill()

                print(player.score)

        clock.tick(max_fps)
        pygame.display.flip()
