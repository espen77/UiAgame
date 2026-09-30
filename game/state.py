from __future__ import annotations

from dataclasses import dataclass

import pygame

from .content import (
    DAY_SECONDS,
    FOOD_PRICE,
    GOAL_SAVINGS,
    HOUSING,
    HOSTEL_PRICE,
    JOBS,
    MAX_EDUCATION_GRADE,
    NO_APARTMENT_COST,
    OUTFITS,
    PHARMACY_FOOD_PRICE,
    XP_PER_LEVEL,
    SCHOOL_MAX_GRADE,
    SCHOOL_STUDY_COST,
    SHOP_OUTFITS,
    UNIVERSITY_MIN_GRADE,
    UNIVERSITY_STUDY_COST,
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
        self.education_grade = 1
        self.xp = 0
        self.owned_outfits = {"shorts"}
        self.current_outfit = "shorts"
        self.completed_jobs: set[str] = set()
        self.apartment = False
        self.home_id: str | None = None
        self.day = 1
        self.day_time = 0.0
        self.last_soup_day = 0
        self.last_church_rest_day = 0
        self.won = False
        self.shift: ShiftState | None = None
        self.position = pygame.Vector2(655, 575)
        self.facing = pygame.Vector2(0, 1)
        self.destination: str | None = None

    @property
    def education_label(self) -> str:
        return education_name(self.education_grade)

    @property
    def career_level(self) -> int:
        return 1 + self.xp // XP_PER_LEVEL

    @property
    def xp_progress(self) -> float:
        return (self.xp % XP_PER_LEVEL) / XP_PER_LEVEL

    def add_xp(self, amount: int) -> int:
        self.xp += max(0, amount)
        return self.xp // XP_PER_LEVEL

    @property
    def home_label(self) -> str:
        return HOUSING[self.home_id].name if self.home_id else "Hospits"

    @property
    def daily_housing_cost(self) -> int:
        return HOUSING[self.home_id].rent if self.home_id else NO_APARTMENT_COST

    def work_blocker(self, job_id: str) -> str | None:
        job = JOBS[job_id]
        if job.outfit not in self.owned_outfits:
            return f"Kjøp {OUTFITS[job.outfit].name} for å få denne jobben."
        if self.education_grade < job.education:
            required = education_name(job.education)
            return f"Krev {required}. Karl er på grade {self.education_grade}."
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
        self.add_xp(max(10, job.wage // 10))
        self.shift = None
        return f"Skiftet er ferdig. Karl tjente {job.wage} kr og fikk XP."

    def required_outfit(self, outfit_id: str) -> str | None:
        tier = OUTFITS[outfit_id].tier
        return next(
            (
                OUTFITS[owned_id].name
                for owned_id in SHOP_OUTFITS
                if OUTFITS[owned_id].tier < tier and owned_id not in self.owned_outfits
            ),
            None,
        )

    def buy_outfit(self, outfit_id: str) -> tuple[bool, str]:
        outfit = OUTFITS[outfit_id]
        if outfit_id in self.owned_outfits:
            self.current_outfit = outfit_id
            return True, f"Karl tok på {outfit.name}."
        if not outfit.purchasable:
            return False, "Denne drakten kan ikke kjøpes."
        previous_tier = self.required_outfit(outfit_id)
        if previous_tier:
            return False, f"Kjøp {previous_tier} før du kan kjøpe {outfit.name}."
        if self.money < outfit.price:
            return False, f"Karl trenger {outfit.price - self.money} kr mer til {outfit.name}."
        self.money -= outfit.price
        self.owned_outfits.add(outfit_id)
        self.current_outfit = outfit_id
        return True, f"{outfit.name} kjøpt og tatt på."

    def study(self, university: bool) -> tuple[bool, str]:
        if self.education_grade >= MAX_EDUCATION_GRADE:
            return False, "Karl har allerede fullført Doktorgrad."
        if university and self.education_grade < UNIVERSITY_MIN_GRADE:
            return False, "Universitetet i Agder krever ferdig Fagskole."
        if not university and self.education_grade >= SCHOOL_MAX_GRADE:
            return False, "Skole er fullført. Universitetet i Agder ligger i vest."
        cost = UNIVERSITY_STUDY_COST if university else SCHOOL_STUDY_COST
        if self.money < cost:
            return False, f"Studier koster {cost} kr."
        self.money -= cost
        self.education_grade += 1
        if "school" not in self.owned_outfits:
            self.owned_outfits.add("school")
        self.current_outfit = "school"
        self.energy = max(0.0, self.energy - 6)
        self.add_xp(25)
        return True, (
            f"En studieuke fullført. Grade {self.education_grade}: {self.education_label}. Du fikk 25 XP."
        )

    def buy_food(self) -> tuple[bool, str]:
        if self.money < FOOD_PRICE:
            return False, f"Mat koster {FOOD_PRICE} kr."
        self.money -= FOOD_PRICE
        self.hunger = min(100.0, self.hunger + 40)
        return True, f"Karl spiste mat for {FOOD_PRICE} kr."

    def buy_pharmacy_food(self) -> tuple[bool, str]:
        if self.money < PHARMACY_FOOD_PRICE:
            return False, f"Måltidet koster {PHARMACY_FOOD_PRICE} kr."
        self.money -= PHARMACY_FOOD_PRICE
        self.hunger = min(100.0, self.hunger + 30)
        self.energy = min(100.0, self.energy + 10)
        return True, f"Karl spiste et måltid på Apotekergården for {PHARMACY_FOOD_PRICE} kr."

    def take_soup(self) -> tuple[bool, str]:
        if self.last_soup_day == self.day:
            return False, "Suppen er allerede hentet i dag."
        self.last_soup_day = self.day
        self.hunger = min(100.0, self.hunger + 25)
        return True, "Karl fikk varm suppe fra menigheten."

    def sleep_church(self) -> tuple[bool, str]:
        if self.last_church_rest_day == self.day:
            return False, "Karl har allerede hvilt i kirken i dag."
        self.last_church_rest_day = self.day
        self.energy = min(100.0, self.energy + (100.0 - self.energy) * 0.10)
        return True, "Karl hvilt i kirken og fikk 10 % energi."

    def buy_home(self, home_id: str) -> tuple[bool, str]:
        home = HOUSING[home_id]
        if self.home_id == home_id:
            return True, f"Karl bor allerede i {home.name.lower()}."
        current_price = HOUSING[self.home_id].price if self.home_id else 0
        if home.price <= current_price:
            return False, "Karl kan ikke bytte til en billigere bolig etter å ha kjøpt en dyrere."
        cost = home.price - current_price
        if self.money < cost:
            return False, f"Karl trenger {cost - self.money} kr mer til {home.name.lower()}."
        self.money -= cost
        self.home_id = home_id
        self.apartment = True
        if current_price:
            return True, f"Karl oppgraderte til {home.name.lower()}."
        return True, f"Karl kjøpte {home.name.lower()} i Grimstad."

    def buy_apartment(self) -> tuple[bool, str]:
        """Backward-compatible shortcut for the original housing system."""
        return self.buy_home("freeway_house")

    def sleep(self) -> tuple[bool, str]:
        if not self.home_id:
            if self.money < HOSTEL_PRICE:
                return False, f"Billig overnatting koster {HOSTEL_PRICE} kr."
            self.money -= HOSTEL_PRICE
            self.energy = min(100.0, self.energy + 35)
            return True, f"Karl sov på hospits for {HOSTEL_PRICE} kr."
        home = HOUSING[self.home_id]
        self.energy = min(100.0, self.energy + (100.0 - self.energy) * home.efficiency)
        self.hunger = max(0.0, self.hunger - 8)
        return True, f"Karl sov i {home.name} med {int(home.efficiency * 100)} % effektiv hvile."

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
        cost = self.daily_housing_cost
        paid = min(self.money, cost)
        self.money -= paid
        self.hunger = max(0.0, self.hunger - 12)
        efficiency = HOUSING[self.home_id].efficiency if self.home_id else 0.0
        recovery = 14 + (100.0 - self.energy) * efficiency * 0.15
        self.energy = min(100.0, self.energy + recovery)
        if paid < cost:
            return f"Dag {self.day}: Karl klarte ikke boligkostnaden på {cost} kr."
        return f"Dag {self.day}: boligkostnad {cost} kr. Energi og mat må fylles."

    def update_goal(self) -> bool:
        requirements = {
            "Doktorgrad": self.education_grade >= 21,
            "Dyrt Hus": self.home_id == "exclusive_house",
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
            ("Fullfør Doktorgrad", self.education_grade >= 21),
            ("Eier Dyrt Hus", self.home_id == "exclusive_house"),
            ("Fullfør ett skift som konsulent", "consultant" in self.completed_jobs),
            (f"Ha minst {GOAL_SAVINGS} kr", self.money >= GOAL_SAVINGS),
        ]
