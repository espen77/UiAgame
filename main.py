from __future__ import annotations

import pygame

from game.assets import load_characters, load_map
from game.content import LOCATIONS
from game.state import GameState
from game.ui import GameUI, Modal, ModalAction
from game.world import World


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Karl i Grimstad")
        self.screen = pygame.display.set_mode((1280, 800), pygame.RESIZABLE)
        pygame.display.set_icon(load_map())
        self.clock = pygame.time.Clock()
        self.state = GameState()
        self.world = World(load_map())
        self.ui = GameUI(load_characters())
        self.running = True
        self.modal: Modal | None = None
        self.modal_context: str | None = None
        self.selected_action = 0
        self.toasts: list[tuple[str, int]] = []
        self.nearby_location: str | None = None

    def run(self) -> None:
        while self.running:
            dt = min(self.clock.tick(60) / 1000, 0.05)
            self.handle_events()
            self.update(dt)
            self.draw()
        pygame.quit()

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.VIDEORESIZE:
                width = max(960, event.w)
                height = max(680, event.h)
                self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.modal:
                action = self.ui.action_at(self.modal, event.pos, self.screen.get_size())
                if action:
                    self.activate(action)

    def handle_keydown(self, event: pygame.event.Event) -> None:
        if self.modal:
            if event.key == pygame.K_ESCAPE:
                self.close_modal()
            elif pygame.K_1 <= event.key <= pygame.K_9:
                index = event.key - pygame.K_1
                if index < len(self.modal.actions) and self.modal.actions[index].enabled:
                    self.selected_action = index
                    self.activate(self.modal.actions[index])
            elif event.key in (pygame.K_UP, pygame.K_w):
                self.move_selection(-1)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.move_selection(1)
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                self.activate_selected()
            return

        if event.key == pygame.K_e:
            self.open_nearby_location()
        elif event.key == pygame.K_c:
            self.open_modal("clothing")
        elif event.key == pygame.K_h:
            self.open_modal("housing")
        elif event.key == pygame.K_F1:
            self.modal = self.ui.build_help_modal()
            self.modal_context = "help"
            self.selected_action = 0

    def move_selection(self, delta: int) -> None:
        if not self.modal or not self.modal.actions:
            return
        count = len(self.modal.actions)
        for offset in range(1, count + 1):
            index = (self.selected_action + delta * offset) % count
            if self.modal.actions[index].enabled:
                self.selected_action = index
                return

    def activate_selected(self) -> None:
        if not self.modal or self.selected_action >= len(self.modal.actions):
            return
        action = self.modal.actions[self.selected_action]
        if action.enabled:
            self.activate(action)

    def open_nearby_location(self) -> None:
        location_id = self.world.nearest_location(self.state.position)
        if location_id:
            self.open_modal(f"location:{location_id}")
        else:
            self.toast("Gå nærmere universitetet, kirken, Auto45, havnen eller skolen.")

    def open_modal(self, context: str) -> None:
        self.modal_context = context
        self.refresh_modal()
        self.selected_action = self._first_enabled_action()

    def refresh_modal(self) -> None:
        if not self.modal_context:
            self.modal = None
            return
        if self.modal_context == "clothing":
            self.modal = self.ui.build_clothing_modal(self.state)
        elif self.modal_context == "housing":
            self.modal = self.ui.build_housing_modal(self.state)
        elif self.modal_context == "help":
            self.modal = self.ui.build_help_modal()
        elif self.modal_context == "win":
            self.modal = self.ui.build_win_modal()
        elif self.modal_context.startswith("location:"):
            location_id = self.modal_context.split(":", 1)[1]
            if location_id in LOCATIONS:
                self.modal = self.ui.build_location_modal(self.state, location_id)
            else:
                self.close_modal()

    def close_modal(self) -> None:
        self.modal = None
        self.modal_context = None
        self.selected_action = 0

    def activate(self, action: ModalAction) -> None:
        if action.id == "close":
            self.close_modal()
            return
        if action.id.startswith("job:"):
            started, message = self.state.start_shift(action.id.split(":", 1)[1])
            self.toast(message)
            if started:
                self.close_modal()
            return
        if action.id.startswith("outfit:"):
            _, message = self.state.buy_outfit(action.id.split(":", 1)[1])
            self.toast(message)
        elif action.id == "buy_food":
            _, message = self.state.buy_food()
            self.toast(message)
        elif action.id == "study_school":
            _, message = self.state.study(university=False)
            self.toast(message)
        elif action.id == "study_university":
            _, message = self.state.study(university=True)
            self.toast(message)
        elif action.id == "soup":
            _, message = self.state.take_soup()
            self.toast(message)
        elif action.id == "buy_apartment":
            _, message = self.state.buy_apartment()
            self.toast(message)
        elif action.id in {"sleep_hostel", "sleep_home"}:
            _, message = self.state.sleep()
            self.toast(message)
        self.refresh_modal()
        self.selected_action = self._first_enabled_action()

    def _first_enabled_action(self) -> int:
        if not self.modal:
            return 0
        for index, action in enumerate(self.modal.actions):
            if action.enabled:
                return index
        return 0

    def update(self, dt: float) -> None:
        now = pygame.time.get_ticks()
        self.toasts = [(message, expires) for message, expires in self.toasts if expires > now]
        if self.modal:
            return

        if self.state.shift:
            message = self.state.update_shift(dt)
            if message:
                self.toast(message)
        else:
            moving = self.world.move_player(self.state, dt)
            message = self.state.advance_time(dt, moving)
            if message:
                self.toast(message)

        if self.state.update_goal():
            self.modal = self.ui.build_win_modal()
            self.modal_context = "win"
            self.selected_action = 0

    def draw(self) -> None:
        self.nearby_location = self.world.draw(self.screen, self.state, pygame.time.get_ticks())
        self.ui.draw_hud(self.screen, self.state)
        self.ui.draw_shift(self.screen, self.state)

        if not self.modal and not self.state.shift and self.nearby_location:
            location_name = LOCATIONS[self.nearby_location].name
            self.ui.draw_interaction_prompt(self.screen, f"[E] Gå inn på {location_name}")

        if self.modal:
            if self.modal.context == "win":
                self.ui.show_character(self.screen, "winner")
            self.ui.draw_modal(self.screen, self.modal, self.selected_action)

        now = pygame.time.get_ticks()
        for message, expires in self.toasts[-3:]:
            self.ui.draw_toast(self.screen, message, expires - now)
        pygame.display.flip()

    def toast(self, message: str) -> None:
        self.toasts.append((message, pygame.time.get_ticks() + 3600))
        self.toasts = self.toasts[-3:]


def main() -> None:
    Game().run()


if __name__ == "__main__":
    main()
