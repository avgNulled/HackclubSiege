# Imports Modules
import os, sys

import csv, json

import numpy as np
import pandas as pd

import pygame

from typing import List, Tuple, Dict, Union, Optional, Any


# PyGame Setup
WIDTH, HEIGHT = 800, 600
vsync = False

screen = pygame.display.set_mode((WIDTH, HEIGHT), vsync=vsync)

# Player Class
class Player:
    def __init__(self, coords: Tuple[int, int], path: str | None = None) -> None:
        