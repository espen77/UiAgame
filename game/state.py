from __future__ import annotations

from dataclasses import dataclass

import pygame

from .content import (
    APARTMENT_PRICE,
    APARTMENT_RENT,
    DAY_SECONDS,
    EDUCATION_POINTS_PER_LEVEL,
    FOOD_PRICE,
    GOAL_SAVINGS,
    HOSTEL_PRICE,
    JOBS,
    MAX_EDUCATION_POINTS,
    NO_APARTMENT_COST,
    OUTFITS,
    education_name,
)


@dataclass
class ShiftState:
    job_id: str
    total: float
    remaining: float


class GameState:
    def __init__(self) -> None:
        self.money = 500
        self.hunger = 100.0
        self.energy = 100.0
        self.education_progress = 0
        self.owned_outfits = {"shorts"}
        self.current_outfit = "shorts"
        self.completed_jobs: set[str] = set()
        self.apartment = False
        self.day = 1
        self.day_time = 0.0
        self.last_soup_day = 0
        self.won = False
        self.shift: ShiftState | None = None
        self.position = pygame.Vector2(655, 575)
        self.facing = pygame.Vector2(0, 1)

    @property
    def education_level(self) -> int:
        return min(3, self.education_progress // EDUCATION_POINTS_PER_LEVEL)

    @property
    def education_label(self) -> str:
        return education_name(self.education_level)

    def work_blocker(self, job_id: str) -> str | None:
        job = JOBS[job_id]
        if job.outfit not in self.owned_outfits:
            return f"Kjøp {OUTFITS[job.outfit].name} for å få denne jobben."
        if self.education_level < job.education:
            required = education_name(job.education)
            return f"Krev {required}. Karl har {self.education_label}."
        if self.hunger < 15:
            return "Karl er for sulten. Kjøp mat først."
        if self.energy < 20:
            return "Karl er for sliten. Hvil i boligmenyen."
        if self.shift is not None:
            return "Et skift er allerede i gang."
        return None

    def start_shift(self, job_id: str) -> tuple[bool, str]:
        blocker = self.work_blocker(job_id)
        if blocker:
            return False, blocker
        job = JOBS[job_id]
        self.current_outfit = job.outfit
        self.shift = ShiftState(job_id=job_id, total=job.duration, remaining=job.duration)
        return True, f"Skift startet: {job.name}."

    def update_shift(self, dt: float) -> str | None:
        if self.shift is None:
            return None
        self.shift.remaining = max(0.0, self.shift.remaining - dt)
        if self.shift.remaining > 0:
            return None
        job = JOBS[self.shift.job_id]
        self.money += job.wage
        self.hunger = max(0.0, self.hunger - 10)
        self.energy = max(0.0, self.energy - 18)
        self.completed_jobs.add(job.id)
        self.shift = None
        return f"Skiftet er ferdig. Karl tjente {job.wage} kr."

    def buy_outfit(self, outfit_id: str) -> tuple[bool, str]:
        outfit = OUTFITS[outfit_id]
        if outfit_id in self.owned_outfits:
            self.current_outfit = outfit_id
            return True, f"Karl tok på {outfit.name}."
        if not outfit.purchasable:
            return False, "Denne drakten kan ikke kjøpes."
        if self.money < outfit.price:
            return False, f"Karl trenger {outfit.price - self.money} kr mer til {outfit.name}."
        self.money -= outfit.price
        self.owned_outfits.add(outfit_id)
        self.current_outfit = outfit_id
        return True, f"{outfit.name} kjøpt og tatt på."

    def study(self, university: bool) -> tuple[bool, str]:
        if self.education_progress >= MAX_EDUCATION_POINTS:
            return False, "Karl har allerede fullført høyeste utdanning."
        if university and self.education_level < 2:
            return False, "Universitetet krever ferdig videregående."
        if not university and self.education_progress >= 6:
            return False, "Videregående er fullført. Universitetet ligger i vest."
        cost = 350 if university else 150
        if self.money < cost:
            return False, f"Studier koster {cost} kr."
        self.money -= cost
        self.education_progress += 1
        if "school" not in self.owned_outfits:
            self.owned_outfits.add("school")
        self.current_outfit = "school"
        self.energy = max(0.0, self.energy - 6)
        return True, (
            f"En studieuke fullført. Utdanning: {self.education_label} "
            f"({self.education_progress}/{MAX_EDUCATION_POINTS})."
        )

    def buy_food(self) -> tuple[bool, str]:
        if self.money < FOOD_PRICE:
            return False, f"Mat koster {FOOD_PRICE} kr."
        self.money -= FOOD_PRICE
        self.hunger = min(100.0, self.hunger + 40)
        return True, f"Karl spiste mat for {FOOD_PRICE} kr."

    def take_soup(self) -> tuple[bool, str]:
        if self.last_soup_day == self.day:
            return False, "Suppen er allerede hentet i dag."
        self.last_soup_day = self.day
        self.hunger = min(100.0, self.hunger + 25)
        return True, "Karl fikk varm suppe fra menigheten."

    def buy_apartment(self) -> tuple[bool, str]:
        if self.apartment:
            return True, "Karl bor allerede i egen bolig."
        if self.money < APARTMENT_PRICE:
            return False, f"Leiligheten koster {APARTMENT_PRICE} kr."
        self.money -= APARTMENT_PRICE
        self.apartment = True
        return True, "Karl kjøpte sin første bolig i Grimstad."

    def sleep(self) -> tuple[bool, str]:
        if not self.apartment:
            if self.money < HOSTEL_PRICE:
                return False, f"Billig overnatting koster {HOSTEL_PRICE} kr."
            self.money -= HOSTEL_PRICE
            self.energy = min(100.0, 86)
            return True, f"Karl sov på hospits for {HOSTEL_PRICE} kr."
        self.energy = 100.0
        self.hunger = max(0.0, self.hunger - 8)
        return True, "Karl sov godt i sin egen leaky."

    def advance_time(self, dt: float, moving: bool) -> str | None:
        hunger_drain = 0.32
        energy_drain = 0.18 if moving else 0.07
        if self.hunger <= 0:
            energy_drain += 0.2
        self.hunger = max(0.0, self.hunger - dt * hunger_drain)
        self.energy = max(0.0, self.energy - dt * energy_drain)
        self.day_time += dt
        day_message = None
        while self.day_time >= DAY_SECONDS:
            self.day_time -= DAY_SECONDS
            day_message = self._start_new_day()
        return day_message

    def _start_new_day(self) -> str:
        self.day += 1
        cost = APARTMENT_RENT if self.apartment else NO_APARTMENT_COST
        paid = min(self.money, cost)
        self.money -= paid
        self.hunger = max(0.0, self.hunger - 12)
        recovery = 28 if self.apartment else 14
        self.energy = min(100.0, self.energy + recovery)
        if paid < cost:
            return f"Dag {self.day}: Karl klarte ikke boligkostnaden på {cost} kr."
        return f"Dag {self.day}: boligkostnad {cost} kr. Energi og mat må fylles."

    def update_goal(self) -> bool:
        requirements = {
            "Utdanning": self.education_level >= 3,
            "Egen bolig": self.apartment,
            "Konsulentjobb fullført": "consultant" in self.completed_jobs,
            f"{GOAL_SAVINGS} kr spare": self.money >= GOAL_SAVINGS,
        }
        complete = all(requirements.values())
        if complete and not self.won:
            self.won = True
            return True
        return False

    def goal_requirements(self) -> list[tuple[str, bool]]:
        return [
            ("Fullfør universitetsutdanning", self.education_level >= 3),
            ("Kjøp egen bolig", self.apartment),
            ("Fullfør ett skift som konsulent", "consultant" in self.completed_jobs),
            (f"Ha minst {GOAL_SAVINGS} kr", self.money >= GOAL_SAVINGS),
        ]
