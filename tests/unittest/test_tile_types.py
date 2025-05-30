from game.world.tile_types import TILE_TYPES, TileType, get_tile_type


class TestTileType:
    def test_tile_type_creation(self):
        tile = TileType("test", True, (255, 255, 255))
        assert tile.name == "test"
        assert tile.walkable is True
        assert tile.color == (255, 255, 255)

    def test_tile_type_attributes(self):
        walkable_tile = TileType("grass", True, (0, 255, 0))
        non_walkable_tile = TileType("wall", False, (128, 128, 128))

        assert walkable_tile.walkable is True
        assert non_walkable_tile.walkable is False


class TestTileTypesMapping:
    def test_known_tile_colors(self):
        grass_tile = get_tile_type((34, 139, 34))
        assert grass_tile.name == "grass"
        assert grass_tile.walkable is True

        wall_tile = get_tile_type((165, 42, 42))
        assert wall_tile.name == "wall"
        assert wall_tile.walkable is False

        water_tile = get_tile_type((0, 0, 255))
        assert water_tile.name == "water"
        assert water_tile.walkable is False

    def test_unknown_color_returns_default(self):
        unknown_tile = get_tile_type((123, 45, 67))
        assert unknown_tile.name == "default"
        assert unknown_tile.walkable is True

    def test_all_defined_tile_types_exist(self):
        expected_tiles = [
            "void",
            "grass",
            "dirt",
            "stone",
            "water",
            "spawn",
            "chest",
            "wall",
            "default",
        ]
        actual_tiles = [tile.name for tile in TILE_TYPES.values()]

        for expected in expected_tiles:
            assert expected in actual_tiles

    def test_spawn_point_is_walkable(self):
        spawn_tile = get_tile_type((255, 0, 0))
        assert spawn_tile.name == "spawn"
        assert spawn_tile.walkable is True

    def test_chest_is_walkable(self):
        chest_tile = get_tile_type((255, 255, 0))
        assert chest_tile.name == "chest"
        assert chest_tile.walkable is True
