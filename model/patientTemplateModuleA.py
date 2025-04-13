from pydantic import BaseModel, Field
from typing import List, Optional
from model.types import YesNoType, Smoker, Alcohol, DrugAddiction

# --- M.A.1.1 ---
class TumorSyndrome(BaseModel):
    relevantTumorSyndrome: str = Field(default="", alias="M_A_1_1_1")
    syndromeNames: List[str] = Field(alias="M_A_1_1_2")
    otherSyndrome: Optional[str] = Field(default="", alias="M_A_1_1_2_1")
    comment: Optional[str] = Field(default=None, alias="M_A_1_1_3")


# --- M.A.1.2 ---
class OncoFamilyHistory(BaseModel):
    familialRelation: str = Field(default="", alias="M_A_1_2_1")
    cancerDiagnosisDetail: str = Field(default="", alias="M_A_1_2_2")
    cancerICD10Codes: Optional[List[str]] = Field(alias="M_A_1_2_3")


# --- M.A.1.3 ---
class DiseaseWithComment(BaseModel):
    diagnoses: List[str]  # Výčet z číselníku – Povinné, 1..*
    comment: Optional[str] = None  # Komentář – Podmíněně povinné, 0..1


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
    hadCancer: YesNoType = Field(alias="M_A_1_5_1")
    previousCancerComment: Optional[str] = Field(default=None, alias="M_A_1_5_1_1")
    diagnosisYear: Optional[str] = Field(default=None, alias="M_A_1_5_1_2")
    treatedFacility: Optional[str] = Field(default=None, alias="M_A_1_5_1_3")
    icdOCode: Optional[str] = Field(default=None, alias="M_A_1_5_1_4")


# --- M.A.1.6 ---
class OncologicalScreening(BaseModel):
    mammography: str = Field(alias="M_A_1_6_1")
    cervical: str = Field(alias="M_A_1_6_2")
    colorectal: str = Field(alias="M_A_1_6_3")
    lung: str = Field(alias="M_A_1_6_4")
    prostate: str = Field(alias="M_A_1_6_5")

    mammographyYear: Optional[str] = Field(default=None, alias="M_A_1_6_1_1")
    cervicalYear: Optional[str] = Field(default=None, alias="M_A_1_6_2_1")
    colorectalYear: Optional[str] = Field(default=None, alias="M_A_1_6_3_1")
    colorectalForm: Optional[str] = Field(default=None, alias="M_A_1_6_3_2")
    lungYear: Optional[str] = Field(default=None, alias="M_A_1_6_4_1")
    prostateYear: Optional[str] = Field(default=None, alias="M_A_1_6_5_1")


# --- M.A.1.7 ---
class Alergy(BaseModel):
    drug: YesNoType = Field(alias="M_A_1_7_1")
    iodine: YesNoType = Field(alias="M_A_1_7_2")
    other: YesNoType = Field(alias="M_A_1_7_3")

    drugSpec: Optional[str] = Field(default=None, alias="M_A_1_7_1_1")
    iodineSpec: Optional[str] = Field(default=None, alias="M_A_1_7_2_1")
    otherSpec: Optional[str] = Field(default=None, alias="M_A_1_7_3_1")


# --- M.A.1.8 ---
class Abusus(BaseModel):
    smoker: Smoker = Field(alias="M_A_1_8_1")
    alcohol: Alcohol = Field(alias="M_A_1_8_2")
    drugAddiction: DrugAddiction = Field(alias="M_A_1_8_3")

    cigarettesPerDay: Optional[int] = Field(default=None, alias="M_A_1_8_1_1")
    smokingYears: Optional[float] = Field(default=None, alias="M_A_1_8_1_2")
    packYears: Optional[int] = Field(default=None, alias="M_A_1_8_1_3")
    smokingComment: Optional[str] = Field(default=None, alias="M_A_1_8_1_4")
    alcoholComment: Optional[str] = Field(default=None, alias="M_A_1_8_2_1")
    drugComment: Optional[str] = Field(default=None, alias="M_A_1_8_3_1")


# --- M.A.2 ---
class AntropometricData(BaseModel):
    measurementDate: str = Field(default="", alias="M_A_2_1")
    heightCm: float = Field(default=0, alias="M_A_2_2")
    weightKg: float = Field(default=0, alias="M_A_2_3")
    bmi: Optional[float] = Field(default=None, alias="M_A_2_4")
    bsa: Optional[float] = Field(default=None, alias="M_A_2_5")


# --- M.A.3 ---
class OverallPacientState(BaseModel):
    ecogStatus: Optional[int] = Field(default=None, alias="M_A_3_1_1")
    ecogDate: Optional[str] = Field(default=None, alias="M_A_3_1_2")

# @dataclass
# class MA32:
#     M_A_3_2_1: Optional[int] = None        # Karnofského index – 0 to 100
#     M_A_3_2_2: Optional[str] = None        # Datum hodnocení

# --- M.A.4 ---
class FertilityPreservationMeasures(BaseModel):
    measureType: str = Field(default="", alias="M_A_4_1")
    dateStarted: Optional[str] = Field(default=None, alias="M_A_4_2")
    storageLocation: Optional[str] = Field(default=None, alias="M_A_4_3")
    optionalComment: Optional[str] = Field(default=None, alias="M_A_4_4")


# --- M.A.1 ---
class RelevantFactors(BaseModel):
    tumorSyndrome: TumorSyndrome = Field(alias="M_A_1_1")
    familyHistory: Optional[OncoFamilyHistory] = Field(alias="M_A_1_2")
    relevantDisease: Optional[RelevantDisease] = Field(alias="M_A_1_3")
    previousCancer: Optional[PreviousOncologicalDisease] = Field(alias="M_A_1_5")
    screening: Optional[OncologicalScreening] = Field(alias="M_A_1_6")
    alergy: Optional[Alergy] = Field(alias="M_A_1_7")
    abusus: Optional[Abusus] = Field(alias="M_A_1_8")


# --- Modul A ---
class PacientParameters(BaseModel):
    relevantFactors: RelevantFactors = Field(alias="M_A_1")
    antropometricData: Optional[AntropometricData] = Field(alias="M_A_2")
    overallPacientState: Optional[OverallPacientState] = Field(alias="M_A_3")
    # M_A_3_2: Optional[List[MA32]] = field(default_factory=list)    #Opatření k zachování plodnosti před onkologickou léčbou TODO duplicate? error in template?
    fertilityPreservationMeasures: Optional[FertilityPreservationMeasures] = Field(alias="M_A_4")
