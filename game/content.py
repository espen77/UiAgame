from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Outfit:
    id: str
    name: str
    price: int
    color: tuple[int, int, int]
    image: str
    description: str
    tier: int = 0
    purchasable: bool = True


OUTFITS: dict[str, Outfit] = {
    "shorts": Outfit(
        id="shorts",
        name="Shorts",
        price=0,
        color=(86, 150, 214),
        image="shorts.png",
        description="Sommerklær som passer til jobb ved kaia.",
        tier=0,
    ),
    "casual": Outfit(
        id="casual",
        name="Casual",
        price=300,
        color=(58, 62, 78),
        image="casual.png",
        description="Mørk polo og jeans. En fornuftig start i butikk.",
        tier=1,
    ),
    "hoodie": Outfit(
        id="hoodie",
        name="Hoodie",
        price=650,
        color=(44, 46, 58),
        image="hoodie.png",
        description="Mykt og praktisk for lagerarbeid på havnen.",
        tier=2,
    ),
    "boilersuit": Outfit(
        id="boilersuit",
        name="Arbeidskledel",
        price=1100,
        color=(236, 186, 36),
        image="boilersuit.png",
        description="Synlig refleks og verktøy. Perfekt for bilmekanikk.",
        tier=3,
    ),
    "looser": Outfit(
        id="looser",
        name="Gamer-hoodie",
        price=1800,
        color=(70, 72, 88),
        image="looser.png",
        description="Avslappet IT-drakt som passer på universitetet.",
        tier=4,
    ),
    "suit": Outfit(
        id="suit",
        name="Dress",
        price=2600,
        color=(24, 30, 52),
        image="suit.png",
        description="Profesjonell dress for menighetsarbeid og rådgivning.",
        tier=5,
    ),
    "school": Outfit(
        id="school",
        name="Skoleuniform",
        price=0,
        color=(32, 56, 104),
        image="school.png",
        description="Blir utdelt når Karl begynner på Vidregående.",
        tier=-1,
        purchasable=False,
    ),
    "winner": Outfit(
        id="winner",
        name="Champion",
        price=0,
        color=(214, 164, 42),
        image="winner.png",
        description="Karl sin seiersdrakt etter en fullstendig karriere.",
        tier=99,
        purchasable=False,
    ),
}

SHOP_OUTFITS = tuple(outfit_id for outfit_id, outfit in OUTFITS.items() if outfit.purchasable)


@dataclass(frozen=True)
class Job:
    id: str
    name: str
    outfit: str
    location: str
    education: int
    wage: int
    duration: float
    description: str


JOBS: dict[str, Job] = {
    "harbor_assistant": Job(
        id="harbor_assistant",
        name="Havneassistent",
        outfit="shorts",
        location="harbor",
        education=1,
        wage=120,
        duration=4.0,
        description="Hjelper ved kaia og får grunnleggende arbeidserfaring.",
    ),
    "store_assistant": Job(
        id="store_assistant",
        name="Butikkassistent",
        outfit="casual",
        location="gas_station",
        education=1,
        wage=170,
        duration=4.0,
        description="Betjener kunder og jobber i butikken ved CircleK.",
    ),
    "clothing_sales": Job(
        id="clothing_sales",
        name="Klesbutikkansatt",
        outfit="casual",
        location="clothing_shop",
        education=1,
        wage=210,
        duration=4.5,
        description="Hjelper kunder med klær og får salgserfaring i butikken.",
    ),
    "warehouse": Job(
        id="warehouse",
        name="Lagerarbeider",
        outfit="hoodie",
        location="harbor",
        education=8,
        wage=280,
        duration=5.0,
        description="Flytter varer og tar ansvar i lageret ved havnen.",
    ),
    "mechanic": Job(
        id="mechanic",
        name="Bilmekaniker",
        outfit="boilersuit",
        location="gas_station",
        education=14,
        wage=430,
        duration=6.0,
        description="Reparerer biler og får fast tilknytning til CircleK.",
    ),
    "it_support": Job(
        id="it_support",
        name="IT-support",
        outfit="looser",
        location="university",
        education=16,
        wage=560,
        duration=6.0,
        description="Løser problemer for ansatte og studenter ved universitetet.",
    ),
    "church_worker": Job(
        id="church_worker",
        name="Menighetsarbeider",
        outfit="suit",
        location="church",
        education=16,
        wage=480,
        duration=5.0,
        description="Organiserer arrangementer og bidrar i menigheten.",
    ),
    "consultant": Job(
        id="consultant",
        name="Universitetskonsulent",
        outfit="suit",
        location="university",
        education=19,
        wage=850,
        duration=7.0,
        description="Karrieretoppen: rådgir universitetet og tjener gode penger.",
    ),
}


@dataclass(frozen=True)
class Location:
    id: str
    name: str
    short_name: str
    x: float
    y: float
    color: tuple[int, int, int]
    description: str


