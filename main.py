import sys
import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
import json
import os

file_path = 'high_score.json'

def check_high_score_file_exists(file_path):
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            json.dump({'high_score': 0}, file)

def init_high_score():
    check_high_score_file_exists(file_path)
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data['high_score']

def draw_high_score(score):
    font = pygame.font.Font(None, 36)
    text_surface = font.render(f"Top score: {score}", True, (255, 255, 255))
    return text_surface

def write_high_score(score):
    with open(file_path, 'w') as file:
        json.dump({'high_score': score}, file)


def main():
    pygame.init()
    print("Starting asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids")
    clock = pygame.time.Clock()
    
    top_score = init_high_score()
    top_score_text = draw_high_score(top_score)
    

    
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    asteroid_field = AsteroidField()
    Shot.containers = (shots, updatable, drawable)

    Player.containers = (updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    dt = 0
    
    #stating the game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        for obj in updatable:
            obj.update(dt)

        for asteroid in asteroids:
            if player.check_collision(asteroid):
                if player.score > top_score:
                    write_high_score(player.score)
                print("Game over!")
                sys.exit()
            for shot in shots:
                if asteroid.check_collision(shot):
                    asteroid.split()
                    shot.kill()
                    player.add_score()

        screen.fill("black")
        screen.blit(player.draw_score(player.score), (10, 10))
        screen.blit(top_score_text, (10, 50))

        for obj in drawable:
            obj.draw(screen)
        
        pygame.display.flip()

        #frame rate
        dt = clock.tick(60) / 1000
        


if __name__ == "__main__":
    main()