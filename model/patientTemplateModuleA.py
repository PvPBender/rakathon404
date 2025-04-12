from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class AnoNeUdaje:
    ano: str
    ne: str
    udaj_neni_k_dispozici: str 

# --- M.A.1.1 ---
@dataclass
class MA11:
    M_A_1_1_1: (
        str  # Relevantní nádorový predispoziční syndrom – Podmíněně povinné, 1..1
    )
    M_A_1_1_2: List[str]  # Název predispozičního syndromu – Povinné, 1..*
    M_A_1_1_2_1: Optional[str] = (
        None  # Jiný predispoziční syndrom – Povinné if M_A_1_1_2 includes "Jiný"
    )
    M_A_1_1_3: Optional[str] = None  # Komentář – Volitelné


# --- M.A.1.2 ---
@dataclass
class MA12:
    M_A_1_2_1: str  # Příbuzenský stav – Podmíněně povinné, 1..1
    M_A_1_2_2: str  # Onkologické onemocnění – specifikace – Podmíněně povinné, 1..1
    M_A_1_2_3: Optional[List[str]] = (
        None  # Onkologické onemocnění – kód MKN-10 – Volitelné, 0..*
    )


# --- M.A.1.3 ---
@dataclass
class DiseaseWithComment:
    diagnózy: List[str]  # Výčet z číselníku – Povinné, 1..*
    komentář: Optional[str] = None  # Komentář – Podmíněně povinné, 0..1


@dataclass
class MA13:
    # Non-default fields first
    M_A_1_3_1: str  # Srdce a cévy
    M_A_1_3_2: str  # Metabolické
    M_A_1_3_3: str  # Plicní
    M_A_1_3_4: str  # GIT
    M_A_1_3_5: str  # Ledviny
    M_A_1_3_6: str  # Autoimunitní
    M_A_1_3_7: str  # Závažné endokrinologické onemocnění
    M_A_1_3_8: str  # Neuropsychiatrické onemocnění
    M_A_1_3_9: str  # Gynekologické onemocnění + anamnéza
    M_A_1_3_10: str  # Závažné infekční onemocnění
    M_A_1_3_11: AnoNeUdaje  # Orgánová transplantace		ANO/NE/údaj není k dispozici
    M_A_1_3_11_1: List[str]  # Organ

    # Default fields after
    M_A_1_3_1_1: Optional[str] = None  # Srdce a cévy - komentář
    M_A_1_3_2_1: Optional[str] = None  # Metabolické - komentář
    M_A_1_3_3_1: Optional[str] = None  # Plicní - komentář
    M_A_1_3_4_1: Optional[str] = None  # GIT - komentář
    M_A_1_3_5_1: Optional[str] = None  # Ledviny - komentář
    M_A_1_3_6_1: Optional[str] = None  # Autoimunitní - komentář
    M_A_1_3_7_1: Optional[str] = None  # Závažné endokrinologické onemocnění - komentář
    M_A_1_3_8_1: Optional[str] = None  # Neuropsychiatrické onemocnění - komentář
    M_A_1_3_9_1: Optional[str] = None  # Onemocnění / funkční stav - komentář
    M_A_1_3_9_2: Optional[str] = None  # HPV pozitivita
    M_A_1_3_9_3: Optional[str] = None  # Menopauza (Rok)
    M_A_1_3_9_4: Optional[str] = None  # Hormonoterapie
    M_A_1_3_9_5: Optional[str] = None  # Antikoncepce
    M_A_1_3_10_1: Optional[str] = None  # Závažné infekční onemocnění - komentář
    M_A_1_3_11_1_1: Optional[str] = None  # Jiné organy
    M_A_1_3_11_2: Optional[str] = None  # Rok transplantace
    M_A_1_3_11_3: Optional[str] = None  # Komentář
    M_A_1_3_12: Optional[str] = None  # jine relevantni zdravotni nalezy


# --- M.A.1.5 ---
@dataclass
class MA15:
    M_A_1_5_1: AnoNeUdaje  # Předchozí onkologické onemocnění – Povinné, 1..1
    M_A_1_5_1_1: Optional[str] = (
        None  # Onemocnění/funkční stav - komentář – Podmíněně povinné, 1..1
    )
    M_A_1_5_1_2: Optional[str] = None  # Rok diagnózy – Volitelné, 0..1
    M_A_1_5_1_3: Optional[str] = (
        None  # Léčen(a) ve zdravotnickém zařízení – Volitelné, 0..1
    )
    M_A_1_5_1_4: Optional[str] = (
        None  # Onkologické nemocnění - kód MKN-O-3 – Volitelné, 0..1
    )


# --- M.A.1.6 ---
@dataclass
class MA16:
    # Non-default fields first
    M_A_1_6_1: str  # Mamografický screening – Povinné, 1..1
    M_A_1_6_2: str  # Screening nádoru děložního hrdla – Povinné, 1..1
    M_A_1_6_3: str  # Screening kolorektálního karcinomu – Povinné, 1..1
    M_A_1_6_4: str  # Plicní screening – Povinné, 1..1
    M_A_1_6_5: str  # Screening prostaty – Povinné, 1..1

    # Default fields after
    M_A_1_6_1_1: Optional[str] = None  # Rok posledního vyšetření – Volitelné, 0..1
    M_A_1_6_2_1: Optional[str] = None  # Rok posledního vyšetření – Volitelné, 0..1
    M_A_1_6_3_1: Optional[str] = None  # Rok posledního vyšetření – Volitelné, 0..1
    M_A_1_6_3_2: Optional[str] = None  # Forma screeningu – Volitelné, 0..1
    M_A_1_6_4_1: Optional[str] = None  # Rok posledního vyšetření – Volitelné, 0..1
    M_A_1_6_5_1: Optional[str] = None  # Rok posledního vyšetření – Volitelné, 0..1


