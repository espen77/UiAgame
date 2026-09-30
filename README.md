# Karl i Grimstad

A small Pygame life-simulation game inspired by *Johannes in the Fast Lane*. Karl starts with shorts, a little money, and a map of Grimstad. He must work, study, buy better clothes, and save for an apartment.

The game uses the map in `images/grimstad_map.png` and the character outfits in `images/character/`.

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

The game opens in a resizable window. The complete Grimstad map always scales to fit the window, so it never scrolls away from view. Use WASD or the arrow keys to move.

## Controls

| Key | Action |
| --- | --- |
| `WASD` / arrows | Move around Grimstad |
| `E` | Enter a nearby location |
| `C` | Open the clothing shop |
| `H` | Open housing and rest |
| `E` | Enter the bar, clothing shop, houses, and other marked locations |
| `1`–`9` / arrows / Enter | Choose menu actions |
| `Esc` | Close a menu |
| `F1` | Show help |

## Game loop

1. Start at Vidregående skole and take study weeks to unlock better jobs.
2. Visit the harbor or Auto45 with the right outfit to work a shift.
3. Visit the clothing shop between Vidregående and the harbor to buy outfits that qualify for higher-paying jobs.
4. Buy food at Auto45 or a cheap meal at the bar, then use the housing menu to rest.
5. Choose housing: the house by the freeway is cheap, while the house by the sea is expensive but restores more energy.
6. Reach the final goal: university education, a consultant shift, a home, and 8,000 kr saved.

## Locations and housing

- The university is in the west, the church in the east, Auto45 by the northern freeway, the harbor in the south, and Vidregående in the center.
- The bar and clothing shop sit between Vidregående and the harbor.
- `Motorveishuset` costs 3,500 kr, has 90 kr daily rent, and restores 88 energy when resting.
- `Huset ved havet` costs 12,000 kr, has 260 kr daily rent, and restores full energy when resting.

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

## Development

Run the unit tests with:

```powershell
py -m unittest discover -s tests -v
```

The main entry point is `main.py`. Game rules, jobs, housing, prices, and normalized map locations live in `game/content.py` and `game/state.py`; the map-fit scaling and movement are in `game/world.py`; HUD and menus are in `game/ui.py`.
