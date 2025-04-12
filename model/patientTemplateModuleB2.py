from dataclasses import dataclass
from typing import Optional
from datetime import date

###############################################################################
# NOTE TO THE READER:
# Below is a single Python file containing dataclasses for each cancer module
# M.B.2.X up to M.B.2.13, based on the specification you provided.
#
# Fields marked “Povinné, 1..1” or “Podmíněně povinné, 1..1” are represented as
# non-Optional, meaning you must supply a value when constructing the dataclass.
# Fields marked “Podmíněně povinné, 0..1” or “Volitelné, 0..1” are represented
# as Optional[…], defaulting to None.
#
# For each “výběr {…}” or code list, here we simply use str. In production,
# you might replace these with Enums for safety.
#
# Every data field has a brief comment with its meaning, cardinality, or extra
# notes taken from the original specification.
###############################################################################


###############################################################################
# M.B.2.1 – Nádory CNS
###############################################################################
@dataclass
class MB21:
    """
    M.B.2.1: Nádory CNS
    """

    # --------------- MOLEKULÁRNĚ-GENETICKÉ MARKERY ---------------
    # Multigenové vyšetření pomocí NGS – výběr {Provedeno, Neprovedeno, Údaj není k dispozici}, (1..1)
    M_B_2_1_2_1: str
    # Datum NGS vyšetření – (datum, 0..1)
    M_B_2_1_2_1_1: Optional[date] = None
    # Vyšetřovaná tkáň – (text, 0..1)
    M_B_2_1_2_1_2: Optional[str] = None
    # Výsledek NGS vyšetření – (text, 1..1)
    M_B_2_1_2_1_3: str = ""
    # Nádorová mutační zátěž (TMB) – (float, 0..1)
    M_B_2_1_2_1_4: Optional[float] = None

    # IDH (isocitrátdehydrogenáza) – (1..1, výběr {mutace, wild-type, ...})
    M_B_2_1_2_2: str = ""
    # kodelece 1p/19q – (1..1)
    M_B_2_1_2_3: str = ""
    # exprese ATRX – (1..1)
    M_B_2_1_2_4: str = ""
    # TERT gen – (1..1)
    M_B_2_1_2_5: str = ""
    # MGMT status – (1..1)
    M_B_2_1_2_6: str = ""
    # homozygotní delece CDKN2A/B – (1..1)
    M_B_2_1_2_7: str = ""
    # p53 gen – (1..1)
    M_B_2_1_2_8: str = ""
    # Jiné relevantní molekulárně-genetické nálezy – (text, 0..1)
    M_B_2_1_2_9: Optional[str] = None

    # --------------- KLASIFIKACE ---------------
    # Lokalizace postižení – (text, 1..1)
    M_B_2_1_3_1: str = ""
    # Histologické verifikace – (ANO/NE/Údaj není k dispozici, 1..1)
    M_B_2_1_3_2: str = ""
    # Typ tumoru dle WHO klasifikace (5 ed.) – (1..1)
    M_B_2_1_3_3: str = ""
    # Subtyp tumoru dle WHO klasifikace (5 ed.) – (0..1)
    M_B_2_1_3_3_1: Optional[str] = None
    # Doplňující informace – (text, 0..1)
    M_B_2_1_3_3_2: Optional[str] = None

    # --------------- RIZIKOVÉ FAKTORY ---------------
    # Radiačně indukované tumory – (ANO/NE/Údaj není k dispozici, 1..1)
    M_B_2_1_4_1: str = ""
    # Dědičné predispoziční syndromy – (výběr, 0..1)
    M_B_2_1_4_2: Optional[str] = None
    # Jiný predispoziční syndrom – (text, 1..1 if “jiný”, else 0..1 overall)
    M_B_2_1_4_2_1: Optional[str] = None


###############################################################################
# M.B.2.2 – Nádory hlavy a krku
###############################################################################
@dataclass
class MB22:
    """
    M.B.2.2: Nádory hlavy a krku
    """

    # --------------- MOLEKULÁRNĚ-GENETICKÉ MARKERY ---------------
    # Multigenové vyšetření pomocí NGS – (1..1)
    M_B_2_2_2_1: str
    # Datum NGS vyšetření – (datum, 0..1)
    M_B_2_2_2_1_1: Optional[date] = None
    # Vyšetřovaná tkáň – (text, 0..1)
    M_B_2_2_2_1_2: Optional[str] = None
    # Výsledek NGS vyšetření – (text, 1..1)
    M_B_2_2_2_1_3: str = ""
    # Nádorová mutační zátěž (TMB) – (float, 0..1)
    M_B_2_2_2_1_4: Optional[float] = None

    # HER2 exprese – (1..1)
    M_B_2_2_2_2: str = ""
    # AR (androgenový receptor) – (1..1)
    M_B_2_2_2_3: str = ""
    # NTRK fúze – (1..1)
    M_B_2_2_2_4: str = ""
    # BRAFV600 – (1..1)
    M_B_2_2_2_5: str = ""
    # RET fúze – (1..1)
    M_B_2_2_2_6: str = ""
    # RET fúze - typ – (text, 0..1; only if RET is "Pozitivní")
    M_B_2_2_2_6_1: Optional[str] = None
    # PD-L1 exprese (CPS) – (float, 0..1)
    M_B_2_2_2_7: Optional[float] = None
    # MSI-H – (1..1)
    M_B_2_2_2_8: str = ""
    # p16 (HPV) – (1..1)
    M_B_2_2_2_9: str = ""
    # EBV DNA copy number – (float, 0..1)
    M_B_2_2_2_10: Optional[float] = None
    # Jiné relevantní molekulárně-genetické nálezy – (text, 0..1)
    M_B_2_2_2_11: Optional[str] = None

    # --------------- RIZIKOVÉ FAKTORY ---------------
    # EBV – (ANO/NE/Údaj není k dispozici, 1..1)
    M_B_2_2_4_1: str = ""
    # HPV – (ANO/NE/Údaj není k dispozici, 1..1)
    M_B_2_2_4_2: str = ""
    # Kouření – (výběr, 1..1)
    M_B_2_2_4_3: str = ""
    # Počet balíčkoroků – (float, 0..1)
    M_B_2_2_4_3_1: Optional[float] = None
    # Alkohol – (výběr, 1..1)
    M_B_2_2_4_4: str = ""


