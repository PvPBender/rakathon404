from dataclasses import dataclass, field
from typing import List, Optional
from model.patientTemplateModuleA import PacientTemplateModuleA as MA
from model.patientTemplateModuleB1 import PacientTemplateModuleB1 as MB1
from model.patientTemplateModuleB2 import PacientTemplateModuleB2 as MB2
from model.patientTemplateModuleC import PacientTemplateModuleC as MC

# from model.patientTemplateModuleB2 import PacientTemplateModuleB2 as MB2
# from model.patientTemplateModuleC import PacientTemplateModuleC as MC


@dataclass
class AnoNeUdaje:
    ano: str
    ne: str
    udaj_neni_k_dispozici: str


@dataclass
class IdentifikatorPacienta:
    typ: str  # Typ identifikátoru (např. rodné číslo, pas)
    identifikator: str  # Identifikátor osoby


@dataclass
class M_1_1:  # Identifikace pacienta
    M_1_1_1: List[str] = field(default_factory=list)  # Křestní jméno – Povinné, 1..*
    M_1_1_2: List[str] = field(default_factory=list)  # Příjmení – Povinné, 1..*
    M_1_1_4: int = 0  # Identifikátor pacienta
    M_1_1_6: str = ""  # Úřední pohlaví – can set a default like "U" or leave empty
    M_1_1_3: Optional[str] = None  # Datum narození – Optional
    M_1_1_5: List[str] = field(default_factory=list)  # Státní občanství
    M_1_1_7: List[str] = field(default_factory=list)  # Komunikační jazyk


@dataclass
class M_1_2:  # Zdravotní pojištění
    M_1_2_1: str = ""  # Kód zdravotní pojišťovny – Podmíněně povinné, 1..1
    M_1_2_2: str = ""  # Název zdravotní pojišťovny – Podmíněně povinné, 1..1
    M_1_2_3: List[str] = field(
        default_factory=list
    )  # Číslo zdravotního pojištění – Podmíněně povinné, 1..1 (0..1 dětská MDS)


@dataclass
class M_1:  # Hlavička dokumentu
    M_1_1: "M_1_1" = field(default_factory=M_1_1)  # Identifikace pacienta – 1..1
    M_1_2: "M_1_2" = field(default_factory=M_1_2)  # Zdravotní pojištění – 1..1


@dataclass
class PacientTemplate:
    M_1: "M_1" = field(default_factory=M_1)  # Hlavička dokumentu – 1..1
    M_A: "MA" = field(default_factory=MA)               # Pacient – 1..1
    M_B1: MB1 = field(default_factory=MB1)                      # Pacient – 1..1
    M_B2: Optional[List["MB2"]] = field(default_factory=list)
    # M_C: Optional[List["MC"]] = field(default_factory=list)
