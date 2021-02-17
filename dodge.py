import pygame
import random
import math
import os
import neat

pygame.init()
pygame.font.init()

WIDTH = 800
HEIGHT = 900
FONT = pygame.font.SysFont('comicsans', 50)
clock = pygame.time.Clock()

# Color catalogue
blue = (0, 50, 200)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
