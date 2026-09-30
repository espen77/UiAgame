# AGENTS.md

## Current state

- `main.py` is a Pygame 2.6 game entry point; this is not a Unity/Godot project.
- `images/` holds general game art. `images/character/` holds character art. Use a `.gitkeep` file when a new asset directory must be committed while empty.
- Preserve existing asset filenames unless the user asks for a rename. In particular, keep `images/character/looser.png`; do not silently "correct" it to `loser.png`.

## Development

- Install dependencies with `py -m pip install -r requirements.txt`.
- Run the game with `py main.py`.
- Run the focused state tests with `py -m unittest discover -s tests -v`.
- There is no configured linter, formatter, type checker, or code generator. Keep changes compatible with Python 3.10+ and Pygame 2.6.

## Architecture

- `game/content.py` is the data source of truth for outfits, jobs, prices, education levels, housing, and normalized map locations. Keep the required geography when editing `LOCATIONS`.
- `game/state.py` owns the economy, needs, education, shifts, housing, and win condition; keep it independent of rendering so it stays unit-testable.
- `game/assets.py` loads the map and character PNGs and removes baked checkerboard backgrounds from thumbnails at load time.
- `game/world.py` scales the complete map to fit the viewport with letterboxing; it owns movement, map markers, and player drawing. Do not reintroduce a scrolling camera.
- `game/ui.py` owns the HUD and modal menus; `main.py` wires input and state transitions together.
- Job/outfit pairings are intentional: `looser` is the IT-support outfit, `school` is issued by study, and `winner` is only the completion portrait.
- Housing is data-driven: `freeway_house` is cheap with lower recovery, while `sea_house` is expensive with full recovery and higher rent.

## Grimstad map

- `images/grimstad_map.txt` is the authoritative Norwegian generation prompt for `images/grimstad_map.png`; keep it with the map.
- Regenerated maps must match real Grimstad: church in the east, harbor in the south, and include apotekergården, the gas station, the pizza bakery, the hotel, the university, and the motorway north of town. *Johnes in the Fast Lane* may guide visual style only, not geography.
- If the map specification changes, update `images/grimstad_map.txt` in the same change.

## OpenCode GitHub agent

- `.github/workflows/opencode.yml` only runs for issue or PR-review comments containing `/oc` or `/opencode`.
- The action is `anomalyco/opencode/github@latest` with model `minimax/MiniMax-M3`. It requires the repository Actions secret `MINIMAX_API_KEY`; never put the key in a file or commit.
- Do not change the action, provider, model, or secret name without explicit approval; those changes alter external code and billing.
- Agent runs can push branches and open pull requests. Treat `/oc` comments as write-capable automation, not read-only chat.
- Successful runs may show `actions/cache` Node 20 deprecation and `cache write denied` warnings. These warnings are currently non-blocking; investigate only when the run itself fails.