###############################################################################
# M.B.2.3 – Nádory respiračního systému a mediastina
###############################################################################
@dataclass
class MB23:
    """
    M.B.2.3: Nádory respiračního systému a mediastina
    """

    # --------------- LABORATORNÍ MARKERY ---------------
    # CEA – (float, 0..1)
    M_B_2_3_1_1: Optional[float] = None
    # CYFRA 21-1 – (float, 0..1)
    M_B_2_3_1_2: Optional[float] = None
    # NSE – (float, 0..1)
    M_B_2_3_1_3: Optional[float] = None
    # chromogranin A – (float, 0..1)
    M_B_2_3_1_4: Optional[float] = None
    # SCCA – (float, 0..1)
    M_B_2_3_1_5: Optional[float] = None

    # --------------- MOLEKULÁRNĚ-GENETICKÉ MARKERY ---------------
    # NGS – (1..1)
    M_B_2_3_2_1: str
    # Datum NGS – (date, 0..1)
    M_B_2_3_2_1_1: Optional[date] = None
    # Vyšetřovaná tkáň – (text, 0..1)
    M_B_2_3_2_1_2: Optional[str] = None
    # Výsledek NGS – (text, 1..1)
    M_B_2_3_2_1_3: str = ""
    # TMB – (float, 0..1)
    M_B_2_3_2_1_4: Optional[float] = None

    # alterace EGFR genu – (1..1)
    M_B_2_3_2_2: str = ""
    # EGFR - typ mutace – (text, 0..1)
    M_B_2_3_2_2_1: Optional[str] = None

    # alterace ALK genu – (1..1)
    M_B_2_3_2_3: str = ""
    # ALK - typ mutace – (text, 0..1)
    M_B_2_3_2_3_1: Optional[str] = None

    # alterace ROS1 genu – (1..1)
    M_B_2_3_2_4: str = ""
    # ROS1 - typ mutace – (text, 0..1)
    M_B_2_3_2_4_1: Optional[str] = None

    # alterace KRAS genu – (1..1)
    M_B_2_3_2_5: str = ""
    # KRAS - typ mutace – (text, 0..1)
    M_B_2_3_2_5_1: Optional[str] = None

    # BRAF – (1..1)
    M_B_2_3_2_6: str = ""
    # BRAF - typ mutace – (text, 0..1)
    M_B_2_3_2_6_1: Optional[str] = None

    # RET fúze – (1..1)
    M_B_2_3_2_7: str = ""
    # RET fúze - typ – (text, 0..1)
    M_B_2_3_2_7_1: Optional[str] = None

    # NTRK fúze – (1..1)
    M_B_2_3_2_8: str = ""
    # HER2 exprese – (1..1)
    M_B_2_3_2_9: str = ""
    # alterace MET genu – (1..1)
    M_B_2_3_2_10: str = ""
    # PD-L1 exprese – (1..1)
    M_B_2_3_2_11: str = ""
    # Jiné relevantní molekulárně-genetické nálezy – (text, 0..1)
    M_B_2_3_2_12: Optional[str] = None

    # --------------- RIZIKOVÉ FAKTORY ---------------
    # Kouření – (1..1)
    M_B_2_3_4_1: str = ""
    # Počet balíčkoroků – (float, 0..1)
    M_B_2_3_4_1_1: Optional[float] = None


###############################################################################
# M.B.2.4 – Nádory GIT (karcinom jícnu)
###############################################################################
@dataclass
class MB24:
    """
    M.B.2.4: Karcinom jícnu
    """

    # --------------- LABORATORNÍ MARKERY ---------------
    # CEA (ug/l) – (float, 0..1)
    M_B_2_4_1_1: Optional[float] = None
    # CA 72-4 – (float, 0..1)
    M_B_2_4_1_2: Optional[float] = None
    # CA 19-9 (kU/l) – (float, 0..1)
    M_B_2_4_1_3: Optional[float] = None

    # --------------- MOLEKULÁRNĚ-GENETICKÉ MARKERY ---------------
    # NGS – (1..1)
    M_B_2_4_2_1: str
    # Datum NGS – (date, 0..1)
    M_B_2_4_2_1_1: Optional[date] = None
    # Vyšetřovaná tkáň – (0..1)
    M_B_2_4_2_1_2: Optional[str] = None
    # Výsledek NGS – (1..1)
    M_B_2_4_2_1_3: str = ""
    # TMB – (float, 0..1, Volitelné)
    M_B_2_4_2_1_4: Optional[float] = None

    # HER2 exprese – (1..1)
    M_B_2_4_2_2: str = ""
    # PD-L1 exprese – (1..1)
    M_B_2_4_2_3: str = ""
    # MMR/MSI – (1..1)
    M_B_2_4_2_4: str = ""
    # BRAF – (1..1)
    M_B_2_4_2_4_1: str = ""
    # BRAF - typ mutace – (text, 0..1)
    M_B_2_4_2_4_1_1: Optional[str] = None
    # NTRK fúze – (1..1)
    M_B_2_4_2_5: str = ""
    # RET fúze – (1..1)
    M_B_2_4_2_6: str = ""
    # RET fúze - typ – (text, 0..1)
    M_B_2_4_2_6_1: Optional[str] = None
    # Jiné relevantní nálezy – (text, 0..1)
    M_B_2_4_2_7: Optional[str] = None

    # --------------- RIZIKOVÉ FAKTORY ---------------
    # Toxonutritivní etiologie – (1..1)
    M_B_2_4_4_1: str = ""
    # Barettův jícen – (1..1)
    M_B_2_4_4_2: str = ""
    # Refluxní choroba – (1..1)
    M_B_2_4_4_3: str = ""


###############################################################################
# M.B.2.5 – Nádory GIT (karcinom žaludku a gastroezofageální junkce)
###############################################################################
@dataclass
class MB25:
    """
    M.B.2.5: Karcinom žaludku / gastroezofageální junkce
    """

    # --------------- LABORATORNÍ MARKERY ---------------
    # CEA [ug/l] – (float, 0..1)
    M_B_2_5_1_1: Optional[float] = None
    # CA 72-4 [jednotka] – (float, 0..1)
    M_B_2_5_1_2: Optional[float] = None
    # CA 19-9 [kU/l] – (float, 0..1)
    M_B_2_5_1_3: Optional[float] = None

    # --------------- MOLEKULÁRNĚ-GENETICKÉ MARKERY ---------------
    M_B_2_5_2_1: str
    M_B_2_5_2_1_1: Optional[date] = None
    M_B_2_5_2_1_2: Optional[str] = None
    M_B_2_5_2_1_3: str = ""
    M_B_2_5_2_1_4: Optional[float] = None

    # HER2 exprese – (1..1)
    M_B_2_5_2_2: str = ""
    # PD-L1 exprese – (1..1)
    M_B_2_5_2_3: str = ""
    # MMR/MSI – (1..1)
    M_B_2_5_2_4: str = ""
    # BRAF – (1..1)
    M_B_2_5_2_5: str = ""
    # BRAF - typ mutace – (text, 0..1)
    M_B_2_5_2_5_1: Optional[str] = None
    # NTRK fúze – (1..1)
    M_B_2_5_2_6: str = ""
    # RET fúze – (1..1)
    M_B_2_5_2_7: str = ""
    # RET fúze - typ – (0..1)
    M_B_2_5_2_7_1: Optional[str] = None
    # Jiné relevantní molekulárně-genetické nálezy – (text, 0..1)
    M_B_2_5_2_5_: Optional[str] = None  # (typo in original doc: "2.5.2.5 Jiné...")

    # --------------- RIZIKOVÉ FAKTORY ---------------
    # Toxonutritivní etiologie – (1..1)
    M_B_2_5_4_1: str = ""
    # Helicobacter pylori – (1..1)
    M_B_2_5_4_2: str = ""
    # Perniciózní anémie – (1..1)
    M_B_2_5_4_3: str = ""
    # Dědičné predispoziční syndromy – (0..1)
    M_B_2_5_4_4: Optional[str] = None
    # Jiný predispoziční syndrom – (1..1 if “jiný”)
    M_B_2_5_4_4_1: Optional[str] = None


