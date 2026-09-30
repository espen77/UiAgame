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

- `game/content.py` is the data source of truth for outfits, jobs, salaries, meal prices, education grades, housing, and normalized map locations. Education is grade-based: 1–7 Barneskole, 8–10 Ungdomskole, 11–13 Vidregående skole, 14–15 Fagskole, 16–18 Bachelor, 19–20 Master, 21–25 Doktorgrad.
- `game/state.py` owns the economy, needs, education grade, shifts, housing efficiency, and win condition; keep it independent of rendering so it stays unit-testable.
- `game/assets.py` loads the map, character PNGs, and `sounds/*.wav`; it removes baked checkerboard backgrounds from thumbnails and degrades safely when audio is unavailable.
- `game/world.py` scales the complete map into the left viewport; it owns movement, click-to-walk targets, markers, and player drawing. Do not reintroduce a scrolling camera.
- `game/ui.py` owns the right-side portrait/status/energy panel and modal menus; `main.py` wires keyboard, mouse navigation, audio, and state transitions together.
- Outfit `tier` values are a strict purchase order; every purchasable tier requires all previous tiers to be owned.
- Job/outfit pairings are intentional: `looser` is the IT-support outfit, `school` is issued by study, and `winner` is only the completion portrait.
- Housing is data-driven: `freeway_house`/Billig Hus is 35 % effective, `middle_house`/Middels Hus is 65 %, and `exclusive_house`/Exclusive House is 100 % and mandatory for the win condition.
- `LOCATIONS` includes the hostel between Skole and Universitetet i Agder and `pharmacy` (Apotekergården); preserve these requested names and positions.
- Keyboard movement and shortcut keys are intentionally disabled; `World.move_toward` is mouse-navigation-only.

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
