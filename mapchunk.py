import random
from pygame import Vector2
from copy import deepcopy

def get_perlin_noise(seed, size:tuple[int, int]):
    random.seed(seed)
    return [[random.random() for j in range(size[1])] for i in range(size[0])]
            
NEIGHBORS = [(0, 0), (1, 0), (0, 1), (-1, 0), (0, -1)]
CHUNK_SIZE = 128

class MapChunk:
    chunks_refr:set
    
    tiles:list[list[float]]
    pos:tuple[int, int]
    
    seed:int
    generation_step:int = 0
    generated:bool = False
    pos:tuple[int, int]

    def __init__(self, chunks, map_seed:int, pos:tuple[int, int]) -> None:
        self.chunks_refr = chunks
        chunks.add(self)
        self.pos = pos
        self.seed = (map_seed + pos[0] + (pos[1] << 8)) % 2 ** 16
        self.tiles = get_perlin_noise(self.seed, (CHUNK_SIZE, CHUNK_SIZE))

    def __repr__(self) -> str:
        return f"""<MapChunk object>"""

    def generate(self):
        for i in range(5):
            self.smooth()    

    def smooth(self):
        new_tiles = self.tiles
        for i in range(len(self.tiles)):
            for j in range(len(self.tiles[0])):
                new_tiles[i][j] = self.get_neighbors_avg((i, j))
        self.tiles = new_tiles
        
    def get_neighbors_avg(self, pos:tuple[int, int]):
        n_sum = 0

        for n in NEIGHBORS:
            try:
                n_sum += self.tiles[pos[0] + n[0]][pos[1] + n[1]]
            except IndexError:
                n_sum += random.random()
            
        return n_sum / len(NEIGHBORS)