###############################################################################
# M.B.2.6 – Nádory GIT (Kolorektální karcinom)
###############################################################################
@dataclass
class MB26:
    """
    M.B.2.6: Kolorektální karcinom
    """

    # --------------- LABORATORNÍ MARKERY ---------------
    # CEA [ug/l] – (float, 0..1)
    M_B_2_6_1_1: Optional[float] = None
    # CA 19-9 [kU/l] – (float, 0..1)
    M_B_2_6_1_2: Optional[float] = None
    # DPD deficience – (1..1)
    M_B_2_6_1_3: str = ""

    # --------------- MOLEKULÁRNĚ-GENETICKÉ MARKERY ---------------
    M_B_2_6_2_1: str
    M_B_2_6_2_1_1: Optional[date] = None
    M_B_2_6_2_1_2: Optional[str] = None
    M_B_2_6_2_1_3: str = ""
    M_B_2_6_2_1_4: Optional[float] = None

    # MMR/MSI – (1..1)
    M_B_2_6_2_2: str = ""
    # alterace KRAS – (1..1)
    M_B_2_6_2_3: str = ""
    # KRAS - typ – (0..1)
    M_B_2_6_2_3_1: Optional[str] = None
    # alterace NRAS – (1..1)
    M_B_2_6_2_4: str = ""
    # NRAS - typ – (0..1)
    M_B_2_6_2_4_1: Optional[str] = None
    # BRAF – (1..1)
    M_B_2_6_2_5: str = ""
    # BRAF - typ – (0..1)
    M_B_2_6_2_5_1: Optional[str] = None
    # HER2 exprese – (1..1)
    M_B_2_6_2_6: str = ""
    # NTRK fúze – (1..1)
    M_B_2_6_2_7: str = ""
    # RET fúze – (1..1)
    M_B_2_6_2_8: str = ""
    # RET fúze - typ – (0..1)
    M_B_2_6_2_8_1: Optional[str] = None
    # patogenní alterace POLE/POLD1 – (1..1)
    M_B_2_6_2_9: str = ""
    # POLE/POLD1 - typ mutace – (0..1)
    M_B_2_6_2_10: Optional[str] = None
    # Jiné relevantní nálezy – (0..1)
    M_B_2_6_2_11: Optional[str] = None

    # --------------- RIZIKOVÉ FAKTORY ---------------
    # Tumor deposits/tumor budding – (1..1)
    M_B_2_6_4_1: str = ""
    # Střevní adenom(y) – (1..1)
    M_B_2_6_4_2: str = ""
    # Ulcerosní kolitida – (1..1)
    M_B_2_6_4_3: str = ""
    # Crohnova choroba – (1..1) but doc says 1..2? Probably a doc nuance. We'll treat as 1..1 here.
    M_B_2_6_4_4: str = ""
    # CRC nebo adenomy (v RA) – (1..1)
    M_B_2_6_4_5: str = ""
    # Dědičné predispoziční syndromy – (0..1)
    M_B_2_6_4_6: Optional[str] = None
    # Jiný predispoziční syndrom – (0..1 if “jiný”)
    M_B_2_6_4_6_1: Optional[str] = None


###############################################################################
# M.B.2.7 – Nádory GIT (Anální karcinom)
###############################################################################
@dataclass
class MB27_Anal:
    """
    M.B.2.7: Anální karcinom
    """

    # --------------- LABORATORNÍ MARKERY ---------------
    # SCCA (jednotka) – (float, 0..1)
    M_B_2_7_1_1: Optional[float] = None
    # DPD deficience – (1..1)
    M_B_2_7_1_2: str = ""

    # --------------- MOLEKULÁRNĚ-GENETICKÉ MARKERY ---------------
    M_B_2_7_2_1: str
    M_B_2_7_2_1_1: Optional[date] = None
    M_B_2_7_2_1_2: Optional[str] = None
    M_B_2_7_2_1_3: str = ""
    M_B_2_7_2_1_4: Optional[float] = None

    # MMR/MSI – (1..1)
    M_B_2_7_2_2: str = ""
    # NTRK fúze – (1..1)
    M_B_2_7_2_3: str = ""
    # Jiné relevantní nálezy – (0..1)
    M_B_2_7_2_4: Optional[str] = None

    # --------------- RIZIKOVÉ FAKTORY ---------------
    # HPV – (1..1)
    M_B_2_7_4_1: str = ""
    # HIV – (1..1)
    M_B_2_7_4_2: str = ""


