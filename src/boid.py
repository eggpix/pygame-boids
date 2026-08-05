import pygame
import math
import random

BOID_RADIUS = 2
BOID_COLOR = "#000000"

class boid():
    def __init__(self, position):
        self.position = position
        self.direction = random.uniform(0, math.pi)

    def move(self):
        self.position[0] += math.cos(self.direction)
        self.position[1] += math.sin(self.direction)

    def draw(self, screen):
        pygame.draw.circle(screen, BOID_COLOR, self.position, BOID_RADIUS)