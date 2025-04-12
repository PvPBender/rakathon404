from dataclasses import dataclass, field
from typing import List, Optional
from model.patientTemplateModuleA import PacientTemplateModuleA as MA
from model.patientTemplateModuleB1 import PacientTemplateModuleB1 as MB1
from model.patientTemplateModuleB2 import PacientTemplateModuleB2 as MB2
from model.patientTemplateModuleC import PacientTemplateModuleC as MC

@dataclass
class AnoNeUdaje:
    ano: str
    ne: str
    udaj_neni_k_dispozici: str 

@dataclass
class IdentifikatorPacienta:
    typ: str                      # Typ identifikátoru (např. rodné číslo, pas)
    identifikator: str           # Identifikátor osoby


@dataclass
class M_1_1:  # Identifikace pacienta
    M_1_1_1: List[str]           # Křestní jméno – Povinné, 1..*
    M_1_1_2: List[str]           # Příjmení – Povinné, 1..*
    M_1_1_3: Optional[str]       # Datum narození – Podmíněně povinné, 1..1 (format: YYYY-MM-DD)
    M_1_1_4: List[IdentifikatorPacienta]  # Identifikátor pacienta – Povinné, 1..*
    M_1_1_5: Optional[List[str]] = field(default_factory=list)  # Státní občanství – Podmíněně povinné, 0..*
    M_1_1_6: str                 # Úřední pohlaví – Povinné, 1..1 (e.g. "M", "F", "O", "U")
    M_1_1_7: Optional[List[str]] = field(default_factory=list)  # Komunikační jazyk – Volitelné, 0..*


@dataclass
class M_1_2:  # Zdravotní pojištění
    M_1_2_1: str                 # Kód zdravotní pojišťovny – Podmíněně povinné, 1..1
    M_1_2_2: str                 # Název zdravotní pojišťovny – Podmíněně povinné, 1..1
    M_1_2_3: Optional[str]       # Číslo zdravotního pojištění – Podmíněně povinné, 1..1 (0..1 dětská MDS)


@dataclass
class M_1:  # Hlavička dokumentu
    M_1_1: M_1_1                 # Identifikace pacienta – 1..1
    M_1_2: M_1_2                 # Zdravotní pojištění – 1..1


@dataclass
class PacientTemplate:
    M_1: M_1                     # Hlavička dokumentu – 1..1
    M_A: MA                     # Pacient – 1..1
    M_B1: MB1                   # Pacient – 1..1
    M_B2: Optional[List[MB2]] = field(default_factory=list)
    M_C: Optional[List[MC]] = field(default_factory=list)