###############################################################################
# M.B.2.7 – Nádory GIT (Karcinom pankreatu) – (the specification reuses “2.7”)
###############################################################################
@dataclass
class MB27_Pankreas:
    """
    M.B.2.7: Karcinom pankreatu (duplicate numbering in the doc)
    """

    # --------------- LABORATORNÍ MARKERY ---------------
    # CA 19-9 [kU/l] – (float, 0..1)
    M_B_2_7_pan_1: Optional[float] = None
    # CEA [ug/l] – (float, 0..1)
    M_B_2_7_pan_2: Optional[float] = None

    # --------------- MOLEKULÁRNĚ-GENETICKÉ MARKERY ---------------
    M_B_2_7_pan_2_1: str
    M_B_2_7_pan_2_1_1: Optional[date] = None
    M_B_2_7_pan_2_1_2: Optional[str] = None
    M_B_2_7_pan_2_1_3: str = ""
    M_B_2_7_pan_2_1_4: Optional[float] = None

    # MMR/MSI – (1..1)
    M_B_2_7_pan_2_2: str = ""
    # HER2 exprese – (1..1)
    M_B_2_7_pan_2_3: str = ""
    # alterace ALK genu – (1..1)
    M_B_2_7_pan_2_4: str = ""
    M_B_2_7_pan_2_4_1: Optional[str] = None  # typ mutace
    # alterace ROS1 genu – (1..1)
    M_B_2_7_pan_2_5: str = ""
    M_B_2_7_pan_2_5_1: Optional[str] = None
    # NRG1 fúze – (1..1)
    M_B_2_7_pan_2_6: str = ""
    # alterace FGFR2 genu – (1..1)
    M_B_2_7_pan_2_7: str = ""
    M_B_2_7_pan_2_7_1: Optional[str] = None
    # NTRK fúze – (1..1)
    M_B_2_7_pan_2_8: str = ""
    # RET fúze – (1..1)
    M_B_2_7_pan_2_9: str = ""
    M_B_2_7_pan_2_9_1: Optional[str] = None
    # alterace BRAF genu – (1..1)
    M_B_2_7_pan_2_10: str = ""
    M_B_2_7_pan_2_10_1: Optional[str] = None
    # alterace KRAS genu – (1..1)
    M_B_2_7_pan_2_11: str = ""
    M_B_2_7_pan_2_11_1: Optional[str] = None
    # alterace PALB2 genu – (1..1)
    M_B_2_7_pan_2_12: str = ""
    # alterace NRG1 genu – (1..1)
    M_B_2_7_pan_2_13: str = ""
    # BRCA1 mutace – (1..1)
    M_B_2_7_pan_2_14: str = ""
    # BRCA2 mutace – (1..1)
    M_B_2_7_pan_2_15: str = ""
    # Jiné relevantní molekulárně-genetické nálezy – (0..1)
    M_B_2_7_pan_2_16: Optional[str] = None

    # --------------- RIZIKOVÉ FAKTORY ---------------
    # Dědičné predispoziční syndromy – (0..1)
    M_B_2_7_pan_4_1: Optional[str] = None
    # Jiný predispoziční syndrom – (0..1)
    M_B_2_7_pan_4_1_1: Optional[str] = None
    # Chronická pankreatitida – (1..1)
    M_B_2_7_pan_4_2: str = ""
    # Pozitivní rodinná anamnéza – (1..1)
    M_B_2_7_pan_4_3: str = ""


###############################################################################
# M.B.2.8 – Nádory GIT (Karcinom jater)
###############################################################################
@dataclass
class MB28:
    """
    M.B.2.8: Karcinom jater
    """

    # --------------- LABORATORNÍ MARKERY ---------------
    # AFP [kU/L] – (float, 0..1)
    M_B_2_8_1_1: Optional[float] = None

    # --------------- MOLEKULÁRNĚ-GENETICKÉ MARKERY ---------------
    M_B_2_8_2_1: str
    M_B_2_8_2_1_1: Optional[date] = None
    M_B_2_8_2_1_2: Optional[str] = None
    M_B_2_8_2_1_3: str = ""
    M_B_2_8_2_1_4: Optional[float] = None

    # --------------- RIZIKOVÉ FAKTORY ---------------
    # Child-Pugh skóre – (0..1, výběr {A,B,C})
    M_B_2_8_4_1: Optional[str] = None
    # Jaterní cirhosa – (1..1)
    M_B_2_8_4_2: str = ""
    # Infekční hepatitida – (1..1)
    M_B_2_8_4_3: str = ""
    # Typ hepatitidy – (1..1 if above = "ANO")
    M_B_2_8_4_3_1: Optional[str] = None


###############################################################################
# M.B.2.9 – Nádory GIT (Karcinom žlučníku a žluč.cest)
###############################################################################
@dataclass
class MB29:
    """
    M.B.2.9: Karcinom žlučníku / žlučových cest
    """

    # --------------- LABORATORNÍ MARKERY ---------------
    # CEA [ug/l] – (float, 0..1)
    M_B_2_9_1_1: Optional[float] = None
    # CA 19-9 [jednotka] – (float, 0..1)
    M_B_2_9_1_2: Optional[float] = None

    # --------------- MOLEKULÁRNĚ-GENETICKÉ MARKERY ---------------
    M_B_2_9_2_1: str
    M_B_2_9_2_1_1: Optional[date] = None
    M_B_2_9_2_1_2: Optional[str] = None
    M_B_2_9_2_1_3: str = ""
    M_B_2_9_2_1_4: Optional[float] = None

    # alterace FGFR2 – (1..1)
    M_B_2_9_2_2: str = ""
    # FGFR2 - typ mutace – (0..1)
    M_B_2_9_2_2_1: Optional[str] = None
    # IDH mutace – (1..1)
    M_B_2_9_2_3: str = ""
    # HER2 exprese – (1..1)
    M_B_2_9_2_4: str = ""
    # alterace BRAF – (1..1)
    M_B_2_9_2_5: str = ""
    # BRAF - typ mutace – (0..1)
    M_B_2_9_2_5_1: Optional[str] = None
    # NTRK fúze – (1..1)
    M_B_2_9_2_6: str = ""
    # MMR/MSI – (1..1)
    M_B_2_9_2_7: str = ""
    # Jiné relevantní nálezy – (0..1)
    M_B_2_9_2_8: Optional[str] = None


###############################################################################
# M.B.2.10 – Karcinom prsu
###############################################################################
@dataclass
class MB210:
    """
    M.B.2.10: Karcinom prsu
    """

    # --------------- LABORATORNÍ MARKERY ---------------
    # CEA (jednotka) – (float, 0..1)
    M_B_2_10_1_1: Optional[float] = None
    # CA 15-3 (jednotka) – (float, 0..1)
    M_B_2_10_1_2: Optional[float] = None

    # --------------- MOLEKULÁRNĚ-GENETICKÉ MARKERY ---------------
    M_B_2_10_2_1: str
    M_B_2_10_2_1_1: Optional[date] = None
    M_B_2_10_2_1_2: Optional[str] = None
    M_B_2_10_2_1_3: str = ""
    M_B_2_10_2_1_4: Optional[float] = None

    # ER – (1..1)
    M_B_2_10_2_2: str = ""
    # PR – (1..1)
    M_B_2_10_2_3: str = ""
    # Proliferace Ki67 – (1..1)
    M_B_2_10_2_4: str = ""
    # HER2 exprese – (1..1)
    M_B_2_10_2_5: str = ""
    # BRCA1 mutace – (1..1)
    M_B_2_10_2_6: str = ""
    # BRCA2 mutace – (1..1)
    M_B_2_10_2_7: str = ""
    # mutace PIK3CA – (1..1)
    M_B_2_10_2_8: str = ""
    # Jiné relevantní nálezy – (0..1)
    M_B_2_10_2_9: Optional[str] = None


