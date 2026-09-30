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

The game opens in a resizable window. The map is centered on Karl; use WASD or the arrow keys to move.

## Controls

| Key | Action |
| --- | --- |
| `WASD` / arrows | Move around Grimstad |
| `E` | Enter a nearby location |
| `C` | Open the clothing shop |
| `H` | Open housing and rest |
| `1`–`9` / arrows / Enter | Choose menu actions |
| `Esc` | Close a menu |
| `F1` | Show help |

## Game loop

1. Start at Vidregående skole and take study weeks to unlock better jobs.
2. Visit the harbor or Auto45 with the right outfit to work a shift.
3. Use the clothing shop to buy outfits that qualify for higher-paying jobs.
4. Buy food at Auto45 and use the housing menu to rest.
5. Save for an apartment and reach the final goal: university education, a consultant shift, an apartment, and 8,000 kr saved.

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

The main entry point is `main.py`. Game rules and economy live in `game/content.py` and `game/state.py`; map movement is in `game/world.py`; HUD and menus are in `game/ui.py`.
