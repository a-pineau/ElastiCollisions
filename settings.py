import os
import pygame

# Settings
FPS = 144 
WIDTH = 800
HEIGHT = 800
TITLE = "Elastic Collisions"
MIN_RAD, MAX_RAD = 10, 20
MAX_VEL = 15

# Colours
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 127, 0)
BACKGROUND = (30, 30, 30)

# Folder to save results as pngs
SNAP_FOLDER = os.path.join(os.path.dirname(__file__), "results")
