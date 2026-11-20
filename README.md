# Lab 4 — Target Aim Trainer

Completed tasks based on the repository specification.

## Implemented changes

1. **Accurate collision detection:** `Target.contains_point()` uses `visual_radius()`, so only the visible shrinking circle is clickable.
2. **Game Over screen:** the round ends at zero seconds and displays final score, accuracy, hits, misses, and difficulty in the game window.
3. **Replay and difficulty:** press `R` to replay at the current difficulty; choose `1` Easy, `2` Medium, or `3` Hard. Press `ESC` to exit from the Game Over screen.
4. **Sound feedback:** the engine looks for `hit.wav`, `miss.wav`, and `game_over.wav` in `assets/sounds/`. Missing sound files or unavailable audio hardware do not prevent the game from running.

## Difficulty settings

| Difficulty | Target lifespan | Starting radius |
|---|---:|---:|
| Easy | 120 frames | 45 px |
| Medium | 90 frames | 40 px |
| Hard | 60 frames | 35 px |

## Setup and run

```bash
python -m venv .venv
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Sound assets

Place three short WAV files at:

- `assets/sounds/hit.wav`
- `assets/sounds/miss.wav`
- `assets/sounds/game_over.wav`

The program supports missing sounds gracefully. Use original or appropriately licensed audio.

## Validation

Run unit tests from the project root:

```bash
python -m unittest discover -s tests -v
```

## Required submission evidence

The README in the starter repository requires (a) a 10-second before-change gameplay video showing the original collision bug, (b) a 10-second after-change gameplay video demonstrating the fixes/features, and (c) a shareable link to the complete LLM conversation. These must be captured from the student's own machine/account; no videos or chat link are fabricated here. Save them under `evidence/` and fill `evidence/CHAT_LINK.txt` before submitting.
