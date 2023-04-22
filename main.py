import pygame
from pygame.math import Vector2
from pygame import transform
from pygame.locals import *
from sys import exit
from mapchunk import MapChunk

pygame.init()
screen = pygame.display.set_mode((800, 450))
res = pygame.math.Vector2(pygame.display.get_window_size())
clock = pygame.time.Clock()

seed = 69

chunks = set()
MapChunk(chunks, seed, (0, 0))
MapChunk(chunks, seed, (1, 0))

for chunk in chunks:
    chunk.step()

txt_size = 48
textures = {
    "stone": transform.scale(pygame.image.load("stone.png").convert(), (txt_size, txt_size)),
    "lava": transform.scale(pygame.image.load("lava.png").convert(), (txt_size, txt_size))
}


def draw_chunk(chunk):
    for i1, x in enumerate(chunk.tiles):
        for i2, y in enumerate(x):
            rect = pygame.Rect(chunk.pos[0] * txt_size * 16 + i1 * txt_size, chunk.pos[1] * txt_size * 16 + i2 * txt_size, txt_size, txt_size)
            if y < .5:
                screen.blit(textures["lava"], rect)
            else:
                screen.blit(textures["stone"], rect)

delta:float = 0
tick:int = 0
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                exit()

        keys_pressed = pygame.key.get_pressed()
        
        for chunk in chunks:
            if tick % 180 == 0:
                chunk.step()
            draw_chunk(chunk)
        
        pygame.display.update()
        screen.fill((0, 0, 0))
        delta = clock.tick(60)
        tick += 1
        print(tick)