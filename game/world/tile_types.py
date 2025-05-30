from typing import Tuple


class TileType:
    def __init__(self, name: str, walkable: bool, color: Tuple[int, int, int]):
        self.name = name
        self.walkable = walkable
        self.color = color


TILE_TYPES = {
    (0, 0, 0): TileType("void", False, (0, 0, 0)),
    (34, 139, 34): TileType("grass", True, (34, 139, 34)),
    (139, 69, 19): TileType("dirt", True, (139, 69, 19)),
    (128, 128, 128): TileType("stone", True, (128, 128, 128)),
    (0, 0, 255): TileType("water", False, (0, 100, 255)),
    (255, 0, 0): TileType("spawn", True, (34, 139, 34)),
    (255, 255, 0): TileType("chest", True, (255, 255, 0)),
    (165, 42, 42): TileType("wall", False, (100, 50, 50)),
    (255, 255, 255): TileType("default", True, (34, 139, 34)),
}


def get_tile_type(color: Tuple[int, int, int]) -> TileType:
    return TILE_TYPES.get(color, TILE_TYPES[(255, 255, 255)])
