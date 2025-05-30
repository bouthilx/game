from unittest.mock import Mock

from game.engine.scene import Scene
from game.engine.scene_manager import SceneManager


class MockScene(Scene):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.entered = False
        self.exited = False
        self.paused = False
        self.resumed = False
        self.events_handled = []
        self.updated = False
        self.rendered = False

    def on_enter(self):
        self.entered = True

    def on_exit(self):
        self.exited = True

    def on_pause(self):
        self.paused = True

    def on_resume(self):
        self.resumed = True

    def handle_event(self, event):
        self.events_handled.append(event)

    def update(self, dt):
        self.updated = True
        self.update_dt = dt

    def render(self, screen):
        self.rendered = True
        self.render_screen = screen


class TestSceneManager:
    def test_scene_manager_creation(self):
        manager = SceneManager()
        assert len(manager.scenes) == 0

    def test_push_scene(self):
        manager = SceneManager()
        scene = MockScene("test")

        manager.push_scene(scene)

        assert len(manager.scenes) == 1
        assert manager.scenes[0] == scene
        assert scene.entered is True

    def test_push_multiple_scenes_pauses_previous(self):
        manager = SceneManager()
        scene1 = MockScene("scene1")
        scene2 = MockScene("scene2")

        manager.push_scene(scene1)
        manager.push_scene(scene2)

        assert len(manager.scenes) == 2
        assert scene1.paused is True
        assert scene1.entered is True
        assert scene2.entered is True
        assert scene2.paused is False

    def test_pop_scene(self):
        manager = SceneManager()
        scene = MockScene("test")

        manager.push_scene(scene)
        manager.pop_scene()

        assert len(manager.scenes) == 0
        assert scene.exited is True

    def test_pop_scene_resumes_previous(self):
        manager = SceneManager()
        scene1 = MockScene("scene1")
        scene2 = MockScene("scene2")

        manager.push_scene(scene1)
        manager.push_scene(scene2)
        manager.pop_scene()

        assert len(manager.scenes) == 1
        assert manager.scenes[0] == scene1
        assert scene2.exited is True
        assert scene1.resumed is True

    def test_pop_empty_stack(self):
        manager = SceneManager()
        manager.pop_scene()  # Should not crash
        assert len(manager.scenes) == 0

    def test_replace_scene(self):
        manager = SceneManager()
        scene1 = MockScene("scene1")
        scene2 = MockScene("scene2")

        manager.push_scene(scene1)
        manager.replace_scene(scene2)

        assert len(manager.scenes) == 1
        assert manager.scenes[0] == scene2
        assert scene1.exited is True
        assert scene2.entered is True

    def test_replace_scene_empty_stack(self):
        manager = SceneManager()
        scene = MockScene("test")

        manager.replace_scene(scene)

        assert len(manager.scenes) == 1
        assert manager.scenes[0] == scene
        assert scene.entered is True

    def test_handle_event_with_scene(self):
        manager = SceneManager()
        scene = MockScene("test")
        event = Mock()

        manager.push_scene(scene)
        manager.handle_event(event)

        assert len(scene.events_handled) == 1
        assert scene.events_handled[0] == event

    def test_handle_event_no_scenes(self):
        manager = SceneManager()
        event = Mock()

        manager.handle_event(event)  # Should not crash

    def test_update_with_scene(self):
        manager = SceneManager()
        scene = MockScene("test")

        manager.push_scene(scene)
        manager.update(0.016)

        assert scene.updated is True
        assert scene.update_dt == 0.016

    def test_update_no_scenes(self):
        manager = SceneManager()
        manager.update(0.016)  # Should not crash

    def test_render_with_scene(self):
        manager = SceneManager()
        scene = MockScene("test")
        screen = Mock()

        manager.push_scene(scene)
        manager.render(screen)

        assert scene.rendered is True
        assert scene.render_screen == screen

    def test_render_no_scenes(self):
        manager = SceneManager()
        screen = Mock()
        manager.render(screen)  # Should not crash

    def test_only_top_scene_receives_events(self):
        manager = SceneManager()
        scene1 = MockScene("scene1")
        scene2 = MockScene("scene2")
        event = Mock()

        manager.push_scene(scene1)
        manager.push_scene(scene2)
        manager.handle_event(event)

        assert len(scene1.events_handled) == 0
        assert len(scene2.events_handled) == 1
