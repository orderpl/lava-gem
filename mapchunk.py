import random
from pygame import Vector2
from copy import deepcopy

def get_perlin_noise(seed, size:tuple[int, int]):
    random.seed(seed)
    return [[random.random() for j in range(size[1])] for i in range(size[0])]
            
NEIGHBORS = [(0, 0), (1, 0), (0, 1), (-1, 0), (0, -1)]
CHUNK_SIZE = 16

class MapChunk:
    chunks_refr:set
    
    tiles:list[list[float]]
    pos:tuple[int, int]
    
    seed:int
    generation_step:int = 0
    generated:bool = False

    def __init__(self, chunks, map_seed:int, pos:tuple[int, int]) -> None:
        self.chunks_refr = chunks
        chunks.append(self)
        self.pos = pos
        self.seed = (map_seed + pos[0] + (pos[1] << 8)) % 2 ** 16
        self.tiles = get_perlin_noise(self.seed, (CHUNK_SIZE, CHUNK_SIZE))

    def step(self):
        match self.generation_step:
            case 0, 1:
                self.smooth()
            case 2:
                self.smooth()
                self.generated = True
                
        self.generation_step += 1
    

    def smooth(self):
        new_tiles = self.tiles
        for i in range(len(self.tiles)):
            for j in range(len(self.tiles[0])):
                new_tiles[i][j] = self.get_neighbors_avg((i, j))
        self.tiles = new_tiles
        
    def get_neighbors_avg(self, pos:tuple[int, int]):
        n_sum = 0
        chunks = []
        tiles = []
        for n in NEIGHBORS:
            if (pos[0] + n[0] < 0 or pos[0] + n[0] > CHUNK_SIZE) or (pos[1] + n[1] < 0 or pos[1] + n[1] > CHUNK_SIZE):
                chunks.append(n)
            else:
                chunks.append((0, 0))
            tiles.append((n[0] + pos[0], n[1] + pos[1]))
        
        for chunk_idx, tile_pos in zip(chunks, tiles):
            n_sum += self.tiles[tile_pos[0]][tile_pos[1]] if chunk_idx == (0, 0) \
                else self.chunks_refr[self.pos[0] + chunk_idx[0]][self.pos[1] + chunk_idx[1]].tiles[tile_pos[0]][tiles[pos[1]]]
            
        return n_sum / len(tiles)
        
    def get_neighboring_chunk(self, pos:tuple[int, int]):
        for c in self.chunks_refr:
            if c.pos == pos:
                return c