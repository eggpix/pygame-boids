import pygame
import boid
import random

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

# boid setup
BOID_AMOUNT = 1000
boids = []
for b in range(BOID_AMOUNT):
    position = [random.randint(0, screen.get_width()-1), random.uniform(0, screen.get_height()-1)]
    boids.append(boid.boid(position))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill("#FFFFFF")

    for b in boids:
        b.move()
        b.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()