###############################################################################
# M.B.2.11 – Gynekologické nádory (čípek a hrdlo děložní)
###############################################################################
@dataclass
class MB211:
    """
    M.B.2.11: Ca čípku a hrdla děložního
    """

    # --------------- LABORATORNÍ MARKERY ---------------
    # CYFRA (ug/l) – (float, 0..1)
    M_B_2_11_1_1: Optional[float] = None
    # SCC (ug/l) – (float, 0..1)
    M_B_2_11_1_2: Optional[float] = None
    # CA 125 (kU/l) – (float, 0..1)
    M_B_2_11_1_3: Optional[float] = None
    # HE4 (pmol/l) – (float, 0..1)
    M_B_2_11_1_4: Optional[float] = None
    # Ca 19-9 (kU/l) – (float, 0..1)
    M_B_2_11_1_5: Optional[float] = None

    # --------------- MOLEKULÁRNĚ-GENETICKÉ MARKERY ---------------
    M_B_2_11_2_1: str
    M_B_2_11_2_1_1: Optional[date] = None
    M_B_2_11_2_1_2: Optional[str] = None
    M_B_2_11_2_1_3: str = ""
    M_B_2_11_2_1_4: Optional[float] = None

    # p53 gen – (1..1)
    M_B_2_11_2_2: str = ""
    # PD-L1 exprese – (1..1)
    M_B_2_11_2_3: str = ""
    # p16 (HPV) – (1..1)
    M_B_2_11_2_4: str = ""
    # Jiné relevantní nálezy – (0..1)
    M_B_2_11_2_5: Optional[str] = None

    # --------------- KLASIFIKACE ---------------
    # FIGO staging – (Povinné 1..1), subfields only if "Ano"
    M_B_2_11_3_1: str = ""  # "ANO/NE"
    # FIGO – (1..1 if above=Ano)
    M_B_2_11_3_1_1: Optional[str] = None
    # FIGO - dovětek – (0..1)
    M_B_2_11_3_1_2: Optional[str] = None

    # --------------- RIZIKOVÉ FAKTORY ---------------
    # Kouření – (1..1)
    M_B_2_11_4_1: str = ""
    # Počet balíčkoroků – (0..1)
    M_B_2_11_4_2: Optional[float] = None
    # Hloubka stromální invaze – (float, 0..1)
    M_B_2_11_4_3: Optional[float] = None


###############################################################################
# M.B.2.12 – Gynekologické nádory (tělo děložní)
###############################################################################
@dataclass
class MB212:
    """
    M.B.2.12: Ca těla děložního
    """

    # --------------- LABORATORNÍ MARKERY ---------------
    # CA 125 (kU/l) – (float, 0..1)
    M_B_2_12_1_1: Optional[float] = None
    # HE4 (pmol/l) – (float, 0..1)
    M_B_2_12_1_2: Optional[float] = None

    # --------------- MOLEKULÁRNĚ-GENETICKÉ MARKERY ---------------
    M_B_2_12_2_1: str
    M_B_2_12_2_1_1: Optional[date] = None
    M_B_2_12_2_1_2: Optional[str] = None
    M_B_2_12_2_1_3: str = ""
    M_B_2_12_2_1_4: Optional[float] = None

    # HER2 exprese – (1..1)
    M_B_2_12_2_2: str = ""
    # MMR/MSI – (1..1)
    M_B_2_12_2_3: str = ""
    # ER – (1..1)
    M_B_2_12_2_4: str = ""
    # PR – (1..1)
    M_B_2_12_2_5: str = ""
    # p53 gen – (1..1)
    M_B_2_12_2_6: str = ""
    # patogenní alterace POLE/POLD1 – (1..1)
    M_B_2_12_2_7: str = ""
    M_B_2_12_2_7_1: Optional[str] = None
    # Jiné relevantní nálezy – (0..1)
    M_B_2_12_2_8: Optional[str] = None

    # --------------- KLASIFIKACE ---------------
    # FIGO staging – (1..1, “ANO/NE”)
    M_B_2_12_3_1: str = ""
    # FIGO – (1..1 if above=Ano)
    M_B_2_12_3_1_1: Optional[str] = None
    # FIGO - dovětek – (0..1)
    M_B_2_12_3_1_2: Optional[str] = None

    # --------------- RIZIKOVÉ FAKTORY ---------------
    # Histologický typ – (0..1)
    M_B_2_12_4_1: Optional[str] = None
    # Invaze myometria – (1..1)
    M_B_2_12_4_2: str = ""
    # Lymfoangioinvaze (LVSI) – (1..1)
    M_B_2_12_4_3: str = ""
    # Obezita – (1..1)
    M_B_2_12_4_4: str = ""
    # Diabetes II.typu – (1..1)
    M_B_2_12_4_5: str = ""
    # Lynchův syndrom – (1..1)
    M_B_2_12_4_6: str = ""


###############################################################################
# M.B.2.13 – Gynekologické nádory (ovaria)
###############################################################################
@dataclass
class MB213:
    """
    M.B.2.13: Nádory ovaria
    """

    # --------------- LABORATORNÍ MARKERY ---------------
    # CEA [ug/l] – (float, 0..1)
    M_B_2_13_1_1: Optional[float] = None
    # CA 125 [kU/l] – (float, 0..1)
    M_B_2_13_1_2: Optional[float] = None
    # CA 19-9 [kU/l] – (float, 0..1)
    M_B_2_13_1_3: Optional[float] = None
    # HE4 [pmol/l] – (float, 0..1)
    M_B_2_13_1_4: Optional[float] = None

    # --------------- MOLEKULÁRNĚ-GENETICKÉ MARKERY ---------------
    M_B_2_13_2_1: str
    M_B_2_13_2_1_1: Optional[date] = None
    M_B_2_13_2_1_2: Optional[str] = None
    M_B_2_13_2_1_3: str = ""
    M_B_2_13_2_1_4: Optional[float] = None

    # BRCA1 mutace – (1..1)
    M_B_2_13_2_2: str = ""
    # BRCA2 mutace – (1..1)
    M_B_2_13_2_3: str = ""
    # HRD status – (1..1)
    M_B_2_13_2_4: str = ""
    # alterace KRAS genu – (1..1)
    M_B_2_13_2_5: str = ""
    M_B_2_13_2_5_1: Optional[str] = None
    # alterace BRAF genu – (1..1)
    M_B_2_13_2_6: str = ""
    M_B_2_13_2_6_1: Optional[str] = None
    # HER2 exprese – (1..1)
    M_B_2_13_2_7: str = ""
    # Jiné relevantní nálezy – (0..1)
    M_B_2_13_2_8: Optional[str] = None

    # --------------- KLASIFIKACE ---------------
    # FIGO staging – (1..1, “ANO/NE”)
    M_B_2_13_3_1: str = ""
    # FIGO – (1..1 if above=Ano)
    M_B_2_13_3_1_1: Optional[str] = None
    # FIGO - dovětek – (0..1)
    M_B_2_13_3_1_2: Optional[str] = None

    # --------------- RIZIKOVÉ FAKTORY ---------------
    # Lynchův syndrom – (not fully specified in truncated snippet; presumably 0..1 or 1..1)
    # The doc line was cut off, so we treat it as 1..1.
    M_B_2_13_4_1: str = ""
    M_B_2_13_4_2: str = ""
    M_B_2_13_4_2_1: str = ""


