# AGENTS.md

## Current state

- This is an asset-only repository. There is no game engine, application code, dependency manifest, build, test, lint, or codegen configuration yet. Do not assume Unity, Godot, or another engine; verify before adding tooling.
- `images/` holds general game art. `images/character/` holds character art. Use a `.gitkeep` file when a new asset directory must be committed while empty.
- Preserve existing asset filenames unless the user asks for a rename. In particular, keep `images/character/looser.png`; do not silently "correct" it to `loser.png`.

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
