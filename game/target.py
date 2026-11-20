"""Target model for the Target Aim Trainer."""
import math


class Target:
    def __init__(self, x, y, base_radius=40, min_radius=12, lifespan_frames=90):
        self.x = int(x)
        self.y = int(y)
        self.base_radius = int(base_radius)
        self.min_radius = int(min_radius)
        self.lifespan_frames = max(1, int(lifespan_frames))
        self.age = 0

    def update(self):
        self.age += 1

    def expired(self):
        return self.age >= self.lifespan_frames

    def visual_radius(self):
        """Return the radius currently drawn on screen."""
        t = min(1.0, self.age / self.lifespan_frames)
        return self.base_radius - (self.base_radius - self.min_radius) * t

    def contains_point(self, x, y):
        """Use the visible radius so the clickable and drawn circles match."""
        return math.hypot(self.x - x, self.y - y) <= self.visual_radius()