###############################################################################
# M.B.2.14 – Gynekologické nádory (zevní rodidla)
###############################################################################
@dataclass
class MB214:
    """
    M.B.2.14: Gynekologické nádory (zevní rodidla)
    """

    # --------------- LABORATORNÍ MARKERY ---------------
    # CEA – (float, 0..1)
    M_B_2_14_1_1: Optional[float] = None
    # CYFRA (ug/l) – (float, 0..1)
    M_B_2_14_1_2: Optional[float] = None
    # SCC (ug/l) – (float, 0..1)
    M_B_2_14_1_3: Optional[float] = None

    # --------------- MOLEKULÁRNĚ-GENETICKÉ MARKERY ---------------
    # NGS – (1..1)
    M_B_2_14_2_1: str
    # Datum NGS vyšetření – (date, 0..1)
    M_B_2_14_2_1_1: Optional[date] = None
    # Vyšetřovaná tkáň – (text, 0..1)
    M_B_2_14_2_1_2: Optional[str] = None
    # Výsledek NGS vyšetření – (text, 1..1)
    M_B_2_14_2_1_3: str = ""
    # Nádorová mutační zátěž (TMB) – (float, 0..1)
    M_B_2_14_2_1_4: Optional[float] = None

    # PD-L1 exprese – (1..1)
    M_B_2_14_2_2: str = ""
    # p53 gen – (1..1)
    M_B_2_14_2_3: str = ""
    # p16 (HPV) – (1..1)
    M_B_2_14_2_4: str = ""
    # Jiné relevantní molekulárně-genetické nálezy – (text, 0..1)
    M_B_2_14_2_5: Optional[str] = None

    # --------------- KLASIFIKACE ---------------
    # FIGO staging – (Povinné, "ANO/NE")
    M_B_2_14_3_1: str = ""
    # FIGO – (1..1 if above=Ano)
    M_B_2_14_3_2: Optional[str] = None
    # FIGO - dovětek – (0..1)
    M_B_2_14_3_3: Optional[str] = None

    # --------------- RIZIKOVÉ FAKTORY ---------------
    # Kouření – (výběr, Povinné)
    M_B_2_14_4_1: str = ""
    # Počet balíčkoroků – (float, 0..1)
    M_B_2_14_4_1_1: Optional[float] = None
    # Dermatóza (v OA) – (1..1)
    M_B_2_14_4_2: str = ""


###############################################################################
# M.B.2.15 – Renální karcinom
###############################################################################
@dataclass
class MB215:
    """
    M.B.2.15: Renální karcinom
    """

    # --------------- LABORATORNÍ MARKERY ---------------
    # (No explicit numeric markers here, or it's not provided in snippet.
    #  We only see references to the next block.)

    # --------------- MOLEKULÁRNĚ-GENETICKÉ MARKERY ---------------
    # NGS – (1..1)
    M_B_2_15_2_1: str
    # Datum NGS vyšetření – (date, 0..1)
    M_B_2_15_2_1_1: Optional[date] = None
    # Vyšetřovaná tkáň – (text, 0..1)
    M_B_2_15_2_1_2: Optional[str] = None
    # Výsledek NGS vyšetření – (text, 1..1)
    M_B_2_15_2_1_3: str = ""
    # Nádorová mutační zátěž (TMB) – (float, 0..1)
    M_B_2_15_2_1_4: Optional[float] = None

    # Relevantní molekulárně-genetické nálezy – (text, 0..1)
    M_B_2_15_2_2: Optional[str] = None

    # --------------- RIZIKOVÉ FAKTORY ---------------
    # IMDC rizikové skóre – (výběr {nízké, střední, vysoké}, 1..1)
    M_B_2_15_4_1: str = ""
    # Dědičné predispoziční syndromy – (0..1)
    M_B_2_15_4_2: Optional[str] = None
    # Jiný predispoziční syndrom – (0..1 if “jiný”)
    M_B_2_15_4_3: Optional[str] = None
    # Obezita – (1..1)
    M_B_2_15_4_4: str = ""
    # Arteriální hypertenze – (1..1)
    M_B_2_15_4_5: str = ""
    # Léčba arteriální hypertenze – (1..1)
    M_B_2_15_4_6: str = ""
    # Kouření – (1..1, e.g. {Aktivní, Bývalý, ...})
    M_B_2_15_4_7: str = ""
    # Počet balíčkoroků – (float, 0..1)
    M_B_2_15_4_8: Optional[float] = None


###############################################################################
# M.B.2.16 – Karcinom močového měchýře a močových cest
###############################################################################
@dataclass
class MB216:
    """
    M.B.2.16: Karcinom močového měchýře a močových cest
    """

    # --------------- LABORATORNÍ MARKERY ---------------
    # (Not explicitly listed beyond headings in the snippet)

    # --------------- MOLEKULÁRNĚ-GENETICKÉ MARKERY ---------------
    # NGS – (1..1)
    M_B_2_16_2_1: str
    # Datum NGS – (date, 0..1)
    M_B_2_16_2_1_1: Optional[date] = None
    # Vyšetřovaná tkáň – (text, 0..1)
    M_B_2_16_2_1_2: Optional[str] = None
    # Výsledek NGS – (text, 1..1)
    M_B_2_16_2_1_3: str = ""
    # Nádorová mutační zátěž (TMB) – (float, 0..1)
    M_B_2_16_2_1_4: Optional[float] = None

    # PD-L1 exprese – (1..1)
    M_B_2_16_2_2: str = ""
    # PD-L1 exprese (CPS) – (float, 0..1)
    M_B_2_16_2_2_1: Optional[float] = None
    # PD-L1 exprese (TPS) – (float, 0..1)
    M_B_2_16_2_2_2: Optional[float] = None

    # alterace FGFR2 genu – (1..1)
    M_B_2_16_2_3: str = ""
    M_B_2_16_2_3_1: Optional[str] = None
    # alterace FGFR3 genu – (1..1)
    M_B_2_16_2_4: str = ""
    M_B_2_16_2_4_1: Optional[str] = None
    # (More such FGFR items if present in doc)

    # --------------- RIZIKOVÉ FAKTORY ---------------
    # Kouření – (1..1)
    M_B_2_16_4_1: str = ""
    # Počet balíčkoroků – (float, 0..1)
    M_B_2_16_4_3: Optional[float] = None
    # Alkohol – (0..1)
    M_B_2_16_4_4: Optional[str] = None
    # Profesní expozice chemickým látkám – (1..1)
    M_B_2_16_4_5: str = ""
    # Chronické infekce močových cest – (1..1)
    M_B_2_16_4_6: str = ""


