from boid import *
import pygame
import random

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Boids 2026")
clock = pygame.time.Clock()
running = True

# boid setup
BOID_AMOUNT = 500
START_VELOCITY = 1.5

boids = []
for b in range(BOID_AMOUNT):
    position = [random.uniform(0, screen.get_width()-1), random.uniform(0, screen.get_height()-1)]
    velocity = [random.uniform(-START_VELOCITY, START_VELOCITY), random.uniform(-START_VELOCITY, START_VELOCITY)]
    boids.append(Boid(position, velocity, screen.get_size()))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill("#FFFFFF")

    grid.clear()
    for boid in boids:
        boid.move()
        cell = (int(boid.position[0] // CELL_SIZE),
                int(boid.position[1] // CELL_SIZE))
        grid.setdefault(cell, []).append(boid)
        boid.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()