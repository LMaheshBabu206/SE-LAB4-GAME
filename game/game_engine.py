"""Game logic, difficulty configuration, scoring and rendering."""
import random
import pygame
from .target import Target

WHITE = (245, 248, 255)
RED = (220, 60, 70)
GREEN = (70, 220, 140)
DARK = (22, 25, 34)
PANEL = (35, 40, 54)

DIFFICULTIES = {
    "Easy": {"lifespan": 120, "radius": 45},
    "Medium": {"lifespan": 90, "radius": 40},
    "Hard": {"lifespan": 60, "radius": 35},
}


class GameEngine:
    def __init__(self, width, height, difficulty="Medium"):
        self.width = width
        self.height = height
        self.margin = 55
        self.hud_height = 58
        self.round_seconds = 30
        self.font = pygame.font.SysFont("Arial", 24)
        self.large_font = pygame.font.SysFont("Arial", 42, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 18)
        self.sound_enabled = True
        self._load_sounds()
        self.start_round(difficulty)

    def _load_sounds(self):
        """Load optional WAV files; game remains playable if audio is unavailable."""
        self.sounds = {}
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            for name in ("hit", "miss", "game_over"):
                path = f"assets/sounds/{name}.wav"
                try:
                    self.sounds[name] = pygame.mixer.Sound(path)
                except (pygame.error, FileNotFoundError):
                    pass
        except pygame.error:
            self.sound_enabled = False

    def play_sound(self, name):
        sound = self.sounds.get(name)
        if self.sound_enabled and sound:
            try:
                sound.play()
            except pygame.error:
                pass

    def start_round(self, difficulty="Medium"):
        self.difficulty = difficulty if difficulty in DIFFICULTIES else "Medium"
        self.settings = DIFFICULTIES[self.difficulty]
        self.hits = 0
        self.misses = 0
        self.score = 0
        self.time_left_ms = self.round_seconds * 1000
        self.game_over = False
        self.target = self._spawn_target()
        self._last_update = pygame.time.get_ticks()

    def _spawn_target(self):
        radius = self.settings["radius"]
        x = random.randint(self.margin + radius, self.width - self.margin - radius)
        y = random.randint(self.margin + self.hud_height + radius,
                           self.height - self.margin - radius)
        return Target(x, y, base_radius=radius, min_radius=10,
                      lifespan_frames=self.settings["lifespan"])

    def handle_event(self, event):
        if self.game_over or event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return
        x, y = event.pos
        if self.target.contains_point(x, y):
            self.hits += 1
            self.score += 1
            self.play_sound("hit")
        else:
            self.misses += 1
            self.play_sound("miss")
        self.target = self._spawn_target()

    def handle_input(self):
        pass

    def update(self):
        if self.game_over:
            return
        now = pygame.time.get_ticks()
        elapsed = max(0, now - self._last_update)
        self._last_update = now
        self.time_left_ms = max(0, self.time_left_ms - elapsed)
        self.target.update()
        if self.target.expired() and self.time_left_ms > 0:
            self.misses += 1
            self.play_sound("miss")
            self.target = self._spawn_target()
        if self.time_left_ms <= 0:
            self.game_over = True
            self.play_sound("game_over")

    def accuracy(self):
        total = self.hits + self.misses
        return round(100 * self.hits / total, 1) if total else 0.0

    def render(self, screen):
        screen.fill(DARK)
        if not self.game_over:
            r = max(1, round(self.target.visual_radius()))
            pygame.draw.circle(screen, RED, (self.target.x, self.target.y), r)
            pygame.draw.circle(screen, WHITE, (self.target.x, self.target.y), r, 2)

        pygame.draw.rect(screen, PANEL, (0, 0, self.width, self.hud_height))
        score = self.font.render(f"Score: {self.score}", True, WHITE)
        timer = self.font.render(f"Time: {self.time_left_ms // 1000}s", True, WHITE)
        accuracy = self.font.render(f"Accuracy: {self.accuracy()}%", True, WHITE)
        diff = self.small_font.render(self.difficulty, True, GREEN)
        screen.blit(score, (14, 14))
        screen.blit(accuracy, (self.width // 2 - accuracy.get_width() // 2, 14))
        screen.blit(timer, (self.width - timer.get_width() - 14, 14))
        screen.blit(diff, (14, self.height - 28))

        if self.game_over:
            self._render_game_over(screen)

    def _render_game_over(self, screen):
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 190))
        screen.blit(overlay, (0, 0))
        title = self.large_font.render("GAME OVER", True, GREEN)
        summary = self.font.render(
            f"Final score: {self.score}    Accuracy: {self.accuracy()}%", True, WHITE)
        stats = self.small_font.render(
            f"Hits: {self.hits}   Misses: {self.misses}   Difficulty: {self.difficulty}", True, WHITE)
        prompt = self.font.render("Press R to replay  |  Press 1 Easy, 2 Medium, 3 Hard  |  ESC to exit", True, WHITE)
        for surface, y in ((title, 170), (summary, 235), (stats, 275), (prompt, 335)):
            screen.blit(surface, (self.width // 2 - surface.get_width() // 2, y))
