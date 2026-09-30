from __future__ import annotations

import math

import pygame

from .content import LOCATIONS, OUTFITS
from .state import GameState


class World:
    def __init__(self, map_surface: pygame.Surface) -> None:
        self.map = map_surface
        self.size = map_surface.get_size()
        self.scaled_map = map_surface
        self.scaled_size = self.size
        self.map_rect = pygame.Rect((0, 0), self.size)
        self.player_speed = 250.0
        self.interaction_radius = 82.0

    def location_position(self, location_id: str) -> pygame.Vector2:
        location = LOCATIONS[location_id]
        return pygame.Vector2(location.x * self.size[0], location.y * self.size[1])

    def map_to_screen(self, position: pygame.Vector2) -> pygame.Vector2:
        map_width, map_height = self.size
        rect = self.map_rect
        return pygame.Vector2(
            rect.x + position.x / map_width * rect.width,
            rect.y + position.y / map_height * rect.height,
        )

    def nearest_location(self, position: pygame.Vector2) -> str | None:
        nearest_id = None
        nearest_distance = self.interaction_radius
        for location_id in LOCATIONS:
            distance = position.distance_to(self.location_position(location_id))
            if distance <= nearest_distance:
                nearest_id = location_id
                nearest_distance = distance
        return nearest_id

    def move_player(self, state: GameState, dt: float) -> bool:
        keys = pygame.key.get_pressed()
        direction = pygame.Vector2(
            int(keys[pygame.K_d] or keys[pygame.K_RIGHT])
            - int(keys[pygame.K_a] or keys[pygame.K_LEFT]),
            int(keys[pygame.K_s] or keys[pygame.K_DOWN])
            - int(keys[pygame.K_w] or keys[pygame.K_UP]),
        )
        if direction.length_squared() == 0:
            return False
        direction = direction.normalize()
        state.position += direction * self.player_speed * dt
        state.position.x = max(24.0, min(self.size[0] - 24.0, state.position.x))
        state.position.y = max(24.0, min(self.size[1] - 24.0, state.position.y))
        state.facing = direction
        return True

    def _fit_map_to_viewport(self, viewport: pygame.Rect) -> None:
        map_width, map_height = self.size
        scale = min(viewport.width / map_width, viewport.height / map_height)
        target_size = (
            max(1, round(map_width * scale)),
            max(1, round(map_height * scale)),
        )
        if target_size != self.scaled_size:
            self.scaled_map = pygame.transform.smoothscale(self.map, target_size)
            self.scaled_size = target_size
        self.map_rect = pygame.Rect((0, 0), target_size)
        self.map_rect.center = viewport.center

    def location_at_screen(self, position: tuple[int, int]) -> str | None:
        point = pygame.Vector2(position)
        for location_id in LOCATIONS:
            marker_position = self.map_to_screen(self.location_position(location_id))
            if point.distance_to(marker_position) <= 42:
                return location_id
        return None

    def move_toward(self, state: GameState, destination: str, dt: float) -> tuple[bool, bool]:
        target = self.location_position(destination)
        to_target = target - state.position
        distance = to_target.length()
        if distance <= self.interaction_radius * 0.55:
            return False, True
        direction = to_target.normalize()
        state.position += direction * min(distance, self.player_speed * dt)
        state.facing = direction
        return True, False

    def draw(
        self,
        surface: pygame.Surface,
        state: GameState,
        now_ms: int,
        viewport: pygame.Rect | None = None,
    ) -> str | None:
        viewport = viewport or surface.get_rect()
        self._fit_map_to_viewport(viewport)
        surface.fill((20, 34, 43))
        surface.blit(self.scaled_map, self.map_rect)
        pygame.draw.rect(surface, (10, 22, 30), self.map_rect, 3)

        marker_font = pygame.font.Font(None, 24)
        label_font = pygame.font.Font(None, 22)
        pulse = 1.0 + 0.08 * math.sin(now_ms / 260)
        nearby = self.nearest_location(state.position)
        visible_rect = self.map_rect.inflate(160, 160)

        for location in LOCATIONS.values():
            position = self.map_to_screen(self.location_position(location.id))
            if not visible_rect.collidepoint((round(position.x), round(position.y))):
                continue
            selected = location.id == nearby
            radius = int((25 if selected else 20) * pulse)
            pygame.draw.circle(surface, (12, 18, 24), position, radius + 5)
            pygame.draw.circle(surface, location.color, position, radius)
            pygame.draw.circle(surface, (245, 247, 250), position, radius, 3)

            letter = location.short_name[0]
            text = marker_font.render(letter, True, (255, 255, 255))
            surface.blit(text, text.get_rect(center=position))

            label = label_font.render(location.short_name, True, (20, 24, 30))
            label_rect = label.get_rect(center=(int(position.x), int(position.y + radius + 17)))
            background = label_rect.inflate(14, 8)
            pygame.draw.rect(surface, (250, 250, 250), background, border_radius=6)
            surface.blit(label, label_rect)

        if state.destination in LOCATIONS:
            start = self.map_to_screen(state.position)
            end = self.map_to_screen(self.location_position(state.destination))
            pygame.draw.line(surface, (255, 214, 84), start, end, 3)
            pygame.draw.circle(surface, (255, 214, 84), end, 28, 4)

        self._draw_player(surface, state)
        return nearby

    def _draw_player(self, surface: pygame.Surface, state: GameState) -> None:
        position = self.map_to_screen(state.position)
        outfit = OUTFITS[state.current_outfit]
        bob = math.sin(pygame.time.get_ticks() / 90) * 1.5

        pygame.draw.ellipse(
            surface,
            (12, 18, 22),
            (position.x - 18, position.y + 12, 36, 13),
        )
        body = pygame.Rect(0, 0, 30, 38)
        body.center = (round(position.x), round(position.y - 4 + bob))
        pygame.draw.rect(surface, outfit.color, body, border_radius=9)
        pygame.draw.rect(surface, (245, 247, 250), body, 3, border_radius=9)

        head = pygame.Rect(0, 0, 25, 25)
        head.center = (round(position.x), round(position.y - 30 + bob))
        pygame.draw.circle(surface, (238, 184, 146), head.center, 13)
        pygame.draw.circle(surface, (38, 30, 28), head.center, 13, 2)
        pygame.draw.arc(surface, (38, 30, 28), head, 0.15, math.pi - 0.15, 3)

        direction = state.facing
        if direction.length_squared() > 0:
            direction = direction.normalize()
            tip = pygame.Vector2(head.center) + direction * 18
            side = pygame.Vector2(-direction.y, direction.x) * 5
            pygame.draw.polygon(
                surface,
                (255, 214, 84),
                [
                    tip,
                    pygame.Vector2(head.center) + direction * 9 + side,
                    pygame.Vector2(head.center) + direction * 9 - side,
                ],
            )
