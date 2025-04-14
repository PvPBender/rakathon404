from typing import Literal
from enum import Enum


type YesNoType = Literal['Ano',  'Ne', 'Není k dispozici']
type Gender = Literal["Muž", "Žena", "Jiné"] # Undifferentiated = Jiné

# A
type Smoker = Literal[
    "Aktivní kuřák", "Bývalý kuřák", "Pasivní kuřák", "Nekuřák", "Údaj není k dispozici"
]
type Alcohol = Literal[
    "Abstinent", "Příležitostní konzumace", "Denní konzumace", "Údaj není k dispozici"
]
type DrugAddiction = Literal[
    "Aktuálně drogově závislý(á)", "Nikdy drogově závislý(á)", "Drogově závislý(á) v minulosti", "Údaj není k dispozici"
]

# B1
# TODO maybe use the codes 
# https://www.wikiskripta.eu/w/MKN-O#:~:text=Klasifikace%20je%20vyj%C3%A1d%C5%99ena%20kombinac%C3%AD%20t%C5%99%C3%AD,%C4%8D%C3%ADslice%20za%20lom%C3%ADtkem%20biologick%C3%A9%20chov%C3%A1n%C3%AD.

# class BiologickeChovani(Enum):
#     Benigní = 0,
#     Nejisté_neznámé = 1,
#     In_situ = 2,
#     Maligní_primární = 3,
#     Maligní_sekundární = 6


type Laterality = Literal[
    "Vpravo", "Vlevo", "Oboustranně", "Odpadá", "Neznámo"
]
type BiologicalBehaviour = Literal[
    "Benigní", "Nejisté/neznámé", "In situ", "Maligní primární", "Maligní sekundární"
]

type tnmCT = Literal[
    "X", "0", "is", "1", "2", "3", "4"
]

type tnmCounts = Literal[
    "1", "2", "3", "m"
]

type tnmCN = Literal[
    "X", "0", "1", "2", "3"
]

type tnmCM = Literal[
    "X", "0", "1"
]

type DiagnosticModalities = Literal[
    "Klinicky jasné", "Klinické vyšetření", "Laboratorní vyšetření/nádorové markery",
    "Cytologie", "Histologie metastázy", "Histologie primárního nádoru",
    "Molekulárně-biologické vyšetření", "Pitva", "DCO"
]

type MetastasisLocation = Literal[
    "Mozek", "Plíce", "Játra", "Viscerální mimo výše uvedené", "Kost", "Měkké tkáně", "Jiné", "Žádné"
]