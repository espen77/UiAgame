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
    purchasable: bool = True


OUTFITS: dict[str, Outfit] = {
    "shorts": Outfit(
        id="shorts",
        name="Shorts",
        price=0,
        color=(86, 150, 214),
        image="shorts.png",
        description="Sommerklær som passer til jobb ved kaia.",
    ),
    "casual": Outfit(
        id="casual",
        name="Casual",
        price=300,
        color=(58, 62, 78),
        image="casual.png",
        description="Mørk polo og jeans. En fornuftig start i butikk.",
    ),
    "hoodie": Outfit(
        id="hoodie",
        name="Hoodie",
        price=650,
        color=(44, 46, 58),
        image="hoodie.png",
        description="Mykt og praktisk for lagerarbeid på havnen.",
    ),
    "boilersuit": Outfit(
        id="boilersuit",
        name="Arbeidskledel",
        price=1100,
        color=(236, 186, 36),
        image="boilersuit.png",
        description="Synlig refleks og verktøy. Perfekt for bilmekanikk.",
    ),
    "looser": Outfit(
        id="looser",
        name="Gamer-hoodie",
        price=1800,
        color=(70, 72, 88),
        image="looser.png",
        description="Avslappet IT-drakt som passer på universitetet.",
    ),
    "suit": Outfit(
        id="suit",
        name="Dress",
        price=2600,
        color=(24, 30, 52),
        image="suit.png",
        description="Profesjonell dress for menighetsarbeid og rådgivning.",
    ),
    "school": Outfit(
        id="school",
        name="Skoleuniform",
        price=0,
        color=(32, 56, 104),
        image="school.png",
        description="Blir utdelt når Karl begynner på Vidregående.",
        purchasable=False,
    ),
    "winner": Outfit(
        id="winner",
        name="Champion",
        price=0,
        color=(214, 164, 42),
        image="winner.png",
        description="Karl sin seiersdrakt etter en fullstendig karriere.",
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
        education=0,
        wage=120,
        duration=4.0,
        description="Hjelper ved kaia og får grunnleggende arbeidserfaring.",
    ),
    "store_assistant": Job(
        id="store_assistant",
        name="Butikkassistent",
        outfit="casual",
        location="gas_station",
        education=0,
        wage=160,
        duration=4.0,
        description="Betjener kunder og jobber i butikken ved Auto45.",
    ),
    "warehouse": Job(
        id="warehouse",
        name="Lagerarbeider",
        outfit="hoodie",
        location="harbor",
        education=1,
        wage=240,
        duration=5.0,
        description="Flytter varer og tar ansvar i lageret ved havnen.",
    ),
    "mechanic": Job(
        id="mechanic",
        name="Bilmekaniker",
        outfit="boilersuit",
        location="gas_station",
        education=2,
        wage=340,
        duration=6.0,
        description="Reparerer biler og får fast tilknytning til Auto45.",
    ),
    "it_support": Job(
        id="it_support",
        name="IT-support",
        outfit="looser",
        location="university",
        education=2,
        wage=400,
        duration=6.0,
        description="Løser problemer for ansatte og studenter ved universitetet.",
    ),
    "church_worker": Job(
        id="church_worker",
        name="Menighetsarbeider",
        outfit="suit",
        location="church",
        education=2,
        wage=360,
        duration=5.0,
        description="Organiserer arrangementer og bidrar i menigheten.",
    ),
    "consultant": Job(
        id="consultant",
        name="Universitetskonsulent",
        outfit="suit",
        location="university",
        education=3,
        wage=600,
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
        name="Universitetet i vest",
        short_name="Universitet",
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
        name="Auto45 ved motorveyen",
        short_name="Auto45",
        x=0.64,
        y=0.32,
        color=(214, 96, 64),
        description="Butikk, mat og bilmekanikk ved motorveyen i nord.",
    ),
    "freeway_house": Location(
        id="freeway_house",
        name="Billig hus ved motorveien",
        short_name="Motorveishuset",
        x=0.78,
        y=0.20,
        color=(214, 172, 62),
        description="Billig bolig nær motorveien, men langt fra havet.",
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
    "sea_house": Location(
        id="sea_house",
        name="Dyrt hus ved havet",
        short_name="Huset ved havet",
        x=0.27,
        y=0.70,
        color=(52, 178, 196),
        description="Eksklusiv bolig med utsikt, høy leie og beste rest.",
    ),
    "school": Location(
        id="school",
        name="Vidregående skole i midten",
        short_name="Vidregående",
        x=0.48,
        y=0.48,
        color=(52, 158, 96),
        description="Studier for å låse opp bedre jobber.",
    ),
    "bar": Location(
        id="bar",
        name="Baren mellom skolen og havnen",
        short_name="Baren",
        x=0.35,
        y=0.60,
        color=(186, 78, 120),
        description="Billig mat og litt ekstra energi til kvelden.",
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
    recovery: int
    location: str
    description: str


HOUSING: dict[str, Housing] = {
    "freeway_house": Housing(
        id="freeway_house",
        name="Billig hus ved motorveien",
        price=3500,
        rent=90,
        recovery=88,
        location="freeway_house",
        description="Billig bolig nær motorveien. Praktisk, men ikke luksus.",
    ),
    "sea_house": Housing(
        id="sea_house",
        name="Dyrt hus ved havet",
        price=12000,
        rent=260,
        recovery=100,
        location="sea_house",
        description="Utsikt over havet, full rest og høy daglig leie.",
    ),
}

EDUCATION_NAMES = {
    0: "Grunnskole",
    1: "Fagskole",
    2: "Videregående",
    3: "Universitet",
}

EDUCATION_POINTS_PER_LEVEL = 3
MAX_EDUCATION_POINTS = 9
DAY_SECONDS = 180.0
BAR_FOOD_PRICE = 40
FOOD_PRICE = 55
HOSTEL_PRICE = 80
NO_APARTMENT_COST = 35
GOAL_SAVINGS = 8000


def jobs_at(location_id: str) -> tuple[Job, ...]:
    return tuple(job for job in JOBS.values() if job.location == location_id)


def jobs_for_outfit(outfit_id: str) -> tuple[Job, ...]:
    return tuple(job for job in JOBS.values() if job.outfit == outfit_id)


def housing_at(location_id: str) -> Housing | None:
    return next((home for home in HOUSING.values() if home.location == location_id), None)


def education_name(level: int) -> str:
    return EDUCATION_NAMES[max(0, min(level, 3))]
