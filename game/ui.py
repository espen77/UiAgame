from __future__ import annotations

from dataclasses import dataclass

import pygame

from .content import (
    BAR_FOOD_PRICE,
    FOOD_PRICE,
    GOAL_SAVINGS,
    HOUSING,
    HOSTEL_PRICE,
    JOBS,
    LOCATIONS,
    OUTFITS,
    SHOP_OUTFITS,
    housing_at,
    jobs_at,
    jobs_for_outfit,
)
from .state import GameState


@dataclass(frozen=True)
class ModalAction:
    id: str
    label: str
    enabled: bool = True
    hint: str = ""


@dataclass
class Modal:
    context: str
    title: str
    subtitle: str
    lines: list[str]
    actions: list[ModalAction]


@dataclass(frozen=True)
class ButtonRect:
    rect: pygame.Rect
    action: ModalAction
    index: int


class GameUI:
    def __init__(self, characters: dict[str, pygame.Surface]) -> None:
        pygame.font.init()
        self.characters = characters
        family = "segoeui,arial,helvetica"
        self.title_font = pygame.font.SysFont(family, 42, bold=True)
        self.heading_font = pygame.font.SysFont(family, 26, bold=True)
        self.body_font = pygame.font.SysFont(family, 19)
        self.body_bold = pygame.font.SysFont(family, 19, bold=True)
        self.small_font = pygame.font.SysFont(family, 16)
        self.tiny_font = pygame.font.SysFont(family, 14)
        self.money_font = pygame.font.SysFont(family, 24, bold=True)

    def build_location_modal(self, state: GameState, location_id: str) -> Modal:
        location = LOCATIONS[location_id]
        actions: list[ModalAction] = []
        for job in jobs_at(location_id):
            blocker = state.work_blocker(job.id)
            actions.append(
                ModalAction(
                    id=f"job:{job.id}",
                    label=f"Jobb: {job.name} (+{job.wage} kr)",
                    enabled=blocker is None,
                    hint=blocker or job.description,
                )
            )

        if location_id == "gas_station":
            actions.append(
                ModalAction(
                    id="buy_food",
                    label=f"Kjøp mat (+40 mat, -{FOOD_PRICE} kr)",
                    enabled=state.money >= FOOD_PRICE,
                    hint="Mat holder Karl i gang mens han jobber.",
                )
            )
        elif location_id == "bar":
            actions.append(
                ModalAction(
                    id="buy_bar_food",
                    label=f"Kjøp måltid (+30 mat, +10 energi, -{BAR_FOOD_PRICE} kr)",
                    enabled=state.money >= BAR_FOOD_PRICE,
                    hint="Billig mat og litt ekstra energi til kvelden.",
                )
            )
        elif location_id == "clothing_shop":
            actions.append(
                ModalAction(
                    id="open_clothing",
                    label="Åpne klesbutikken",
                    hint="Kjøp klær som åpner nye jobber.",
                )
            )
        elif location_id == "school":
            actions.append(
                ModalAction(
                    id="study_school",
                    label="Studieuke ved Vidregående (-150 kr)",
                    enabled=state.money >= 150 and state.education_progress < 6,
                    hint=(
                        "Utdanningsnivået øker etter hver tredje studieuke."
                        if state.money >= 150 and state.education_progress < 6
                        else "Videregående er fullført. Universitetet ligger i vest."
                        if state.education_progress >= 6
                        else "Karl trenger 150 kr til studiene."
                    ),
                )
            )
        elif location_id == "university":
            university_blocked = state.education_level < 2
            actions.append(
                ModalAction(
                    id="study_university",
                    label="Studieuke ved universitetet (-350 kr)",
                    enabled=not university_blocked and state.education_progress < 9 and state.money >= 350,
                    hint=(
                        "Krever ferdig videregående."
                        if university_blocked
                        else "Fullfører universitetsutdanningen."
                        if state.money >= 350
                        else "Karl trenger 350 kr til studiene."
                    ),
                )
            )
        elif location_id == "church":
            soup_available = state.last_soup_day != state.day
            actions.append(
                ModalAction(
                    id="soup",
                    label="Hent varm suppe (gratis)",
                    enabled=soup_available,
                    hint="Menigheten hjelper Karl én gang per dag." if soup_available else "Suppen er allerede hentet i dag.",
                )
            )

        home = housing_at(location_id)
        if home:
            is_current = state.home_id == home.id
            current_price = HOUSING[state.home_id].price if state.home_id else 0
            cost = max(0, home.price - current_price)
            actions.append(
                ModalAction(
                    id=f"buy_home:{home.id}",
                    label=(
                        f"Bor her: {home.name}"
                        if is_current
                        else f"Kjøp {home.name} (-{cost} kr)"
                    ),
                    enabled=not is_current and state.money >= cost,
                    hint=(
                        f"Leie: {home.rent} kr per dag. {home.description}"
                        if not is_current
                        else f"Du bor allerede her. Leie: {home.rent} kr per dag."
                    ),
                )
            )

        actions.append(ModalAction(id="close", label="Lukk (Esc)"))
        return Modal(
            context=f"location:{location_id}",
            title=location.name,
            subtitle=location.description,
            lines=[
                f"Utdanning: {state.education_label}",
                f"Penger: {state.money} kr",
                f"Nåværende klær: {OUTFITS[state.current_outfit].name}",
            ],
            actions=actions,
        )

    def build_clothing_modal(self, state: GameState) -> Modal:
        actions: list[ModalAction] = []
        for outfit_id in SHOP_OUTFITS:
            outfit = OUTFITS[outfit_id]
            job_names = ", ".join(job.name for job in jobs_for_outfit(outfit_id))
            if outfit_id in state.owned_outfits:
                is_current = state.current_outfit == outfit_id
                actions.append(
                    ModalAction(
                        id=f"outfit:{outfit_id}",
                        label=f"Uliket: {outfit.name}" if is_current else f"Ta på {outfit.name}",
                        enabled=not is_current,
                        hint=outfit.description,
                    )
                )
            else:
                actions.append(
                    ModalAction(
                        id=f"outfit:{outfit_id}",
                        label=f"Kjøp {outfit.name} (-{outfit.price} kr)",
                        enabled=state.money >= outfit.price,
                        hint=f"{outfit.description} Jobber: {job_names}.",
                    )
                )
        actions.append(ModalAction(id="close", label="Lukk (Esc)"))
        return Modal(
            context="clothing",
            title="Klesbutikken",
            subtitle="Bedre klærer åpner bedre jobber. En jobb kler Karl automatisk.",
            lines=[f"Penger: {state.money} kr", f"Utdanning: {state.education_label}"],
            actions=actions,
        )

    def build_housing_modal(self, state: GameState) -> Modal:
        actions: list[ModalAction] = []
        for home in HOUSING.values():
            is_current = state.home_id == home.id
            current_price = HOUSING[state.home_id].price if state.home_id else 0
            cost = max(0, home.price - current_price)
            if is_current:
                label = f"Bor her: {home.name}"
                enabled = False
                hint = f"Du bor allerede her. Leie: {home.rent} kr per dag."
            else:
                label = f"{'Oppgrader til' if current_price else 'Kjøp'} {home.name} (-{cost} kr)"
                enabled = state.money >= cost and home.price > current_price
                hint = f"Leie: {home.rent} kr per dag. {home.description}"
            actions.append(ModalAction(id=f"buy_home:{home.id}", label=label, enabled=enabled, hint=hint))

        if state.apartment:
            actions.append(
                ModalAction(
                    id="sleep_home",
                    label="Hvil i egen bolig (gratis)",
                    hint=f"Full energi ({state.home_label}).",
                )
            )
        else:
            actions.append(
                ModalAction(
                    id="sleep_hostel",
                    label=f"Hvil på hospits (-{HOSTEL_PRICE} kr)",
                    enabled=state.money >= HOSTEL_PRICE,
                    hint="Billig, men gir mindre energi enn egen bolig.",
                )
            )
        actions.append(ModalAction(id="close", label="Lukk (Esc)"))
        return Modal(
            context="housing",
            title="Bolig i Grimstad",
            subtitle="Billig ved motorveien eller dyrt ved havet.",
            lines=[
                f"Penger: {state.money} kr",
                f"Nåværende bolig: {state.home_label}",
                f"Daglig kostnad: {state.daily_housing_cost} kr",
            ],
            actions=actions,
        )

    def build_help_modal(self) -> Modal:
        return Modal(
            context="help",
            title="Karl i Grimstad",
            subtitle="Jobb, studer, kjøp klær og spar til en egen bolig.",
            lines=[
                "WASD eller piltaster: gå",
                "E: gå inn på et sted",
                "C: klesbutikken",
                "H: bolig og hvile",
                "1-9: velg en handling i en meny",
                "Esc: lukk meny",
                "Mål: universitetsutdanning, egen bolig, konsulentjobb og minst 8000 kr.",
                "Hus: billig ved motorveien, dyrt og luksuriøst ved havet.",
            ],
            actions=[ModalAction(id="close", label="Spill (Esc)", hint="Lukk hjelpevinduet.")],
        )

    def build_win_modal(self) -> Modal:
        return Modal(
            context="win",
            title="Karl vant karrieren!",
            subtitle="Fra shortser på kaia til universitetskonsulent.",
            lines=[
                f"Full utdanning, egen bolig, konsulentjobb og {GOAL_SAVINGS} kr spare.",
                "Du kan fortsette spille og bygge opp sparepengene.",
            ],
            actions=[ModalAction(id="close", label="Feir! (Esc)", hint="Karl er både rik og kjent i Grimstad.")],
        )

    def layout_modal(self, modal: Modal, viewport: tuple[int, int]) -> tuple[pygame.Rect, list[ButtonRect]]:
        width = min(780, viewport[0] - 40)
        button_height = 62
        button_gap = 8
        wrapped_lines = sum(len(self.wrap_text(line, self.body_font, width - 68)) for line in modal.lines)
        content_height = 112 + wrapped_lines * 25 + len(modal.actions) * (button_height + button_gap) + 24
        height = min(viewport[1] - 36, max(320, content_height))
        rect = pygame.Rect(0, 0, width, height)
        rect.center = (viewport[0] // 2, viewport[1] // 2)

        y = rect.y + 112 + wrapped_lines * 25 + 4
        buttons: list[ButtonRect] = []
        for index, action in enumerate(modal.actions):
            button_rect = pygame.Rect(
                rect.x + 28,
                y + index * (button_height + button_gap),
                rect.width - 56,
                button_height,
            )
            buttons.append(ButtonRect(button_rect, action, index))
        return rect, buttons

    def action_at(self, modal: Modal, position: tuple[int, int], viewport: tuple[int, int]) -> ModalAction | None:
        _, buttons = self.layout_modal(modal, viewport)
        for button in buttons:
            if button.action.enabled and button.rect.collidepoint(position):
                return button.action
        return None

    def draw_hud(self, surface: pygame.Surface, state: GameState) -> None:
        self._draw_status_card(surface, state)
        self._draw_portrait(surface, state)
        self._draw_needs(surface, state)
        self._draw_objective(surface, state)
        self._draw_controls(surface)

    def draw_shift(self, surface: pygame.Surface, state: GameState) -> None:
        if state.shift is None:
            return
        job = JOBS[state.shift.job_id]
        width = min(520, surface.get_width() - 80)
        rect = pygame.Rect(0, 0, width, 96)
        rect.center = (surface.get_width() // 2, surface.get_height() // 2 + 150)
        self._panel(surface, rect)
        self._text(
            surface,
            f"Du jobber som {job.name}",
            self.heading_font,
            (rect.centerx, rect.y + 14),
            (255, 255, 255),
            center=True,
        )
        bar = pygame.Rect(rect.x + 28, rect.bottom - 24, rect.width - 56, 14)
        pygame.draw.rect(surface, (56, 66, 76), bar, border_radius=7)
        progress = 1 - state.shift.remaining / state.shift.total
        fill = bar.inflate(-4, -4)
        fill.width = max(0, int(fill.width * progress))
        if fill.width > 0:
            pygame.draw.rect(surface, (72, 196, 152), fill, border_radius=5)

    def draw_modal(self, surface: pygame.Surface, modal: Modal, selected: int | None = None) -> None:
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((5, 8, 12, 188))
        surface.blit(overlay, (0, 0))
        rect, buttons = self.layout_modal(modal, surface.get_size())
        self._panel(surface, rect, (250, 252, 255), (22, 30, 40))
        self._text(surface, modal.title, self.title_font, (rect.x + 32, rect.y + 18), (24, 32, 42))
        self._text(surface, modal.subtitle, self.body_font, (rect.x + 32, rect.y + 70), (76, 88, 100))

        y = rect.y + 112
        for line in modal.lines:
            for part in self.wrap_text(line, self.body_font, rect.width - 68):
                self._text(surface, part, self.body_font, (rect.x + 32, y), (40, 50, 60))
                y += 25

        for button in buttons:
            enabled = button.action.enabled
            background = (48, 128, 96) if enabled else (203, 208, 213)
            if selected == button.index and enabled:
                background = (34, 156, 112)
            pygame.draw.rect(surface, background, button.rect, border_radius=10)
            prefix = f"{button.index + 1}. " if enabled else ""
            label = self.body_bold.render(f"{prefix}{button.action.label}", True, (255, 255, 255) if enabled else (104, 112, 120))
            surface.blit(label, label.get_rect(midtop=(button.rect.centerx, button.rect.y + 7)))
            if button.action.hint:
                hint_color = (226, 240, 234) if enabled else (124, 132, 140)
                hint = self.wrap_text(button.action.hint, self.tiny_font, button.rect.width - 24)
                if hint:
                    hint_surface = self.tiny_font.render(hint[0], True, hint_color)
                    surface.blit(hint_surface, hint_surface.get_rect(midbottom=(button.rect.centerx, button.rect.bottom - 5)))

    def draw_toast(self, surface: pygame.Surface, message: str, remaining_ms: int) -> None:
        text = self.body_bold.render(message, True, (255, 255, 255))
        rect = text.get_rect(center=(surface.get_width() // 2, surface.get_height() - 118))
        panel = rect.inflate(36, 24)
        alpha = int(235 * min(1.0, max(0.0, remaining_ms / 600)))
        panel_surface = pygame.Surface(panel.size, pygame.SRCALPHA)
        panel_surface.fill((20, 28, 36, alpha))
        surface.blit(panel_surface, panel.topleft)
        surface.blit(text, rect)

    def draw_interaction_prompt(self, surface: pygame.Surface, message: str) -> None:
        rect = pygame.Rect(0, 0, 330, 46)
        rect.center = (surface.get_width() // 2, 112)
        self._panel(surface, rect)
        self._text(
            surface,
            message,
            self.body_bold,
            rect.center,
            (255, 255, 255),
            center=True,
            shadow=(10, 12, 16),
        )

    def show_character(self, surface: pygame.Surface, outfit_id: str, size: tuple[int, int] = (300, 450)) -> None:
        image = self.characters.get(outfit_id)
        if not image:
            return
        scaled = pygame.transform.smoothscale(image, size)
        rect = scaled.get_rect(center=(surface.get_width() // 2 + 190, surface.get_height() // 2 - 10))
        shadow = rect.inflate(20, 20)
        pygame.draw.rect(surface, (28, 36, 46), shadow, border_radius=16)
        surface.blit(scaled, rect)

    def _draw_status_card(self, surface: pygame.Surface, state: GameState) -> None:
        rect = pygame.Rect(18, 18, 320, 168)
        self._panel(surface, rect)
        self._text(surface, "KARL I GRIMSTAD", self.heading_font, (rect.x + 18, rect.y + 12), (245, 247, 250))
        self._text(surface, f"{state.money} kr", self.money_font, (rect.x + 18, rect.y + 45), (255, 214, 84))
        job = self._current_job(state)
        job_text = job.name if job else "Søk om jobb"
        self._text(surface, f"Jobb: {job_text}", self.body_font, (rect.x + 18, rect.y + 80), (225, 232, 238))
        self._text(
            surface,
            f"Utdanning: {state.education_label}   Dag: {state.day}",
            self.body_font,
            (rect.x + 18, rect.y + 107),
            (225, 232, 238),
        )
        self._text(
            surface,
            f"Bolig: {state.home_label}",
            self.body_font,
            (rect.x + 18, rect.y + 134),
            (225, 232, 238),
        )

    def _draw_portrait(self, surface: pygame.Surface, state: GameState) -> None:
        rect = pygame.Rect(surface.get_width() - 146, 18, 128, 178)
        self._panel(surface, rect)
        portrait = self.characters.get(state.current_outfit)
        if portrait:
            surface.blit(portrait, portrait.get_rect(midtop=(rect.centerx, rect.y + 8)))
        self._text(
            surface,
            OUTFITS[state.current_outfit].name,
            self.small_font,
            (rect.centerx, rect.bottom - 26),
            (255, 255, 255),
            center=True,
        )

    def _draw_needs(self, surface: pygame.Surface, state: GameState) -> None:
        rect = pygame.Rect(18, surface.get_height() - 98, 300, 80)
        self._panel(surface, rect)
        self._bar(surface, pygame.Rect(rect.x + 16, rect.y + 20, rect.width - 32, 14), state.hunger, (236, 96, 84), "Mat")
        self._bar(surface, pygame.Rect(rect.x + 16, rect.y + 51, rect.width - 32, 14), state.energy, (72, 176, 230), "Energi")

    def _draw_objective(self, surface: pygame.Surface, state: GameState) -> None:
        rect = pygame.Rect(surface.get_width() // 2 - 210, 18, 420, 66)
        self._panel(surface, rect)
        goal = "MÅL: BLI KARRIERESUCCESS" if not state.won else "MÅL FULLFØRT!"
        self._text(surface, goal, self.body_bold, (rect.centerx, rect.y + 12), (255, 214, 84), center=True)
        self._text(
            surface,
            f"universitet  •  bolig  •  konsulent  •  {GOAL_SAVINGS} kr",
            self.small_font,
            (rect.centerx, rect.y + 40),
            (225, 232, 238),
            center=True,
        )

    def _draw_controls(self, surface: pygame.Surface) -> None:
        self._text(
            surface,
            "[E] Gå inn   [C] Klær   [H] Bolig   [F1] Hjelp",
            self.small_font,
            (surface.get_width() // 2, surface.get_height() - 28),
            (255, 255, 255),
            center=True,
            shadow=(10, 12, 16),
        )

    def _current_job(self, state: GameState):
        candidates = [
            job
            for job in JOBS.values()
            if job.outfit == state.current_outfit and state.education_level >= job.education
        ]
        if not candidates:
            candidates = [job for job in JOBS.values() if job.outfit == state.current_outfit]
        return max(candidates, key=lambda job: job.wage) if candidates else None

    def _bar(
        self,
        surface: pygame.Surface,
        rect: pygame.Rect,
        value: float,
        color: tuple[int, int, int],
        label: str,
    ) -> None:
        self._text(surface, label, self.small_font, (rect.x, rect.y - 6), (230, 236, 240))
        pygame.draw.rect(surface, (62, 72, 82), rect, border_radius=7)
        fill = rect.inflate(-4, -4)
        fill.width = max(0, int(fill.width * max(0.0, min(1.0, value / 100))))
        if fill.width > 0:
            pygame.draw.rect(surface, color, fill, border_radius=5)

    def _panel(
        self,
        surface: pygame.Surface,
        rect: pygame.Rect,
        fill: tuple[int, int, int] = (18, 24, 32),
        border: tuple[int, int, int] = (70, 84, 96),
    ) -> None:
        pygame.draw.rect(surface, (6, 9, 12), rect.move(4, 5), border_radius=12)
        pygame.draw.rect(surface, fill, rect, border_radius=12)
        pygame.draw.rect(surface, border, rect, 2, border_radius=12)

    def _text(
        self,
        surface: pygame.Surface,
        value: str,
        font: pygame.font.Font,
        position,
        color,
        center: bool = False,
        shadow: tuple[int, int, int] | None = None,
    ) -> pygame.Rect:
        if shadow:
            shadow_text = font.render(value, True, shadow)
            if center:
                surface.blit(shadow_text, shadow_text.get_rect(center=position))
            else:
                surface.blit(shadow_text, shadow_text.get_rect(topleft=position).move(2, 2))
        text = font.render(value, True, color)
        rect = text.get_rect(center=position) if center else text.get_rect(topleft=position)
        surface.blit(text, rect)
        return rect

    def wrap_text(self, text: str, font: pygame.font.Font, max_width: int) -> list[str]:
        words = text.split()
        lines: list[str] = []
        current = ""
        for word in words:
            candidate = word if not current else f"{current} {word}"
            if font.size(candidate)[0] <= max_width:
                current = candidate
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines or [""]
