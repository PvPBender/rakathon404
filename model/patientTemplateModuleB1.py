from dataclasses import dataclass
from typing import List, Optional, Union

# --- Value Sets ---
@dataclass
class Lateralita:
    VPRAVO: str = "vpravo"
    VLEVO: str = "vlevo"
    OBOUSTRANNE: str = "oboustranně"
    ODPADA: str = "odpadá"
    NEZNAMO: str = "neznámo"

@dataclass
class BiologickeChovani:
    BENIGNI: str = "0"
    NEJISTE_NEZNAME: str = "1"
    IN_SITU: str = "2"
    MALIGNI_PRIMARNI: str = "3"
    MALIGNI_SEKUNDARNI: str = "6"

@dataclass
class TNM_CT:
    value: str  # one of ["X", "0", "is", "1", "2", "3", "4"]

@dataclass
class TNM_CETNOST:
    value: str  # one of ["1", "2", "3", "m"]

@dataclass
class TNM_CN:
    value: str  # one of ["X", "0", "1", "2", "3"]

@dataclass
class TNM_CM:
    value: str  # one of ["X", "0", "1"]

@dataclass
class MB1:
    # Non-default fields first
    M_B_1_2_1: str
    M_B_1_2_3: str
    M_B_1_2_4: str
    M_B_1_2_5: Lateralita
    M_B_1_2_8: str
    M_B_1_4_1: str  # Výběr diagnostické skupiny (Povinné)
    M_B_3_2_2: str  # Datum relapsu/progrese
    M_B_3_2_2_1: str  # Typ relapsu

    # Default fields after
    M_B_1_1: Optional[int] = None
    M_B_1_2_2: Optional[List[str]] = None
    M_B_1_2_6: Optional[str] = None
    M_B_1_2_7: Optional[str] = None
    M_B_1_2_9: Optional[str] = None
    M_B_1_2_10: Optional[str] = None
    M_B_1_2_11: Optional[BiologickeChovani] = None
    M_B_1_2_12: Optional[str] = None
    M_B_1_2_13: Optional[str] = None
    M_B_1_2_14: Optional[str] = None
    M_B_1_2_15: Optional[str] = None

    M_B_1_3_1_1: Optional[TNM_CT] = None
    M_B_1_3_1_2: Optional[TNM_CETNOST] = None
    M_B_1_3_1_3: Optional[TNM_CN] = None
    M_B_1_3_1_4: Optional[TNM_CM] = None

    M_B_1_3_2_1: Optional[int] = None
    M_B_1_3_2_2: Optional[int] = None
    M_B_1_3_2_3: Optional[int] = None
    M_B_1_3_2_4: Optional[TNM_CT] = None
    M_B_1_3_2_5: Optional[TNM_CETNOST] = None
    M_B_1_3_2_6: Optional[TNM_CN] = None
    M_B_1_3_2_7: Optional[str] = None
    M_B_1_3_2_8: Optional[int] = None
    M_B_1_3_2_9: Optional[int] = None
    M_B_1_3_2_10: Optional[int] = None
    M_B_1_3_2_11: Optional[int] = None
    M_B_1_3_2_12: Optional[TNM_CM] = None

    M_B_1_3_3: Optional[str] = None
    M_B_1_3_4: Optional[List[str]] = None
    M_B_1_3_4_1: Optional[str] = None
    M_B_1_3_5: Optional[str] = None
    M_B_1_3_6: Optional[str] = None
    M_B_1_3_7: Optional[str] = None
    M_B_1_3_8: Optional[str] = None
    M_B_1_3_9: Optional[str] = None

    M_B_2_XX: Optional[str] = None  # Volitelný komentář / doplnění / slovní popis diagnózy
    M_B_3_2_1: Optional[bool] = None  # Trvá léčebná odpověď
    M_B_3_2_3: Optional[str] = None  # Volitelný komentář

@dataclass
class PacientTemplateModuleB1:
    M_B_1 : MB1