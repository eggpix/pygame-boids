import pygame
import math

BOID_RADIUS = 2
BOID_COLOR = "#404040"

DETECTION_RADIUS = 60
BOID_FOV = math.radians(180)
CELL_SIZE = DETECTION_RADIUS
MINIMUM_BOID_DISTANCE = 30
MIN_SPEED = 1
MAX_SPEED = 2
MAX_STEER_FORCE = 1

ALIGNMENT_STEER = 0.1
COHESION_STEER = 0.02
SEPARATION_WEIGHT = 0.5

grid = {}

class Boid():
    def __init__(self, position, velocity, screen_size):
        self.position = [float(position[0]), float(position[1])]
        self.velocity = [float(velocity[0]), float(velocity[1])]
        self.screen_size = screen_size

    def move(self):

        cell_x = int(self.position[0] // CELL_SIZE)
        cell_y = int(self.position[1] // CELL_SIZE)

        alignment_x = 0
        alignment_y = 0

        cohesion_dx = 0
        cohesion_dy = 0

        separation_x = 0
        separation_y = 0

        count = 0
        separation_count = 0

        self_direction = math.atan2(self.velocity[1], self.velocity[0])

        grid_width = self.screen_size[0] // CELL_SIZE
        grid_height = self.screen_size[1] // CELL_SIZE

        for y in range(cell_y - 1, cell_y + 2):
            for x in range(cell_x - 1, cell_x + 2):
                neighbor_x = (x + grid_width) % grid_width
                neighbor_y = (y + grid_height) % grid_height
                for boid in grid.get((neighbor_x, neighbor_y), []):
                    if boid is self: continue

                    dx = self.position[0] - boid.position[0]
                    if dx > self.screen_size[0] / 2: dx -= self.screen_size[0]
                    elif dx < -self.screen_size[0] / 2: dx += self.screen_size[0]
                    dy = self.position[1] - boid.position[1]
                    if dy > self.screen_size[1] / 2: dy -= self.screen_size[1]
                    elif dy < -self.screen_size[1] / 2: dy += self.screen_size[1]
                    boid_distance = math.hypot(dx, dy)

                    direction_to_boid = math.atan2(-dy, -dx)
                    angle_diff = (direction_to_boid - self_direction + math.pi) % (2 * math.pi) - math.pi
                    boid_in_view = abs(angle_diff) <= BOID_FOV / 2

                    if 0 < boid_distance < MINIMUM_BOID_DISTANCE:
                        separation_x += dx / (boid_distance * boid_distance)
                        separation_y += dy / (boid_distance * boid_distance)
                        separation_count += 1
                    elif 0 < boid_distance < DETECTION_RADIUS and boid_in_view:
                        alignment_x += boid.velocity[0]
                        alignment_y += boid.velocity[1]

                        cohesion_dx += -dx
                        cohesion_dy += -dy

                        count += 1

        if count:
            alignment_x /= count
            alignment_y /= count
            steer_x = alignment_x - self.velocity[0]
            steer_y = alignment_y - self.velocity[1]
            magnitude = math.hypot(steer_x, steer_y)
            if magnitude > MAX_STEER_FORCE:
                scale = MAX_STEER_FORCE / magnitude
                steer_x *= scale
                steer_y *= scale
            self.velocity[0] += steer_x * ALIGNMENT_STEER
            self.velocity[1] += steer_y * ALIGNMENT_STEER

            cohesion_dx /= count
            cohesion_dy /= count

            distance = math.hypot(cohesion_dx, cohesion_dy)

            if distance > 0:
                cohesion_dx /= distance
                cohesion_dy /= distance

                steer_x = cohesion_dx - self.velocity[0]
                steer_y = cohesion_dy - self.velocity[1]

                magnitude = math.hypot(steer_x, steer_y)

                if magnitude > MAX_STEER_FORCE:
                    scale = MAX_STEER_FORCE / magnitude
                    steer_x *= scale
                    steer_y *= scale

                self.velocity[0] += steer_x * COHESION_STEER
                self.velocity[1] += steer_y * COHESION_STEER
        if separation_count:
            separation_x /= separation_count
            separation_y /= separation_count

            steer_x = separation_x - self.velocity[0]
            steer_y = separation_y - self.velocity[1]

            magnitude = math.hypot(steer_x, steer_y)

            if magnitude > MAX_STEER_FORCE:
                scale = MAX_STEER_FORCE / magnitude
                steer_x *= scale
                steer_y *= scale

            self.velocity[0] += steer_x * SEPARATION_WEIGHT
            self.velocity[1] += steer_y * SEPARATION_WEIGHT

        speed = math.hypot(*self.velocity)

        if speed > MAX_SPEED:
            scale = MAX_SPEED / speed
            self.velocity[0] *= scale
            self.velocity[1] *= scale

        elif speed < MIN_SPEED:
            scale = MIN_SPEED / speed
            self.velocity[0] *= scale
            self.velocity[1] *= scale
                
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

        self.position[0] %= self.screen_size[0]
        self.position[1] %= self.screen_size[1]

    def draw(self, screen):
        angle = math.atan2(self.velocity[1], self.velocity[0])
        points = [
            (2, 0),     # nose
            (-3, 2),    # rear top
            (-2, 0),    # tail notch
            (-3, -2),   # rear bottom
        ]

        cos_a = math.cos(angle)
        sin_a = math.sin(angle)

        transformed = []
        for px, py in points:
            x = self.position[0] + px * cos_a - py * sin_a
            y = self.position[1] + px * sin_a + py * cos_a
            transformed.append((int(x), int(y)))

        pygame.draw.polygon(screen, BOID_COLOR, transformed)