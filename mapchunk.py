import random
from pygame import Vector2
from copy import deepcopy

def get_perlin_noise(seed, size:tuple[int, int]):
    random.seed(seed)
    return [[random.random() for j in range(size[1])] for i in range(size[0])]
            
neighbors = [(0, 0), (1, 0), (0, 1), (-1, 0), (0, -1)]

class MapChunk:
    tiles:list[list[float]]
    perlin:list[list[float]]
    pos:tuple[int, int]
    neighbors_noises:dict[int, list[float]]
    
    seed:int
    generated:bool = False

    def __init__(self, map_seed:int, pos:tuple[int, int]) -> None:
        self.pos = pos
        self.seed = (map_seed + pos[0] + (pos[1] << 8)) % 2 ** 16
        self.perlin = get_perlin_noise(self.seed, (16, 16))

    def get_neighbors(self, chunklist:list):
        for idx, chunk in enumerate(neighbors):
            tiles = []
            
            self.neighbors_noises.update({idx})

    def generate(self):
        self.generated = True
        self.tiles = deepcopy(self.perlin)
        for i in range(2):
            self.tiles = self.smooth(self.tiles)

    def smooth(self, tiles:list[list[float]]):
        new_tiles = tiles
        for i in range(len(tiles)):
            for j in range(len(tiles[0])):
                n_sum = 0
                for n in neighbors:
                    try:
                        n_sum += tiles[i + n[0]][j + n[1]]
                    except IndexError:
                        pass
                new_tiles[i][j] = n_sum / 5
        return new_tiles