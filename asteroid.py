import pygame
import random
from constants import *
from circleshape import CircleShape



class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
            pygame.draw.circle(screen, "white", self.position, self.radius, 2)

    def update(self, dt):
            self.position += (self.velocity * dt)

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        angle_amount = random.uniform(20, 50)
        angle_left = self.velocity.rotate(angle_amount)
        angle_right = self.velocity.rotate(-angle_amount)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        
        asteroid_left = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid_left.velocity = angle_left * 1.2
        
       
        asteroid_right = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid_right.velocity = angle_right * 1.2