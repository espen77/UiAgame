# Karl i Grimstad

A small Pygame life-simulation game inspired by *Johannes in the Fast Lane*. Karl starts with shorts, a little money, and a map of Grimstad. He must work, study, buy better clothes, and save for the Exclusive House.

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
| `WASD` / arrows | Move around Grimstad |
| Left click | Walk to a marked place and enter automatically |
| `E` | Enter a nearby building, shop, hostel, or house |
| `C` | Open the clothing shop |
| `H` | Open housing and rest |
| `1`–`9` / arrows / Enter | Choose menu actions |
| `Esc` | Close a menu |
| `F1` | Show help |

## Game loop

1. Start at Vidregående skole and take study weeks to unlock better jobs.
2. Visit the harbor or Auto45 with the right outfit to work a shift.
3. Visit the clothing shop between Vidregående and the harbor. Clothing levels must be owned in order before the next level can be bought.
4. Buy food at Auto45 or a cheap meal at Apotekergården, then rest at the hostel or a home.
5. Choose housing: the house by the freeway is cheap, while Exclusive House costs more but restores full energy.
6. Reach the final goal: university education, a consultant shift, Exclusive House ownership, and 8,000 kr saved.

## Locations and housing

- The university is in the west, the church in the east, Auto45 by the northern freeway, the harbor in the south, and Vidregående in the center.
- Apotekergården and the clothing shop sit between Vidregående and the harbor. The hostel sits between Vidregående and the university.
- `Motorveishuset` costs 3,500 kr, has 90 kr daily rent, and restores 88 energy when resting.
- `Exclusive House` is south of the church in the bottom-right part of the map. It costs 12,000 kr, has 260 kr daily rent, restores full energy, and is required to win.

## Jobs

| Job | Outfit | Location | Education | Pay per shift |
| --- | --- | --- | --- | ---: |
| Havneassistent | Shorts | Harbor | Grunnskole | 120 kr |
| Butikkassistent | Casual | Auto45 | Grunnskole | 160 kr |
| Lagerarbeider | Hoodie | Harbor | Fagskole | 240 kr |
| Bilmekaniker | Arbeidskledel | Auto45 | Videregående | 340 kr |
| IT-support | Gamer-hoodie | Universitetet | Videregående | 400 kr |
| Menighetsarbeider | Dress | Kirken | Videregående | 360 kr |
| Universitetskonsulent | Dress | Universitetet | Universitet | 600 kr |

## Sounds

The `sounds/` directory contains effects for walking, sleeping, working, opening doors, and eating or drinking. The bundled WAV files are synthesized placeholders and can be replaced without changing code.

## Development

Run the unit tests with:

```powershell
py -m unittest discover -s tests -v
```

The main entry point is `main.py`. Game rules, jobs, housing, prices, and normalized map locations live in `game/content.py` and `game/state.py`; the map-fit scaling and movement are in `game/world.py`; HUD and menus are in `game/ui.py`.