###############################################################################
# M.B.2.17 – Karcinom prostaty
###############################################################################
@dataclass
class MB217:
    """
    M.B.2.17: Karcinom prostaty
    """

    # --------------- LABORATORNÍ MARKERY ---------------
    # PSA (ng/ml) – (float, 0..1)
    M_B_2_17_1_1: Optional[float] = None
    # PSAD (ng/ml^2) – (float, 0..1)
    M_B_8_1_1_2: Optional[float] = None
    # PHI (prostate health index) – (float, 0..1)
    M_B_8_1_1_3: Optional[float] = None
    # PSAdt (PSA doubling time) – (float, 0..1)
    M_B_8_1_1_4: Optional[float] = None
    # NSE – (float, 0..1)
    M_B_8_1_1_5: Optional[float] = None
    # chromogranin A – (float, 0..1)
    M_B_8_1_1_6: Optional[float] = None

    # --------------- MOLEKULÁRNĚ-GENETICKÉ MARKERY ---------------
    # NGS – (1..1)
    M_B_2_17_2_1: str
    M_B_2_17_2_2: Optional[date] = None
    M_B_2_17_2_3: Optional[str] = None
    M_B_2_17_2_4: str = ""
    M_B_2_17_2_5: Optional[float] = None

    # BRCA1 mutace – (1..1)
    M_B_2_17_2_2_: str = ""
    # BRCA2 mutace – (1..1)
    M_B_2_17_2_3_: str = ""
    # ATM mutace – (1..1)
    M_B_2_17_2_4_: str = ""
    # Jiné relevantní nálezy – (text, 0..1)
    M_B_2_17_2_5_: Optional[str] = None

    # --------------- KLASIFIKACE ---------------
    # Gleason staging – (Povinné "ANO/NE")
    M_B_2_17_3_1: str = ""
    # Gleason grade primární – (1..1 if above=Ano)
    M_B_2_17_3_2: Optional[str] = None
    # Gleason grade sekundární – (1..1)
    M_B_2_17_3_3: Optional[str] = None
    # Gleason grade sekundární - komponenta(%) – (float, 0..1)
    M_B_2_17_3_3_1: Optional[float] = None
    # Gleason grade terciární – (0..1 if doc says "Podmíněně")
    M_B_2_17_3_4: Optional[str] = None
    # Gleason grade terciární komponenta(%) – (float, 0..1)
    M_B_2_17_3_4_1: Optional[float] = None
    # Gleason - skore – (1..1)
    M_B_2_17_3_5: str = ""
    # WHO ISUP Grade group – (1..1)
    M_B_2_17_3_6: str = ""

    # --------------- RIZIKOVÉ FAKTORY ---------------
    # mpMR PIRADS – (0..1, {1..5})
    M_B_2_17_4_1: Optional[str] = None
    # kribriformní histologický subtyp – (1..1)
    M_B_2_17_4_2: str = ""
    # intraduktální karcinom – (1..1)
    M_B_2_17_4_3: str = ""
    # lymfovaskulární invaze – (1..1)
    M_B_2_17_4_4: str = ""
    # perineurální šíření – (1..1)
    M_B_2_17_4_5: str = ""
    # Riziko recidivy (EAU guidelines) – (1..1)
    M_B_2_17_4_6: str = ""


###############################################################################
# M.B.2.18 – Germinální nádory pohlavních orgánů
###############################################################################
@dataclass
class MB218:
    """
    M.B.2.18: Germinální nádory
    """

    # --------------- LABORATORNÍ MARKERY ---------------
    # AFP [kU/L] – (float, 0..1)
    M_B_2_18_1_1: Optional[float] = None
    # bHCG [U/L] – (float, 0..1)
    M_B_2_18_1_2: Optional[float] = None
    # LDH [ukat/L] – (float, 0..1)
    M_B_2_18_1_3: Optional[float] = None
    # miR371 – (float, 0..1)
    M_B_2_18_1_4: Optional[float] = None

    # --------------- MOLEKULÁRNĚ-GENETICKÉ MARKERY ---------------
    # NGS – (1..1)
    M_B_2_18_2_1: str
    M_B_2_18_2_1_1: Optional[date] = None
    M_B_2_18_2_1_2: Optional[str] = None
    M_B_2_18_2_1_3: str = ""
    M_B_2_18_2_1_4: Optional[float] = None

    # Jiné relevantní molekulárně-genetické nálezy – (text, 0..1)
    M_B_2_18_2_2: Optional[str] = None


###############################################################################
# M.B.2.20 – Nádory kůže (nemelanomové)
###############################################################################
@dataclass
class MB220:
    """
    M.B.2.20: Nádory kůže (nemelanomové)
    """

    # --------------- RIZIKOVÉ FAKTORY ---------------
    # Nádory kůže v RA – (1..1)
    M_B_2_20_2_1: str = ""
    # Dědičné predispoziční syndromy – (0..1)
    M_B_2_20_2_2: Optional[str] = None
    # Jiný predispoziční syndrom – (1..1 if "jiný" chosen)
    M_B_2_20_2_2_1: Optional[str] = None
    # Nádor kůže v OA – (1..1)
    M_B_2_20_2_3: str = ""
    # Chronická imunosupresivní léčba – (1..1)
    M_B_2_20_2_4: str = ""


