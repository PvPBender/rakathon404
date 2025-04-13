from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
from model.types import Gender

from model.patientTemplateModuleA import PacientParameters
from model.patientTemplateModuleB1 import DiagnosisB1
from model.patientTemplateModuleB2 import DiagnosisB2
# from model.patientTemplateModuleC import PacientTemplateModuleC as MC


class Identifier(BaseModel):
    typ: str  # Typ identifikátoru (např. rodné číslo, pas) TODO
    identifikator: str  # Identifikátor osoby


class PacientIdentification:  # Identifikace pacienta
    name: str = Field(alias="M.1.1.1")  # Povinné, 1..*
    surname: str = Field(alias="M.1.1.2")  # Povinné, 1..*
    dateOfBirth: date
    pacIdentifier: Identifier
    nationality: Optional[str] = None
    sex: Gender = Field(default_factory=list) 
    language: str = Field(default_factory=list)


class HealthInsurance:  # Zdravotní pojištění
    code: int = ""  # Kód zdravotní pojišťovny – Podmíněně povinné, 1..1
    name: str = ""  # Název zdravotní pojišťovny – Podmíněně povinné, 1..1
    id: str = Field(default_factory=list)  # Číslo zdravotního pojištění – Podmíněně povinné, 1..1 (0..1 dětská MDS)


class DocumentHeader:  # Hlavička dokumentu
    pacientIdentification: PacientIdentification = Field(alias="M_1_1")  # Identifikace pacienta – 1..1
    healthInsurance: HealthInsurance = Field(alias="M_1_2")  # Zdravotní pojištění – 1..1


class PacientTemplate:
    documentHeader: DocumentHeader = Field(alias="M_1")
    pacientParameters: PacientParameters = Field(alias="M_A")
    diagnosisB1: DiagnosisB1 = Field(alias="M_B_1")
    diagnosisB2: Optional[DiagnosisB2] = Field(alias="M_B_2")  # Optional list of MB2
    # M_C: Optional[List["MC"]] = field(default_factory=list)    # Optional list of MC
