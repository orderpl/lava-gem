import pygame
from pygame import Vector2
from pygame.locals import *
from sys import exit
import mapchunk

pygame.init()
screen = pygame.display.set_mode((1600, 900))
res = pygame.math.Vector2(pygame.display.get_window_size())
clock = pygame.time.Clock()

chunk = mapchunk.MapChunk(0, (0, 0))


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

        keys_pressed = pygame.key.get_pressed()
        
        for i1, x in enumerate(chunk.tiles):
            for i2, y in enumerate(x):
                pygame.draw.rect(screen, [y * 255] * 3, pygame.Rect(100 + i1 * 10, 100 + i2 * 10, 10, 10))
        
        pygame.display.update()
        screen.fill((0, 0, 0))
        clock.tick(60)