###############################################################################
# M.B.2.21 – Maligní melanom
###############################################################################
@dataclass
class MB221:
    """
    M.B.2.21: Maligní melanom
    """

    # --------------- LABORATORNÍ MARKERY ---------------
    # S100b [µg/l] – (float, 0..1)
    M_B_2_21_1_1: Optional[float] = None
    # LDH [µkat/l] – (float, 0..1)
    M_B_2_21_1_2: Optional[float] = None

    # --------------- MOLEKULÁRNĚ-GENETICKÉ MARKERY ---------------
    # NGS – (1..1)
    M_B_2_21_2_1: str
    # Datum NGS – (date, 0..1)
    M_B_2_21_2_2: Optional[date] = None
    # Vyšetřovaná tkáň – (text, 0..1)
    M_B_2_21_2_3: Optional[str] = None
    # Výsledek NGS – (1..1)
    M_B_2_21_2_4: str = ""
    # TMB – (float, 0..1)
    M_B_2_21_2_5: Optional[float] = None

    # PD-L1 exprese – (1..1)
    M_B_2_21_2_2_: str = ""
    # alterace BRAF genu – (1..1)
    M_B_2_21_2_3_: str = ""
    # BRAF - typ mutace – (text, 0..1)
    M_B_2_21_2_3_1: Optional[str] = None
    # alterace NRAS genu – (1..1)
    M_B_2_21_2_4_: str = ""
    # NRAS - typ mutace – (text, 0..1)
    M_B_2_21_2_4_1: Optional[str] = None
    # cKIT – (1..1)
    M_B_2_21_2_5_: str = ""
    # Jiné molekulárně-genetické nálezy – (text, 0..1)
    M_B_2_21_2_6: Optional[str] = None

    # --------------- KLASIFIKACE ---------------
    # Podtyp melanomu (superficiální, nodulární, …) – (1..1)
    M_B_2_21_3_1: str = ""
    # Breslow [mm] – (float, 0..1)
    M_B_2_21_3_2: Optional[float] = None
    # Clark – (1..1)
    M_B_2_21_3_3: str = ""
    # Ulcerace – (1..1)
    M_B_2_21_3_4: str = ""
    # Počet mitos (/mm2) – (float, 0..1)
    M_B_2_21_3_5: Optional[float] = None
    # Lymfovaskulární invaze – (1..1)
    M_B_2_21_3_6: str = ""
    # Perineurální invaze – (1..1)
    M_B_2_21_3_7: str = ""
    # Tumor infiltrující lymfocyty – (1..1)
    M_B_2_21_3_8: str = ""
    # Sentinelová uzlina – (1..1)
    M_B_2_21_3_10: str = ""
    # Satelity/intransitní metastázy – (1..1)
    M_B_2_21_3_11: str = ""

    # --------------- RIZIKOVÉ FAKTORY ---------------
    # Melanom v RA – (1..1)
    M_B_2_21_4_1: str = ""
    # Dědičné predispoziční syndromy – (0..1)
    M_B_2_21_4_2: Optional[str] = None
    # Jiný predispoziční syndrom – (0..1 if “jiný”)
    M_B_2_21_4_3: Optional[str] = None
    # Melanom v OA – (1..1)
    M_B_2_21_4_4: str = ""
    # Fototyp (1..6) – (0..1)
    M_B_2_21_4_5: Optional[str] = None
    # Lokalizace (hlava a krk, trup, HK, DK) – (1..1)
    M_B_2_21_4_6: str = ""
    # Akrolentiginózní typ – (1..1)
    M_B_2_21_4_7: str = ""
    # Chronická imunosupresivní léčba – (1..1)
    M_B_2_21_4_8: str = ""


###############################################################################
# M.B.2.22 – Nádory kostí a sarkomy měkkých tkání
###############################################################################
@dataclass
class MB222:
    """
    M.B.2.22: Nádory kostí a sarkomy měkkých tkání
    """

    # --------------- LABORATORNÍ MARKERY ---------------
    # (Not detailed in the snippet, just a heading.)

    # --------------- MOLEKULÁRNĚ-GENETICKÉ MARKERY ---------------
    # NGS – (1..1)
    M_B_2_22_2_1: str
    # Datum NGS – (date, 0..1)
    M_B_2_22_2_1_1: Optional[date] = None
    # Vyšetřovaná tkáň – (text, 0..1)
    M_B_2_22_2_1_2: Optional[str] = None
    # Výsledek NGS – (text, 1..1)
    M_B_2_22_2_1_3: str = ""
    # TMB – (float, 0..1)
    M_B_2_22_2_1_4: Optional[float] = None
    # Relevantní molekulárně-genetické nálezy – (text, 0..1)
    M_B_2_22_2_2: Optional[str] = None

    # --------------- KLASIFIKACE ---------------
    # Staging dle AJCC (8. th 2016) – (Povinné, 1..1, “Ano/Ne”)
    M_B_2_22_3_1: str = ""
    # AJCC skupina (I, II, III, IV) – (1..1 if above=Ano)
    M_B_2_22_3_2: Optional[str] = None


@dataclass
class MB223:
    """
    M.B.2.23: Nádory endokrinních žláz
    """

    # ------------------ LABORATORNÍ MARKERY (M.B.2.23.1) ------------------
    # CEA (karcinomembryonální antigen) – (float, Podmíněně povinné, 0..1) – u medulárního karcinomu
    M_B_2_23_1_1: Optional[float] = None

    # NSE (neuron specifická enoláza) – (float, Podmíněně povinné, 0..1)
    M_B_2_23_1_2: Optional[float] = None

    # chromogranin A – (float, Podmíněně povinné, 0..1)
    M_B_2_23_1_3: Optional[float] = None

    # ------------------ MOLEKULÁRNĚ-GENETICKÉ MARKERY (M.B.2.23.2) ------------------
    # Multigenové vyšetření pomocí NGS – (výběr {Provedeno, Neprovedeno, Údaj není k dispozici}, 1..1)
    M_B_2_23_2_1: str = ""
    # Datum NGS vyšetření – (date, 0..1)
    M_B_2_23_2_1_1: Optional[date] = None
    # Vyšetřovaná tkáň – (text, 0..1)
    M_B_2_23_2_1_2: Optional[str] = None
    # Výsledek NGS vyšetření – (text, 1..1)
    M_B_2_23_2_1_3: str = ""
    # Nádorová mutační zátěž (TMB) – (float, 0..1)
    M_B_2_23_2_1_4: Optional[float] = None

    # RET mutace – (výběr {Pozitivní, Negativní, Nelze stanovit, Nevyšetřeno}, 1..1)
    M_B_2_23_2_2: str = ""
    # RET - typ mutace – (text, 0..1)
    M_B_2_23_2_2_1: Optional[str] = None

    # BRAF mutace – (výběr {Pozitivní, Negativní, Nelze stanovit, Nevyšetřeno}, 1..1)
    M_B_2_23_2_3: str = ""
    # BRAF - typ mutace – (text, 0..1)
    M_B_2_23_2_3_1: Optional[str] = None

    # RAS mutace (např. HRAS, KRAS, NRAS) – (výběr {Pozitivní, Negativní, Nelze stanovit, Nevyšetřeno}, 1..1)
    M_B_2_23_2_4: str = ""
    # RAS - typ mutace – (text, 0..1)
    M_B_2_23_2_4_1: Optional[str] = None

    # MEN1 mutace – (výběr {Pozitivní, Negativní, Nelze stanovit, Nevyšetřeno}, 1..1)
    M_B_2_23_2_5: str = ""

    # Jiné relevantní molekulárně-genetické nálezy – (text, 0..1)
    M_B_2_23_2_6: Optional[str] = None

    # ------------------ KLASIFIKACE (M.B.2.23.3) ------------------
    # (Exact staging details for endocrine tumors can vary (AJCC/ENETS).
    #  The specification snippet does not show the exact fields, so
    #  here is a placeholder for classification.)
    # Podmíněně povinné? Possibly 1..1 with further subfields if “Ano.”
    M_B_2_23_3_1: Optional[str] = None  # e.g., "WHO classification" or "AJCC stage"

    # ------------------ RIZIKOVÉ FAKTORY (M.B.2.23.4) ------------------
    # (Same here: the doc snippet is minimal, so we place a placeholder.)
    M_B_2_23_4_1: Optional[str] = None  # e.g. "Familiární zátěž, MEN2, etc."