# --- M.A.1.7 ---
@dataclass
class MA17:
    # Non-default fields first
    M_A_1_7_1: AnoNeUdaje  # Léková alergie – Povinné, 1..1
    M_A_1_7_2: AnoNeUdaje  # Alergie na jód/kontrastní látky – Povinné, 1..1
    M_A_1_7_3: AnoNeUdaje  # Jiné alergie (např. potravinové, pyly, prach) – Povinné, 1..1

    # Default fields after
    M_A_1_7_1_1: Optional[str] = None  # Specifikace lékové alergie – Podmíněně povinné, 0..1
    M_A_1_7_2_1: Optional[str] = None  # Specifikace jód/kontrast – Podmíněně povinné, 0..1
    M_A_1_7_3_1: Optional[str] = None  # Specifikace jiných alergií – Podmíněně povinné, 0..1


@dataclass
class Kurak:
    aktivniKurak: str
    byvalyKurak: str
    pasivniKurak: str
    nekurak: str
    udaj_neni_k_dispozici: str


@dataclass
class Alkohol:
    abstinent: str
    prilezitostniKonzumace: str
    denniKonzumace: str
    udaj_neni_k_dispozici: str


@dataclass
class Drogovazavislost:
    aktualneDrogoveZavislost: str
    nikdyDrogoveZavislost: str
    drogoveZavislostVMinulosti: str
    udaj_neni_k_dispozici: str


# --- M.A.1.8 ---
@dataclass
class MA18:
    # Non-default fields first
    M_A_1_8_1: Kurak  # Kouření – Povinné, 1..1 výběr {Aktivní kuřák, Bývalý kuřák, Pasivní kuřák, Nekuřák, údaj není k dispozici}
    M_A_1_8_2: Alkohol  # Alkohol – Povinné, 1..1 výběr {Abstinent, Příležitostní konzumace, Denní konzumace, údaj není k dispozici}
    M_A_1_8_3: Drogovazavislost  # Drogová závislost – Povinné, 1..1 výběr {Aktuálně drogově závislý(á), Nikdy drogově závislý(á), Drogově závislý(á) v minulosti, Údaj není k dispozici}

    # Default fields after
    M_A_1_8_1_1: Optional[float] = None  # Počet denně vykouřených balíčků/krabiček – Podmíněně povinné, 0..1
    M_A_1_8_1_2: Optional[float] = None  # Počet let kouření – Podmíněně povinné, 0..1
    M_A_1_8_1_3: Optional[float] = None  # Počet balíčkoroků – Podmíněně povinné, 0..1
    M_A_1_8_1_4: Optional[str] = None  # Kouření – komentář – Volitelné, 0..1
    M_A_1_8_2_1: Optional[str] = None  # Alkohol – komentář – Volitelné, 0..1
    M_A_1_8_3_1: Optional[str] = None  # Drogová závislost – komentář – Volitelné, 0..1


@dataclass
class MA2:
    M_A_2_1: str  # Datum měření – Povinné
    M_A_2_2: float  # Výška v cm – Povinné, 1..1
    M_A_2_3: float  # Hmotnost v kg – Povinné, 1..1
    M_A_2_4: Optional[float] = (
        None  # BMI – Podmíněně povinné (automatický výpočet), 1..1
    )
    M_A_2_5: Optional[float] = (
        None  # BSA – Podmíněně povinné (automatický výpočet), 1..1
    )

# --- M.A.3 ---
@dataclass
class MA3:
    M_A_3_1_1: Optional[int] = None        # Performance status (ECOG) – 0 to 5
    M_A_3_1_2: Optional[str] = None        # Datum hodnocení

@dataclass
class MA32:
    M_A_3_2_1: Optional[int] = None        # Karnofského index – 0 to 100
    M_A_3_2_2: Optional[str] = None        # Datum hodnocení

# --- M.A.4 ---
@dataclass
class MA4:
    M_A_4_1: str                           # Typ opatření
    M_A_4_2: Optional[str] = None          # Datum provedení/zahájení opatření
    M_A_4_3: Optional[str] = None          # Místo uložení vzorku
    M_A_4_4: Optional[str] = None          # Volitelný komentář



# --- M.A.1 ---
@dataclass
class MA1:
    M_A_1_1: MA11
    M_A_1_2: Optional[List[MA12]] = field(default_factory=list)
    M_A_1_3: Optional[MA13] = None
    M_A_1_5: Optional[List[MA15]] = field(default_factory=list)
    M_A_1_6: Optional[MA16] = None
    M_A_1_7: Optional[MA17] = None
    M_A_1_8: Optional[MA18] = None


# --- Modul A ---
@dataclass
class PacientTemplateModuleA:
    M_A_1: MA1
    M_A_2: Optional[List[MA2]] = field(default_factory=list)
    M_A_3: Optional[List[MA3]] = field(default_factory=list)
    M_A_3_2: Optional[List[MA32]] = field(default_factory=list)         
    M_A_4: Optional[List[MA4]] = field(default_factory=list)
