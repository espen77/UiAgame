from __future__ import annotations

from pathlib import Path

import pygame

from .content import OUTFITS


ROOT = Path(__file__).resolve().parent.parent
MAP_PATH = ROOT / "images" / "grimstad_map.png"
CHARACTER_DIR = ROOT / "images" / "character"


def load_map() -> pygame.Surface:
    if not MAP_PATH.exists():
        raise FileNotFoundError(f"Mappen mangler: {MAP_PATH}")
    return pygame.image.load(MAP_PATH.as_posix()).convert()


def _is_checkerboard_background(red: int, green: int, blue: int) -> bool:
    return min(red, green, blue) >= 175 and max(red, green, blue) - min(red, green, blue) <= 24


def _remove_checkerboard(surface: pygame.Surface) -> pygame.Surface:
    width, height = surface.get_size()
    pixels = [[surface.get_at((x, y)) for x in range(width)] for y in range(height)]
    visited = bytearray(width * height)
    stack: list[tuple[int, int]] = []

    for x in range(width):
        stack.append((x, 0))
        stack.append((x, height - 1))
    for y in range(height):
        stack.append((0, y))
        stack.append((width - 1, y))

    while stack:
        x, y = stack.pop()
        index = y * width + x
        if visited[index]:
            continue
        visited[index] = 1
        pixel = pixels[y][x]
        if not _is_checkerboard_background(pixel.r, pixel.g, pixel.b):
            continue
        surface.set_at((x, y), (pixel.r, pixel.g, pixel.b, 0))
        if x > 0:
            stack.append((x - 1, y))
        if x + 1 < width:
            stack.append((x + 1, y))
        if y > 0:
            stack.append((x, y - 1))
        if y + 1 < height:
            stack.append((x, y + 1))
    return surface


def load_character(filename: str, size: tuple[int, int] = (108, 162)) -> pygame.Surface:
    path = CHARACTER_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Karakterbilde mangler: {path}")
    original = pygame.image.load(path.as_posix())
    scaled = pygame.transform.smoothscale(original, size).convert_alpha()
    if not original.get_flags() & pygame.SRCALPHA:
        scaled = _remove_checkerboard(scaled)
    return scaled


def load_characters() -> dict[str, pygame.Surface]:
    return {outfit_id: load_character(outfit.image) for outfit_id, outfit in OUTFITS.items()}
