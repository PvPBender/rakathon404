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


class PatientIdentification(BaseModel):  # M.1.1
    firstName: str = Field(alias="M.1.1.1")  # Křestní jméno (First name)
    lastName: str = Field(alias="M.1.1.2")  # Příjmení (Surname)
    dateOfBirth: date = Field(default=None, alias="M.1.1.3")  # Datum narození (Date of Birth)
    identifier: Identifier = Field(default=None, alias="M.1.1.4")  # Identifikátor pacienta
    nationality: Optional[str] = Field(default=None, alias="M.1.1.5")  # Státní občanství (Citizenship)
    gender: Optional[Gender] = Field(default=None, alias="M.1.1.6")  # Úřední pohlaví (Legal Gender)
    language: Optional[str] = Field(default=None, alias="M.1.1.7")  # Komunikační jazyk (Communication Language)


class HealthInsurance(BaseModel):  # M.1.2
    code: int = Field(alias="M.1.2.1")  # Kód zdravotní pojišťovny
    company: str = Field(alias="M.1.2.2")  # Název zdravotní pojišťovny
    insuranceNumber: str = Field(alias="M.1.2.3")  # Číslo zdravotního pojištění


class DocumentHeader:  # Hlavička dokumentu
    pacientIdentification: PacientIdentification = Field(alias="M_1_1")  # Identifikace pacienta – 1..1
    healthInsurance: HealthInsurance = Field(alias="M_1_2")  # Zdravotní pojištění – 1..1


class PacientTemplate:
    documentHeader: DocumentHeader = Field(alias="M_1")
    pacientParameters: PacientParameters = Field(alias="M_A")
    diagnosisB1: DiagnosisB1 = Field(alias="M_B_1")
    diagnosisB2: Optional[DiagnosisB2] = Field(alias="M_B_2")  # Optional list of MB2
    # M_C: Optional[List["MC"]] = field(default_factory=list)    # Optional list of MC