# Positions are normalized against images/grimstad_map.png.
LOCATIONS: dict[str, Location] = {
    "university": Location(
        id="university",
        name="Universitetet i Agder",
        short_name="Universitetet i Agder",
        x=0.17,
        y=0.25,
        color=(72, 96, 196),
        description="Studier, IT-support og den beste konsulentjobben.",
    ),
    "church": Location(
        id="church",
        name="Kirken i øst",
        short_name="Kirken",
        x=0.86,
        y=0.52,
        color=(156, 108, 188),
        description="Menighetsarbeid og gratis suppe en gang per dag.",
    ),
    "gas_station": Location(
        id="gas_station",
        name="CircleK ved motorveien",
        short_name="CircleK",
        x=0.64,
        y=0.32,
        color=(214, 96, 64),
        description="Butikk, mat og bilmekanikk ved motorveyen i nord.",
    ),
    "freeway_house": Location(
        id="freeway_house",
        name="Billig Hus ved motorveien",
        short_name="Billig Hus",
        x=0.78,
        y=0.20,
        color=(214, 172, 62),
        description="Billig bolig nær motorveien, men langt fra havet.",
    ),
    "middle_house": Location(
        id="middle_house",
        name="Middels Hus nær sentrum",
        short_name="Middels Hus",
        x=0.68,
        y=0.57,
        color=(150, 116, 200),
        description="Middels bolig med bedre hvile enn Billig Hus.",
    ),
    "harbor": Location(
        id="harbor",
        name="Havnen i sør",
        short_name="Havnen",
        x=0.44,
        y=0.75,
        color=(36, 150, 178),
        description="Havneassistent og lagerarbeid nær vannet.",
    ),
    "exclusive_house": Location(
        id="exclusive_house",
        name="Dyrt Hus",
        short_name="Dyrt Hus",
        x=0.78,
        y=0.79,
        color=(52, 178, 196),
        description="Eksklusiv bolig sør for kirken med utsikt, høy leie og beste rest.",
    ),
    "school": Location(
        id="school",
        name="Skolen i midten",
        short_name="Skole",
        x=0.48,
        y=0.48,
        color=(52, 158, 96),
        description="Studier for å låse opp bedre jobber.",
    ),
    "pharmacy": Location(
        id="pharmacy",
        name="Apotekergården mellom skolen og havnen",
        short_name="Apotekergården",
        x=0.35,
        y=0.60,
        color=(186, 78, 120),
        description="Billig mat, litt ekstra energi og et lite pause-sted.",
    ),
    "hostel": Location(
        id="hostel",
        name="Hospitset mellom skolen og universitetet",
        short_name="Hospitset",
        x=0.31,
        y=0.36,
        color=(112, 116, 130),
        description="Billig overnatting for Karl når han ikke har egen bolig.",
    ),
    "clothing_shop": Location(
        id="clothing_shop",
        name="Klesbutikken mellom skolen og havnen",
        short_name="Klesbutikken",
        x=0.58,
        y=0.60,
        color=(120, 86, 190),
        description="Her kan Karl kjøpe klærer som åpner nye jobber.",
    ),
}


@dataclass(frozen=True)
class Housing:
    id: str
    name: str
    price: int
    rent: int
    efficiency: float
    location: str
    description: str


HOUSING: dict[str, Housing] = {
    "freeway_house": Housing(
        id="freeway_house",
        name="Billig Hus",
        price=3500,
        rent=90,
        efficiency=0.35,
        location="freeway_house",
        description="Billig bolig nær motorveien. Praktisk, men gir minst rest.",
    ),
    "middle_house": Housing(
        id="middle_house",
        name="Middels Hus",
        price=7000,
        rent=170,
        efficiency=0.65,
        location="middle_house",
        description="Middels bolig nær sentrum med 65 % effektiv hvile.",
    ),
    "exclusive_house": Housing(
        id="exclusive_house",
        name="Dyrt Hus",
        price=12000,
        rent=260,
        efficiency=1.0,
        location="exclusive_house",
        description="Utsikt sør for kirken, 100 % effektiv hvile og høy daglig leie.",
    ),
}

EDUCATION_NAMES = {
    "Barneskole": (1, 7),
    "Ungdomskole": (8, 10),
    "Vidregående skole": (11, 13),
    "Fagskole": (14, 15),
    "Bachelor": (16, 18),
    "Master": (19, 20),
    "Doktorgrad": (21, 25),
}

MAX_EDUCATION_GRADE = 25
SCHOOL_MAX_GRADE = 15
UNIVERSITY_MIN_GRADE = 15
SCHOOL_STUDY_COST = 120
UNIVERSITY_STUDY_COST = 300
DAY_SECONDS = 180.0
PHARMACY_FOOD_PRICE = 65
FOOD_PRICE = 95
HOSTEL_PRICE = 80
NO_APARTMENT_COST = 35
GOAL_SAVINGS = 8000
XP_PER_LEVEL = 100


def jobs_at(location_id: str) -> tuple[Job, ...]:
    return tuple(job for job in JOBS.values() if job.location == location_id)


def jobs_for_outfit(outfit_id: str) -> tuple[Job, ...]:
    return tuple(job for job in JOBS.values() if job.outfit == outfit_id)


def housing_at(location_id: str) -> Housing | None:
    return next((home for home in HOUSING.values() if home.location == location_id), None)


def education_name(grade: int) -> str:
    grade = max(1, min(MAX_EDUCATION_GRADE, grade))
    for name, (first, last) in EDUCATION_NAMES.items():
        if first <= grade <= last:
            return name
    return "Doktorgrad"
