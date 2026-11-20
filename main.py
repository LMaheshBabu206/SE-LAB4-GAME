"""Target Aim Trainer - run with: python main.py"""
import pygame
from game.game_engine import GameEngine

WIDTH, HEIGHT = 700, 500
FPS = 60


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Target Aim Trainer")
    clock = pygame.time.Clock()
    engine = GameEngine(WIDTH, HEIGHT)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and engine.game_over:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key in (pygame.K_r, pygame.K_1, pygame.K_2, pygame.K_3):
                    difficulty = {
                        pygame.K_1: "Easy",
                        pygame.K_2: "Medium",
                        pygame.K_3: "Hard",
                    }.get(event.key, engine.difficulty)
                    engine.start_round(difficulty)
            else:
                engine.handle_event(event)

        engine.handle_input()
        engine.update()
        engine.render(screen)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
