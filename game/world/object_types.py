from typing import Dict, Tuple


class ObjectType:
    def __init__(
        self,
        name: str,
        size: Tuple[int, int],  # Size in tiles (width, height)
        sprite_path: str = None,
        walkable: bool = False,
    ):
        self.name = name
        self.size = size  # (width_tiles, height_tiles)
        self.sprite_path = sprite_path
        self.walkable = walkable


# Object definitions - colors map to object types
OBJECT_TYPES: Dict[Tuple[int, int, int], ObjectType] = {
    # Trees and nature
    (50, 150, 50): ObjectType("small_tree", (1, 1), "assets/sprites/small_tree.png"),
    (40, 120, 40): ObjectType("large_tree", (2, 2), "assets/sprites/large_tree.png"),
    (60, 180, 60): ObjectType("bush", (1, 1), "assets/sprites/bush.png"),
    # Buildings
    (150, 75, 0): ObjectType("house", (3, 2), "assets/sprites/house.png", walkable=False),
    (120, 60, 0): ObjectType("shed", (2, 1), "assets/sprites/shed.png", walkable=False),
    (100, 50, 0): ObjectType("well", (1, 1), "assets/sprites/well.png", walkable=False),
    # Interactive objects
    (200, 200, 0): ObjectType(
        "chest", (1, 1), "assets/sprites/chest.png", walkable=True
    ),
    (180, 100, 50): ObjectType(
        "barrel", (1, 1), "assets/sprites/barrel.png", walkable=False
    ),
    # Infrastructure
    (100, 100, 100): ObjectType(
        "stone_wall", (1, 1), "assets/sprites/stone_wall.png", walkable=False
    ),
    (80, 60, 40): ObjectType(
        "wooden_fence", (1, 1), "assets/sprites/wooden_fence.png", walkable=False
    ),
    (150, 150, 150): ObjectType(
        "bridge", (3, 1), "assets/sprites/bridge.png", walkable=True
    ),
}


def get_object_type(color: Tuple[int, int, int]) -> ObjectType:
    """Get object type from color, returns None if not found."""
    return OBJECT_TYPES.get(color, None)


def is_object_color(color: Tuple[int, int, int]) -> bool:
    """Check if color represents an object."""
    return color in OBJECT_TYPES