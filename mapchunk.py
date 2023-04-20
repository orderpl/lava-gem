import random
from pygame import Vector2

def get_perlin_noise(seed, size:tuple[int, int]):
    random.seed(seed)
    return [[random.random() for j in range(size[1])] for i in range(size[0])]


            
neighbors = [(0, 0), (1, 0), (0, 1), (-1, 0), (0, -1)]

class MapChunk:
    def __init__(self, map_seed:int, chunk_pos:tuple[int, int]) -> None:
        self.seed = (map_seed + chunk_pos[0] + (chunk_pos[1] >> 8)) % 2 ** 16
        self.tiles = get_perlin_noise(self.seed, (16, 16))
        
    def smooth(self):
        new_tiles = self.tiles
        for i in range(len(self.tiles)):
            for j in range(len(self.tiles[0])):
                n_sum = 0
                for n in neighbors:
                    try:
                        n_sum += self.tiles[i + n[0]][j + n[1]]
                    except IndexError:
                        pass
                new_tiles[i][j] = n_sum / 5
        self.tiles = new_tiles