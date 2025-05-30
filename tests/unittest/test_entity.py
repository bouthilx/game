from game.entities.entity import Entity


class TestEntity:
    def test_entity_creation(self):
        entity = Entity(10, 20, 32, 32)
        assert entity.x == 10
        assert entity.y == 20
        assert entity.width == 32
        assert entity.height == 32
        assert entity.velocity_x == 0.0
        assert entity.velocity_y == 0.0
        assert entity.speed == 100.0
        assert entity.active is True

    def test_entity_default_values(self):
        entity = Entity()
        assert entity.x == 0
        assert entity.y == 0
        assert entity.width == 32
        assert entity.height == 32

    def test_position_property(self):
        entity = Entity(15, 25)
        assert entity.position == (15, 25)

        entity.position = (30, 40)
        assert entity.x == 30
        assert entity.y == 40

    def test_rect_property(self):
        entity = Entity(10, 20, 32, 48)
        rect = entity.rect
        assert rect.x == 10
        assert rect.y == 20
        assert rect.width == 32
        assert rect.height == 48

    def test_update_with_velocity(self):
        entity = Entity(0, 0)
        entity.velocity_x = 100
        entity.velocity_y = 50

        entity.update(0.1)  # 100ms

        assert entity.x == 10  # 100 * 0.1
        assert entity.y == 5  # 50 * 0.1

    def test_update_inactive_entity(self):
        entity = Entity(0, 0)
        entity.velocity_x = 100
        entity.velocity_y = 50
        entity.active = False

        entity.update(0.1)

        assert entity.x == 0
        assert entity.y == 0
