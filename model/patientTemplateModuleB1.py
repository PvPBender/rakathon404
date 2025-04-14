from pydantic import BaseModel, Field
from typing import List, Optional
from model.types import Laterality, BiologicalBehaviour, tnmCounts, tnmCM, tnmCN, tnmCT, DiagnosticModalities, MetastasisLocation


class DiagnosisB1(BaseModel):
    diagnosisOrder: str = Field(alias="M_B_1_2_1")  # Pořadové číslo onkologické diagnózy
    diagnosisText: str = Field(alias="M_B_1_2_3")  # Diagnóza (slovně)
    diagnosisCode: str = Field(alias="M_B_1_2_4")  # Diagnóza – kód MKN
    laterality: Laterality = Field(alias="M_B_1_2_5")  # Lateralita
    topography: str = Field(alias="M_B_1_2_8")  # Topografie
    diagnosticGroup: str = Field(alias="M_B_1_4_1")  # Výběr diagnostické skupiny
    relapseDate: str = Field(alias="M_B_3_2_2")  # Datum relapsu/progrese
    relapseType: str = Field(alias="M_B_3_2_2_1")  # Typ relapsu

    # Optional fields
    sequenceNumber: Optional[int] = Field(default=None, alias="M_B_1_1")
    diagnosticModalities: Optional[List[DiagnosticModalities]] = Field(default=None, alias="M_B_1_2_2")
    morphologyText: Optional[str] = Field(default=None, alias="M_B_1_2_6")
    morphologyType: Optional[str] = Field(default=None, alias="M_B_1_2_7")
    combinedMorphology: Optional[str] = Field(default=None, alias="M_B_1_2_9")
    morphologyCode: Optional[str] = Field(default=None, alias="M_B_1_2_10")
    biologicalBehavior: Optional[BiologicalBehaviour] = Field(default=None, alias="M_B_1_2_11")
    grading: Optional[str] = Field(default=None, alias="M_B_1_2_12")
    mknoVersion: Optional[str] = Field(default=None, alias="M_B_1_2_13")
    diagnosisComment: Optional[str] = Field(default=None, alias="M_B_1_2_14")
    orphaCode: Optional[str] = Field(default=None, alias="M_B_1_2_15")

    # Clinical TNM
    cT: Optional[tnmCT] = Field(default=None, alias="M_B_1_3_1_1")
    frequency: Optional[tnmCounts] = Field(default=None, alias="M_B_1_3_1_2")
    cN: Optional[tnmCN] = Field(default=None, alias="M_B_1_3_1_3")
    cM: Optional[tnmCM] = Field(default=None, alias="M_B_1_3_1_4")

    # Pathological TNM
    pY: Optional[int] = Field(default=None, alias="M_B_1_3_2_1")
    pR: Optional[int] = Field(default=None, alias="M_B_1_3_2_2")
    pA: Optional[int] = Field(default=None, alias="M_B_1_3_2_3")
    pT: Optional[tnmCM] = Field(default=None, alias="M_B_1_3_2_4")
    pFrequency: Optional[tnmCounts] = Field(default=None, alias="M_B_1_3_2_5")
    pN: Optional[tnmCN] = Field(default=None, alias="M_B_1_3_2_6")
    pSn: Optional[str] = Field(default=None, alias="M_B_1_3_2_7")
    positiveSentinelNodes: Optional[int] = Field(default=None, alias="M_B_1_3_2_8")
    totalSentinelNodes: Optional[int] = Field(default=None, alias="M_B_1_3_2_9")
    positiveOtherNodes: Optional[int] = Field(default=None, alias="M_B_1_3_2_10")
    totalOtherNodes: Optional[int] = Field(default=None, alias="M_B_1_3_2_11")
    pM: Optional[tnmCM] = Field(default=None, alias="M_B_1_3_2_12")

    stage: Optional[str] = Field(default=None, alias="M_B_1_3_3")  # Stádium
    metastasisLocation: Optional[List[MetastasisLocation]] = Field(default=None, alias="M_B_1_3_4")  # Lokalizace metastáz
    metastasisComment: Optional[str] = Field(default=None, alias="M_B_1_3_4_1")
    lymphInvasion: Optional[str] = Field(default=None, alias="M_B_1_3_5")  # L
    venousInvasion: Optional[str] = Field(default=None, alias="M_B_1_3_6")  # V
    perineuralInvasion: Optional[str] = Field(default=None, alias="M_B_1_3_7")  # Pn
    classificationR: Optional[str] = Field(default=None, alias="M_B_1_3_8")  # R
    stagingInfo: Optional[str] = Field(default=None, alias="M_B_1_3_9")  # Staging - doplňující informace

    treatmentOngoing: Optional[bool] = Field(default=None, alias="M_B_3_2_1")  # Trvá léčebná odpověď
    additionalComment: Optional[str] = Field(default=None, alias="M_B_3_2_3")  # Volitelný komentář


class PacientTemplateModuleB1(BaseModel):
    diagnosisModuleB1: DiagnosisB1 = Field(alias="M_B_1")
    # diagnosisModuleB2Adult
