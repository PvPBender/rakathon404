from pydantic import BaseModel, Field
from typing import List, Optional
from model.types import YesNoType, Smoker, Alcohol, DrugAddiction

# --- M.A.1.1 ---
class TumorSyndrome(BaseModel):
    M_A_1_1_1: str = ""  # Relevantní nádorový predispoziční syndrom – Podmíněně povinné, 1..1
    M_A_1_1_2: List[str]  # Název predispozičního syndromu – Povinné, 1..*
    M_A_1_1_2_1: Optional[str] = ""  # Jiný predispoziční syndrom – Povinné if M_A_1_1_2 includes "Jiný"
    M_A_1_1_3: Optional[str] = None  # Komentář – Volitelné


# --- M.A.1.2 ---
class OncoFamilyHistory(BaseModel):
    M_A_1_2_1: str = ""  # Příbuzenský stav – Podmíněně povinné, 1..1
    M_A_1_2_2: str = ""  # Onkologické onemocnění – specifikace – Podmíněně povinné, 1..1
    M_A_1_2_3: Optional[List[str]]  # Onkologické onemocnění – kód MKN-10 – Volitelné, 0..*


# --- M.A.1.3 ---
class DiseaseWithComment(BaseModel):
    diagnózy: List[str]  # Výčet z číselníku – Povinné, 1..*
    komentář: Optional[str] = None  # Komentář – Podmíněně povinné, 0..1


class RelevantDisease(BaseModel):
    # Non-default fields first
    M_A_1_3_1: str = ""  # Srdce a cévy
    M_A_1_3_2: str = ""  # Metabolické
    M_A_1_3_3: str = ""  # Plicní
    M_A_1_3_4: str = ""  # GIT
    M_A_1_3_5: str = ""  # Ledviny
    M_A_1_3_6: str = ""  # Autoimunitní
    M_A_1_3_7: str = ""  # Závažné endokrinologické onemocnění
    M_A_1_3_8: str = ""  # Neuropsychiatrické onemocnění
    M_A_1_3_9: str = ""  # Gynekologické onemocnění + anamnéza
    M_A_1_3_10: str = ""  # Závažné infekční onemocnění
    M_A_1_3_11: YesNoType  # Orgánová transplantace		ANO/NE/údaj není k dispozici
    M_A_1_3_11_1: List[str]  # Organy

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
class PreviousOncologicalDisease(BaseModel):
    M_A_1_5_1: YesNoType  # Předchozí onkologické onemocnění – Povinné, 1..1
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
class OncologicalScreening(BaseModel):
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
class Alergy(BaseModel):
    # Non-default fields first
    M_A_1_7_1: YesNoType  # Léková alergie – Povinné, 1..1
    M_A_1_7_2: YesNoType  # Alergie na jód/kontrastní látky – Povinné, 1..1
    M_A_1_7_3: YesNoType  # Jiné alergie (např. potravinové, pyly, prach) – Povinné, 1..1

    # Default fields after
    M_A_1_7_1_1: Optional[str] = None  # Specifikace lékové alergie – Podmíněně povinné, 0..1
    M_A_1_7_2_1: Optional[str] = None  # Specifikace jód/kontrast – Podmíněně povinné, 0..1
    M_A_1_7_3_1: Optional[str] = None  # Specifikace jiných alergií – Podmíněně povinné, 0..1



# --- M.A.1.8 ---
class Abusus(BaseModel): # MA_1_8
    smoker: Smoker = Field(alias="M_A_1_8_1")  # Kouření – Povinné, 1..1
    alcohol: Alcohol = Field(alias="M_A_1_8_2")  # Alkohol – Povinné, 1..1
    drugAddiction: DrugAddiction = Field(alias="M_A_1_8_3")  # Drogová závislost – Povinné, 1..1

    # Default fields after
    M_A_1_8_1_1: Optional[float] = None  # Počet denně vykouřených balíčků/krabiček – Podmíněně povinné, 0..1
    M_A_1_8_1_2: Optional[float] = None  # Počet let kouření – Podmíněně povinné, 0..1
    M_A_1_8_1_3: Optional[float] = None  # Počet balíčkoroků – Podmíněně povinné, 0..1
    M_A_1_8_1_4: Optional[str] = None  # Kouření – komentář – Volitelné, 0..1
    M_A_1_8_2_1: Optional[str] = None  # Alkohol – komentář – Volitelné, 0..1
    M_A_1_8_3_1: Optional[str] = None  # Drogová závislost – komentář – Volitelné, 0..1


class AntropometricData(BaseModel):
    M_A_2_1: str = ""    # Datum měření – Povinné
    M_A_2_2: float = 0  # Výška v cm – Povinné, 1..1
    M_A_2_3: float = 0  # Hmotnost v kg – Povinné, 1..1
    M_A_2_4: Optional[float] = (
        None  # BMI – Podmíněně povinné (automatický výpočet), 1..1
    )
    M_A_2_5: Optional[float] = (
        None  # BSA – Podmíněně povinné (automatický výpočet), 1..1
    )

# --- M.A.3 ---
class OverallPacientState(BaseModel):
    M_A_3_1_1: Optional[int] = None        # Performance status (ECOG) – 0 to 5
    M_A_3_1_2: Optional[str] = None        # Datum hodnocení

# @dataclass
# class MA32:
#     M_A_3_2_1: Optional[int] = None        # Karnofského index – 0 to 100
#     M_A_3_2_2: Optional[str] = None        # Datum hodnocení

# --- M.A.4 ---
class FertilityPreservationMeasures(BaseModel):
    M_A_4_1: str = ""                    # Typ opatření
    M_A_4_2: Optional[str] = None          # Datum provedení/zahájení opatření
    M_A_4_3: Optional[str] = None          # Místo uložení vzorku
    M_A_4_4: Optional[str] = None          # Volitelný komentář



# --- M.A.1 ---
class RelevantFactors(BaseModel):
    M_A_1_1: TumorSyndrome = Field(alias="M_A_1_1")
    M_A_1_2: Optional[OncoFamilyHistory] = Field(alias="M_A_1_2")
    M_A_1_3: Optional[RelevantDisease] = Field(alias="M_A_1_3")
    M_A_1_5: Optional[PreviousOncologicalDisease] = Field(alias="M_A_1_5")
    M_A_1_6: Optional[OncologicalScreening] = Field(alias="M_A_1_6")
    M_A_1_7: Optional[Alergy] = Field(alias="M_A_1_7")
    M_A_1_8: Optional[Abusus] = Field(alias="M_A_1_8")


# --- Modul A ---
class PacientParameters(BaseModel):
    relevantFactors: RelevantFactors = Field(alias="M_A_1")
    antropometricData: Optional[AntropometricData] = Field(alias="M_A_2")
    overallPacientState: Optional[OverallPacientState] = Field(alias="M_A_3")
    # M_A_3_2: Optional[List[MA32]] = field(default_factory=list)    #Opatření k zachování plodnosti před onkologickou léčbou TODO duplicate? error in template?
    fertilityPreservationMeasures: Optional[FertilityPreservationMeasures] = Field(alias="M_A_4")
