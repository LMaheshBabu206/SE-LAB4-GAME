import unittest
from game.target import Target


class TargetCollisionTests(unittest.TestCase):
    def test_center_is_always_inside(self):
        target = Target(100, 100)
        target.age = 45
        self.assertTrue(target.contains_point(100, 100))

    def test_late_click_outside_visible_radius_is_rejected(self):
        target = Target(100, 100, base_radius=40, min_radius=12, lifespan_frames=90)
        target.age = 80
        self.assertLess(target.visual_radius(), 16)
        self.assertFalse(target.contains_point(120, 100))

    def test_point_on_visible_edge_is_inside(self):
        target = Target(100, 100, base_radius=40, min_radius=12, lifespan_frames=90)
        target.age = 45
        radius = target.visual_radius()
        self.assertTrue(target.contains_point(100 + radius, 100))

    def test_point_outside_visible_edge_is_rejected(self):
        target = Target(100, 100, base_radius=40, min_radius=12, lifespan_frames=90)
        target.age = 45
        self.assertFalse(target.contains_point(100 + target.visual_radius() + 1, 100))


if __name__ == "__main__":
    unittest.main()
