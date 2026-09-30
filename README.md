# Karl i Grimstad

A small Pygame life-simulation game inspired by *Johannes in the Fast Lane*. Karl starts with shorts, a little money, and a map of Grimstad. He must work, study, buy better clothes, and save for Dyrt Hus.

The game uses the map in `images/grimstad_map.png`, the character outfits in `images/character/`, and the effects in `sounds/`.

## Requirements

- Python 3.10+
- Pygame 2.6+

Install the dependency:

```powershell
py -m pip install -r requirements.txt
```

## Run

```powershell
py main.py
```

The game opens in a resizable window. The complete Grimstad map always scales into the left side, while Karl's portrait, needs, energy bar, and next-goal text stay in the right-side panel.

## Controls

| Key | Action |
| --- | --- |
| Left click | Walk to a marked place and enter automatically |
| `1`–`9` / Enter | Choose menu actions |
| `Esc` | Close a menu |
| `F1` | Show help |

Keyboard movement and shortcut keys are intentionally disabled; the game is played by clicking the map and menus.

## Game loop

1. Start at Skole and study from Barneskole through Fagskole to unlock better jobs.
2. Visit the harbor or CircleK with the right outfit to work a shift.
3. Visit the clothing shop between Skole and the harbor. Clothing levels must be owned in order before the next level can be bought.
4. Buy food at CircleK or a meal at Apotekergården, then rest at the hostel, a home, or in the church.
5. Choose housing: Billig Hus is 35 % effective, Middels Hus is 65 % effective, and Dyrt Hus is 100 % effective.
6. Reach the final goal: Doktorgrad, a consultant shift, Dyrt Hus ownership, and 8,000 kr saved.

## Locations and housing

- Universitetet i Agder is in the west, the church in the east, CircleK by the northern freeway, the harbor in the south, and Skole in the center.
- Apotekergården and the clothing shop sit between Skole and the harbor. The hostel sits between Skole and Universitetet i Agder.
- `Billig Hus` costs 3,500 kr, has 90 kr daily rent, and provides 35 % effective rest.
- `Middels Hus` costs 7,000 kr, has 170 kr daily rent, and provides 65 % effective rest.
- `Dyrt Hus` is south of the church in the bottom-right part of the map. It costs 12,000 kr, has 260 kr daily rent, provides 100 % effective rest, and is required to win.

## Education grades

`1–7 Barneskole` · `8–10 Ungdomskole` · `11–13 Vidregående skole` · `14–15 Fagskole` · `16–18 Bachelor` · `19–20 Master` · `21–25 Doktorgrad`

Skole in the middle handles grades 1–15. Universitetet i Agder handles grades 16–25.

## Jobs

| Job | Outfit | Location | Education | Pay per shift |
| --- | --- | --- | --- | ---: |
| Havneassistent | Shorts | Harbor | Barneskole 1 | 120 kr |
| Butikkassistent | Casual | CircleK | Barneskole 1 | 170 kr |
| Klesbutikkansatt | Casual | Klesbutikken | Barneskole 1 | 210 kr |
| Lagerarbeider | Hoodie | Harbor | Ungdomskole 8 | 280 kr |
| Bilmekaniker | Arbeidskledel | CircleK | Fagskole 14 | 430 kr |
| IT-support | Gamer-hoodie | Universitetet i Agder | Bachelor 16 | 560 kr |
| Menighetsarbeider | Dress | Kirken | Bachelor 16 | 480 kr |
| Universitetskonsulent | Dress | Universitetet i Agder | Master 19 | 850 kr |

## Progression

Working and studying award XP. The HUD shows XP toward the next career level at the bottom of the right panel.

## Sounds

The `sounds/` directory contains effects for walking, sleeping, working, studying, opening doors, and eating or drinking. The bundled WAV files are synthesized placeholders and can be replaced without changing code.

## Development

Run the unit tests with:

```powershell
py -m unittest discover -s tests -v
```

The main entry point is `main.py`. Game rules, jobs, housing, prices, and normalized map locations live in `game/content.py` and `game/state.py`; the map-fit scaling and movement are in `game/world.py`; HUD and menus are in `game/ui.py`.
