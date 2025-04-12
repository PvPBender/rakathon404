from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from typing import List, Optional

#
# ==============================
#        ENUM DEFINITIONS
# ==============================
#


class AnoNeUdaj(Enum):
    """
    Common enumerations for fields that have the choices
    {ANO, NE, Údaj není k dispozici}.
    """

    ANO = "ANO"
    NE = "NE"
    UDAJ_NENI_K_DISPOZICI = "Údaj není k dispozici"


class IndikaceOperacnihoVykonu(Enum):
    """
    M.C.2.2 Indikace operačního výkonu – výběr {onkologická, ne-onkologická}
    """

    ONKOLOGICKA = "onkologická"
    NE_ONKOLOGICKA = "ne-onkologická"


class StrategieOnkologickeOperace(Enum):
    """
    M.C.2.3 Strategie onkologické operace –
    výběr {kurativní, paliativní, preventivní, výlučně diagnostická, rekonstrukční}
    """

    KURATIVNI = "kurativní"
    PALIATIVNI = "paliativní"
    PREVENTIVNI = "preventivní"
    VYLUCNE_DIAGNOSTICKA = "výlučně diagnostická"
    REKONSTRUKCNI = "rekonstrukční"


class PoradiOnkolOperace(Enum):
    """
    M.C.2.4 Pořadí onkol.operace –
    výběr {primární, následná}
    """

    PRIMARNI = "primární"
    NASLEDNA = "následná"


class OperacniPristup(Enum):
    """
    M.C.2.5 Operační přístup –
    výběr {otevřený, endoskopický, laparoskopický, vaginální, robotický, kombinovaný};
    lze zvolit více možností
    """

    OTEVRENY = "otevřený"
    ENDOSKOPICKY = "endoskopický"
    LAPAROSKOPICKY = "laparoskopický"
    VAGINALNI = "vaginální"
    ROBOTICKY = "robotický"
    KOMBINOVANY = "kombinovaný"


class TypVykonuPrimarniNador(Enum):
    """
    M.C.2.6 Typ výkonu - primární nádor –
    výběr {radikální resekce orgánu, parciální resekce orgánu,
           debulking (cytoredukce), biopsie, žádná}
    """

    RADIKALNI_RESEKCE = "radikální resekce orgánu"
    PARCIALNI_RESEKCE = "parciální resekce orgánu"
    DEBULKING = "debulking (cytoredukce)"
    BIOPSIE = "biopsie"
    ZADNA = "žádná"


class RadikalniResekceCNS(Enum):
    """
    M.C.2.6.1 Radikální resekce - nádory CNS –
    výběr {GTR (radikální totální resekce), NTR (téměř totální resekce), STR (subtotální resekce)}
    """

    GTR = "GTR (radikální totální resekce)"
    NTR = "NTR (téměř totální resekce)"
    STR = "STR (subtotální resekce)"


class MakroskopickeRezidum(Enum):
    """
    M.C.2.7 Makroskopické rezidum nádoru (R2) –
    výběr {Ano, Ne, Nehodnoceno}
    """

    ANO = "Ano"
    NE = "Ne"
    NEHODNOCENO = "Nehodnoceno"


class TypVykonuRegionalniUzliny(Enum):
    """
    M.C.2.8 Typ výkonu - regionální uzliny (výsledný stav) –
    výběr {sentinelová biopsie, targeted dissection, lymfadenektomie,
           sampling, žádný}; lze zvolit více možností
    """

    SENTINELOVA_BIOPSIE = "sentinelová biopsie"
    TARGETED_DISSECTION = "targeted dissection"
    LYMFADENEKTOMIE = "lymfadenektomie"
    SAMPLING = "sampling"
    ZADNY = "žádný"


class Metastazektomie(Enum):
    """
    M.C.2.9 Metastazektomie - vzdálené metastázy –
    výběr {ANO, NE, Údaj není k dispozici}
    """

    ANO = "ANO"
    NE = "NE"
    UDAJ_NENI_K_DISPOZICI = "Údaj není k dispozici"


class MetastazektomieLokalizace(Enum):
    """
    M.C.2.9.1 Lokalizace vzdálených metastáz –
    výběr {plíce, kostní dřeň, kost, pleura, játra, peritoneum, mozek,
           nadledviny, uzliny, kůže, jiný orgán}; více možností
    """

    Plice = "plíce"
    KostniDren = "kostní dřeň"
    Kost = "kost"
    Pleura = "pleura"
    Jatra = "játra"
    Peritoneum = "peritoneum"
    Mozek = "mozek"
    Nadledviny = "nadledviny"
    Uzliny = "uzliny"
    Kuze = "kůže"
    JinyOrgan = "jiný orgán"


class SpecialniMetoda(Enum):
    """
    M.C.2.10 Speciální metoda –
    výběr {ANO, NE}
    """

    ANO = "ANO"
    NE = "NE"


class SpecialniMetodaSpecifikace(Enum):
    """
    M.C.2.10.1 Speciální metoda - specifikace –
    výběr {HIPEC, PIPAC, ILP, RFA, kryoablace, MWA, Jiná}
    """

    HIPEC = "HIPEC"
    PIPAC = "PIPAC"
    ILP = "ILP"
    RFA = "RFA"
    KRYOABLACE = "kryoablace"
    MWA = "MWA"
    JINA = "Jiná"


class PlanovanaStrategie(Enum):
    """
    Used in multiple modules (M.C.3, M.C.4, M.C.5, M.C.6, M.C.7, M.C.8, M.C.9):
    výběr {kurativní, paliativní}
    """

    KURATIVNI = "kurativní"
    PALIATIVNI = "paliativní"


class UpresneniStrategie(Enum):
    """
    Used in multiple modules (M.C.3, M.C.4, M.C.5, M.C.6, M.C.7, M.C.8, M.C.9):
    výběr {neoadjuvance, adjuvance, upfront}
    (In some modules, 'upfront' might not appear, but we include it
     if the specification mentions it.)
    """

    NEOADJUVANCE = "neoadjuvance"
    ADJUVANCE = "adjuvance"
    UPFRONT = "upfront"


class AnoNeUdajVolitelne(Enum):
    """
    Used for M.C.4.5 Konkomitantní strategie or M.C.4.7 Brachyterapie, etc.,
    which can be ANO/NE/Údaj není k dispozici but is also Volitelné (0..1).
    We'll still store it as an Enum.
    """

    ANO = "ANO"
    NE = "NE"
    UDAJ_NENI_K_DISPOZICI = "Údaj není k dispozici"


class TypZevniRadioterapie(Enum):
    """
    M.C.4.6.1 Typ zevní RT:
    výběr {fotonová, protonová, elektronová, ortovoltážní}, více možností
    """

    FOTONOVA = "fotonová"
    PROTONOVA = "protonová"
    ELEKTRONOVA = "elektronová"
    ORTOVOLTAZNI = "ortovoltážní"


class HodnocenaLecebnaOdpoved(Enum):
    """
    M.C.10.2.2 Hodnocená léčebná odpověď –
    výběr {Kompletní remise (CR), Parciální remise (PR), Stabilizace (SD),
           Progrese (PD), Nelze hodnotit}
    """

    CR = "Kompletní remise (CR)"
    PR = "Parciální remise (PR)"
    SD = "Stabilizace (SD)"
    PD = "Progrese (PD)"
    NELZE_HODNOTIT = "Nelze hodnotit"


class ProgreseTyp(Enum):
    """
    M.C.10.2.3 Progrese –
    výběr {lokální recidiva, diseminace}
    """

    LOKALNI_RECIDIVA = "lokální recidiva"
    DISEMINACE = "diseminace"


class ToxicitaAsociovanaS(Enum):
    """
    M.C.11.3 Toxicita asociovaná s léčbou –
    výběr {chirurgickou, chemoterapií, radioterapií,
           biologickou/cílenou, imunoterapií, hormonoterapií,
           s jiným druhem léčby, neznámo}; více možností
    """

    CHIRURGICKOU = "chirurgickou"
    CHEMOTERAPII = "chemoterapií"
    RADIOTERAPII = "radioterapií"
    BIOLOGICKOU_CILENOU = "biologickou/cílenou"
    IMUNOTERAPII = "imunoterapií"
    HORMONOTERAPII = "hormonoterapií"
    JINA_LECBA = "s jiným druhem léčby"
    NEZNAMO = "neznámo"


class TypToxicity(Enum):
    """
    M.C.11.4 Typ toxicity –
    výběr {akutní, chronická}
    """

    AKUTNI = "akutní"
    CHRONICKA = "chronická"


class UpravaAdIntegrum(Enum):
    """
    M.C.11.5 Úprava ad integrum –
    výběr {ANO, NE, údaj není k dispozici}
    Re-uses the same pattern as AnoNeUdaj
    """

    ANO = "ANO"
    NE = "NE"
    UDAJ_NENI_K_DISPOZICI = "Údaj není k dispozici"


class HodnoceniNsledkuLecby(Enum):
    """
    M.C.11.6 Hodnocení následků léčby –
    výběr {0 - Žádný následek, 1- Následky asymptomatické..., 2- Následky jsou asymptomatické...,
           3- Následky (fyzické nebo psychické)..., 4- Závažné následky...}
    """

    ZERO = "0 - Žádný následek"
    ONE = "1- Následky jsou asymptomatické a nevyžadují léčbu..."
    TWO = "2- Následky jsou asymptomatické díky dlouhodobé léčbě..."
    THREE = "3- Následky (fyzické nebo psychické), které již nelze zmírnit..."
    FOUR = "4- Závažné následky (fyzické nebo psychické), které již nelze zmírnit..."


class TypStudie(Enum):
    """
    M.C.12.2 Typ studie –
    výběr {akademická, komerční}
    """

    AKADEMICKA = "akademická"
    KOMERCNI = "komerční"


#
# ==============================
#     DATACLASS DEFINITIONS
# ==============================
#

# NOTE: M.C.1 is mostly a heading plus a derived field for "Datum zahájení léčby (nejstarší datum)."
# We'll omit M.C.1 or treat it trivially, as it is "Odvozený parametr."
# The main repeated sets start from M.C.2 onward.


#
# --- M.C.2 (Chirurgická léčba) ---
#
@dataclass
class MC2:
    """
    Opakovatelná sada parametrů pro Chirurgickou léčbu (M.C.2).
    """

    # M.C.2.1 (Povinné, 1..1)
    M_C_2_1: date = None
    """Datum operace – Povinné, 1..1"""

    # M.C.2.2 (Podmíněně povinné, 1..1)
    M_C_2_2: Optional[IndikaceOperacnihoVykonu] = None
    """Indikace operačního výkonu – výběr {onkologická, ne-onkologická}"""

    # M.C.2.3 (Podmíněně povinné, 1..1)
    M_C_2_3: Optional[StrategieOnkologickeOperace] = None
    """Strategie onkologické operace – výběr {kurativní, paliativní, ...}"""

    # M.C.2.4 (Podmíněně povinné, 1..1)
    M_C_2_4: Optional[PoradiOnkolOperace] = None
    """Pořadí onkol.operace – výběr {primární, následná}"""

    # M.C.2.5 (Podmíněně povinné, 1..1, více možností)
    M_C_2_5: List[OperacniPristup] = field(default_factory=list)
    """Operační přístup – více možností {otevřený, endoskopický, ...}"""

    # M.C.2.5.1 (Podmíněně povinné, 1..1)
    M_C_2_5_1: Optional[AnoNeUdaj] = None
    """Konverze – výběr {ANO, NE, Údaj není k dispozici}"""

    # M.C.2.6 (Podmíněně povinné, 1..1)
    M_C_2_6: Optional[TypVykonuPrimarniNador] = None
    """Typ výkonu - primární nádor – {radikální resekce orgánu, ...}"""

    # M.C.2.6.1 (Podmíněně povinné, 0..1)
    M_C_2_6_1: Optional[RadikalniResekceCNS] = None
    """Radikální resekce - nádory CNS – {GTR, NTR, STR}"""

    # M.C.2.7 (Povinné, 1..1)
    M_C_2_7: MakroskopickeRezidum = field(default_factory=MakroskopickeRezidum)
    """Makroskopické rezidum nádoru (R2) – {Ano, Ne, Nehodnoceno}"""

    # M.C.2.8 (Podmíněně povinné, 0..*)
    M_C_2_8: List[TypVykonuRegionalniUzliny] = field(default_factory=list)
    """Typ výkonu - regionální uzliny – více možností {sentinelová biopsie, ...}"""

    # M.C.2.9 (Podmíněně povinné, 1..1)
    M_C_2_9: Optional[Metastazektomie] = None
    """Metastazektomie - vzdálené metastázy – {ANO, NE, Údaj není k dispozici}"""

    # M.C.2.9.1 (Podmíněně povinné, 1..*, accessible if M.C.2.9 == ANO)
    M_C_2_9_1: List[MetastazektomieLokalizace] = field(default_factory=list)
    """Lokalizace vzdálených metastáz – více možností {plíce, játra, atd.}"""

    # M.C.2.9.1.1 (Podmíněně povinné, 1..1 if "jiný orgán" was chosen)
    M_C_2_9_1_1: Optional[str] = None
    """Jiný orgán – text, conditionally required if 'jiný orgán' chosen above"""

    # M.C.2.10 (Podmíněně povinné, 1..1)
    M_C_2_10: Optional[SpecialniMetoda] = None
    """Speciální metoda – {ANO, NE}"""

    # M.C.2.10.1 (Podmíněně povinné, 1..1 if M.C.2.10 == ANO)
    M_C_2_10_1: Optional[SpecialniMetodaSpecifikace] = None
    """Speciální metoda - specifikace – {HIPEC, PIPAC, ILP, ...}"""

    # M.C.2.10.2 (Podmíněně povinné, 1..1 if M.C.2.10.1 == Jiná)
    M_C_2_10_2: Optional[str] = None
    """Speciální metoda - Jiná – text, conditionally required"""

    # M.C.2.11 (Volitelné, 0..1)
    M_C_2_11: Optional[str] = None
    """Volitelný komentář – text"""


#
# --- M.C.3 (CHEMOTERAPIE) ---
#
@dataclass
class MC3:
    """
    Opakovatelná sada parametrů pro CHEMOTERAPII (M.C.3).
    """

    # M.C.3.1 (Podmíněně povinné, 0..1)
    M_C_3_1: Optional[date] = None
    """Datum zahájení – Podmíněně povinné, 0..1"""

    # M.C.3.2 (Podmíněně povinné, 0..1)
    M_C_3_2: Optional[date] = None
    """Datum ukončení – Podmíněně povinné, 0..1"""

    # M.C.3.3 (Podmíněně povinné, 0..1)
    M_C_3_3: Optional[PlanovanaStrategie] = None
    """Plánovaná strategie – výběr {kurativní, paliativní}"""

    # M.C.3.4 (Volitelné, 0..1) if M.C.3.3 == "kurativní"
    M_C_3_4: Optional[UpresneniStrategie] = None
    """Upřesnění strategie – výběr {neoadjuvance, adjuvance, upfront}"""

    # M.C.3.5 (Podmíněně povinné, 0..1)
    M_C_3_5: Optional[str] = None
    """Režim – text (např. název chemoterapeutického režimu)"""

    # M.C.3.6 (Volitelné, 0..*)
    M_C_3_6: List[str] = field(default_factory=list)
    """Podané léčivo – číselník ATC, více možností"""

    # M.C.3.7 (Podmíněně povinné, 1..1)
    M_C_3_7: Optional[AnoNeUdaj] = None
    """Byla překročena kumulativní dávka? – {ANO, NE, Údaj není k dispozici}"""

    # M.C.3.8 (Volitelné, 0..1)
    M_C_3_8: Optional[str] = None
    """Volitelný komentář – text"""


#
# --- M.C.4 (RADIOTERAPIE) ---
#
@dataclass
class MC4:
    """
    Opakovatelná sada parametrů pro RADIOTERAPII (M.C.4).
    """

    # M.C.4.1 (Povinné, 1..1)
    M_C_4_1: date = None
    """Datum zahájení série – Povinné, 1..1"""

    # M.C.4.2 (Podmíněně povinné, 0..1)
    M_C_4_2: Optional[date] = None
    """Datum ukončení série – Podmíněně povinné, 0..1"""

    # M.C.4.3 (Podmíněně povinné, 0..1) – výběr {kurativní, paliativní}
    M_C_4_3: Optional[PlanovanaStrategie] = None
    """Plánovaná strategie – {kurativní, paliativní}"""

    # M.C.4.4 (Volitelné, 0..1) – výběr {neoadjuvance, adjuvance, upfront}
    M_C_4_4: Optional[UpresneniStrategie] = None
    """Upřesnění strategie – volitelné, 0..1"""

    # M.C.4.5 (Volitelné, 0..1) – výběr {ANO, NE, Údaj není k dispozici}
    M_C_4_5: Optional[AnoNeUdajVolitelne] = None
    """Konkomitantní strategie – ANO/NE/Údaj není k dispozici"""

    # M.C.4.6 (Povinné, 1..1) – výběr {ANO, NE, Údaj není k dispozici}
    M_C_4_6: AnoNeUdaj = field(default_factory=AnoNeUdaj)
    """Zevní radioterapie – Povinné, 1..1"""

    # M.C.4.6.1 (Podmíněně povinné, 1..1) if M.C.4.6 == ANO,
    # více možností {fotonová, protonová, elektronová, ortovoltážní}
    M_C_4_6_1: List[TypZevniRadioterapie] = field(default_factory=list)
    """Typ zevní RT – více možností"""

    # M.C.4.7 (Povinné, 1..1) – ANO/NE/Údaj není k dispozici
    M_C_4_7: AnoNeUdaj = field(default_factory=AnoNeUdaj)
    """Brachyterapie – Povinné, 1..1"""

    # M.C.4.8 (Podmíněně povinné, 0..1) – text
    M_C_4_8: Optional[str] = None
    """Cílový objem – text"""

    # M.C.4.9 (Podmíněně povinné, 0..1) – integer
    M_C_4_9: Optional[int] = None
    """Počet frakcí – integer"""

    # M.C.4.10 (Podmíněně povinné, 0..1) – integer, jednotka (Gy)
    M_C_4_10: Optional[int] = None
    """Celková dávka (Gy) – integer"""

    # M.C.4.11 (Podmíněně povinné, 0..1) – text
    M_C_4_11: Optional[str] = None
    """Ozáření vulnerabilních orgánů – text"""

    # M.C.4.12 (Volitelné, 0..1) – text
    M_C_4_12: Optional[str] = None
    """Radioterapeutické centrum – text"""

    # M.C.4.13 (Volitelné, 0..1) – text
    M_C_4_13: Optional[str] = None
    """Volitelný komentář – text"""


#
# --- M.C.5 (CÍLENÁ LÉČBA) ---
#
@dataclass
class MC5:
    """
    Opakovatelná sada parametrů pro CÍLENOU LÉČBU (M.C.5).
    """

    # M.C.5.1 (Povinné, 1..1)
    M_C_5_1: date = None
    """Datum zahájení – Povinné, 1..1"""

    # M.C.5.2 (Podmíněně povinné, 0..1)
    M_C_5_2: Optional[date] = None
    """Datum ukončení – Podmíněně povinné, 0..1"""

    # M.C.5.3 (Podmíněně povinné, 0..1)
    M_C_5_3: Optional[PlanovanaStrategie] = None
    """Plánovaná strategie – {kurativní, paliativní}"""

    # M.C.5.4 (Volitelné, 0..1) if M.C.5.3 = kurativní
    M_C_5_4: Optional[UpresneniStrategie] = None
    """Upřesnění strategie – {neoadjuvance, adjuvance}"""

    # M.C.5.5 (Povinné, 1..1) – text
    M_C_5_5: str = ""
    """Režim – text (povinné)"""

    # M.C.5.6 (Volitelné, 0..*) – číselník ATC, více možností
    M_C_5_6: List[str] = field(default_factory=list)
    """Podané léčivo – více možností"""

    # M.C.5.7 (Volitelné, 0..1) – text
    M_C_5_7: Optional[str] = None
    """Volitelný komentář – text"""


#
# --- M.C.6 (HORMONOTERAPIE) ---
#
@dataclass
class MC6:
    """
    Opakovatelná sada parametrů pro HORMONOTERAPII (M.C.6).
    """

    # M.C.6.1 (Povinné, 1..1)
    M_C_6_1: date = None
    """Datum zahájení – Povinné, 1..1"""

    # M.C.6.2 (Podmíněně povinné, 0..1)
    M_C_6_2: Optional[date] = None
    """Datum ukončení – Podmíněně povinné, 0..1"""

    # M.C.6.3 (Podmíněně povinné, 0..1)
    M_C_6_3: Optional[PlanovanaStrategie] = None
    """Plánovaná strategie – {kurativní, paliativní}"""

    # M.C.6.4 (Volitelné, 0..1) if M.C.6.3 = kurativní
    M_C_6_4: Optional[UpresneniStrategie] = None
    """Upřesnění strategie – {neoadjuvance, adjuvance}"""

    # M.C.6.5 (Povinné, 1..1) – text
    M_C_6_5: str = ""
    """Režim – text (povinné)"""

    # M.C.6.6 (Volitelné, 0..*) – číselník ATC, více možností
    M_C_6_6: List[str] = field(default_factory=list)
    """Podané léčivo – více možností"""

    # M.C.6.7 (Volitelné, 0..1) – text
    M_C_6_7: Optional[str] = None
    """Volitelný komentář – text"""


#
# --- M.C.7 (IMUNOTERAPIE) ---
#
@dataclass
class MC7:
    """
    Opakovatelná sada parametrů pro IMUNOTERAPII (M.C.7).
    """

    # M.C.7.1 (Povinné, 1..1)
    M_C_7_1: date = None
    """Datum zahájení – Povinné, 1..1"""

    # M.C.7.2 (Podmíněně povinné, 0..1)
    M_C_7_2: Optional[date] = None
    """Datum ukončení – Podmíněně povinné, 0..1"""

    # M.C.7.3 (Podmíněně povinné, 0..1)
    M_C_7_3: Optional[PlanovanaStrategie] = None
    """Plánovaná strategie – {kurativní, paliativní}"""

    # M.C.7.4 (Volitelné, 0..1)
    M_C_7_4: Optional[UpresneniStrategie] = None
    """Upřesnění strategie – {neoadjuvance, adjuvance} if M.C.7.3 = kurativní"""

    # M.C.7.5 (Povinné, 1..1) – text
    M_C_7_5: str = ""
    """Režim – povinné, 1..1"""

    # M.C.7.6 (Volitelné, 0..*) – číselník ATC, více možností
    M_C_7_6: List[str] = field(default_factory=list)
    """Podané léčivo – více možností"""

    # M.C.7.7 (Volitelné, 0..1) – text
    M_C_7_7: Optional[str] = None
    """Volitelný komentář – text"""


#
# --- M.C.8 (CYTOKINOVÁ TERAPIE) ---
#
@dataclass
class MC8:
    """
    Opakovatelná sada parametrů pro CYTOKINOVOU TERAPII (M.C.8).
    """

    # M.C.8.1 (Povinné, 1..1)
    M_C_8_1: date = None
    """Datum zahájení – Povinné, 1..1"""

    # M.C.8.2 (Podmíněně povinné, 0..1)
    M_C_8_2: Optional[date] = None
    """Datum ukončení – Podmíněně povinné, 0..1"""

    # M.C.8.3 (Podmíněně povinné, 0..1)
    M_C_8_3: Optional[PlanovanaStrategie] = None
    """Plánovaná strategie – {kurativní, paliativní}"""

    # M.C.8.4 (Volitelné, 0..1)
    M_C_8_4: Optional[UpresneniStrategie] = None
    """Upřesnění strategie – {neoadjuvance, adjuvance} if M.C.8.3 = kurativní"""

    # M.C.8.5 (Povinné, 1..1) – text
    M_C_8_5: str = ""
    """Režim – povinné, 1..1"""

    # M.C.8.6 (Volitelné, 0..1) – text
    M_C_8_6: Optional[str] = None
    """Volitelný komentář – text"""


#
# --- M.C.9 (JINÉ LÉČEBNÉ MODALITY) ---
#
@dataclass
class MC9:
    """
    Opakovatelná sada parametrů pro JINÉ LÉČEBNÉ MODALITY (M.C.9).
    """

    # M.C.9.1 (Povinné, 1..1)
    M_C_9_1: date = None    
    """Datum zahájení – Povinné, 1..1"""

    # M.C.9.2 (Podmíněně povinné, 0..1)
    M_C_9_2: Optional[date] = None
    """Datum ukončení – Podmíněně povinné, 0..1"""

    # M.C.9.3 (Podmíněně povinné, 0..1)
    M_C_9_3: Optional[PlanovanaStrategie] = None
    """Plánovaná strategie – {kurativní, paliativní}"""

    # M.C.9.4 (Volitelné, 0..1)
    M_C_9_4: Optional[UpresneniStrategie] = None
    """Upřesnění strategie – {neoadjuvance, adjuvance} if M.C.9.3 = kurativní"""

    # M.C.9.5 (Povinné, 1..1) – číselník
    # (RFA, MWA, jiná termoablace, embolizace/chemoembolizace, kryoterapie,
    #  vertebroplastika, intravezikální léčba, intrakavitální léčba, ILP, jiná)
    # The specification says "více možností," but the table shows "1..1"?
    # Possibly it means you can pick multiple from that číselník. We'll assume 1..1 or more:
    M_C_9_5: List[str] = field(default_factory=list)
    """Jiná léčba – 1..1, possibly více možností from a special číselník"""

    # M.C.9.6 (Volitelné, 0..1)
    M_C_9_6: Optional[str] = None
    """Volitelný komentář – text"""


#
# --- M.C.10 (LÉČEBNÁ ODPOVĚĎ) ---
#
@dataclass
class MC10_2:
    """
    M.C.10.2  (Opakovatelná sada parametrů) – Přešetření
    """

    # M.C.10.2.1 (Povinné, 0..1)
    M_C_10_2_1: Optional[date] = None
    """Datum hodnocení léčebné odpovědi – datum, povinné 0..1 (somewhat contradictory 
       but let's treat it as optional)"""

    # M.C.10.2.2 (Povinné, 1..1) – výběr {CR, PR, SD, PD, Nelze hodnotit}
    M_C_10_2_2: HodnocenaLecebnaOdpoved = field(default_factory=HodnocenaLecebnaOdpoved)
    """Hodnocená léčebná odpověď – povinné, 1..1"""

    # M.C.10.2.3 (Podmíněně povinné, 1..1 if Progrese)
    M_C_10_2_3: Optional[ProgreseTyp] = None
    """Progrese – výběr {lokální recidiva, diseminace} if M.C.10.2.2=Progrese(PD)"""

    # M.C.10.2.4 (Volitelné, 0..1)
    M_C_10_2_4: Optional[str] = None
    """Volitelný komentář – text"""


@dataclass
class MC10:
    """
    M.C.10 Léčebná odpověď – nadpis
    """

    # M.C.10.1 (Podmíněně povinné, 1..1)
    M_C_10_1: Optional[str] = None
    """Guideline/kritéria pro hodnocení léčebné odpovědi – text, 1..1 
       (the table says 'Podmíněně povinné', but we store as optional 
        with the condition in real usage)"""

    # M.C.10.2 (Opakovatelná sada parametrů, 0..*)
    M_C_10_2: List[MC10_2] = field(default_factory=list)
    """Přešetření – 0..*"""


#
# --- M.C.11 (ZÁVAŽNÁ TOXICITA) ---
#
@dataclass
class MC11:
    """
    M.C.11 Závažná toxicita onkologické léčby relevantní pro následnou péči
    (Opakovatelná sada parametrů)
    """

    # M.C.11.1 (Povinné, 1..1)
    M_C_11_1: str = ""
    """Název – text, povinné, 1..1"""

    # M.C.11.2 (Podmíněně povinné, 1..1)
    M_C_11_2: Optional[date] = None
    """Datum – datum, podmíněně povinné, 1..1"""

    # M.C.11.3 (Podmíněně povinné, 1..1) – výběr {chirurgickou, chemoterapií, ...}; více možností
    M_C_11_3: List[ToxicitaAsociovanaS] = field(default_factory=list)
    """Toxicita asociovaná s léčbou – multiple choice"""

    # M.C.11.4 (Podmíněně povinné, 1..1)
    M_C_11_4: Optional[TypToxicity] = None
    """Typ toxicity – {akutní, chronická}"""

    # M.C.11.5 (Podmíněně povinné, 1..1)
    M_C_11_5: Optional[UpravaAdIntegrum] = None
    """Úprava ad integrum – {ANO, NE, Údaj není k dispozici}"""

    # M.C.11.6 (Podmíněně povinné, 1..1)
    M_C_11_6: Optional[HodnoceniNsledkuLecby] = None
    """Hodnocení následků léčby – {0,1,2,3,4} (detailed text)"""

    # M.C.11.7 (Volitelné, 0..1) – text
    M_C_11_7: Optional[str] = None
    """Volitelný komentář – text"""


#
# --- M.C.12 (Pacient zařazený do intervenční klinické studie) ---
#
@dataclass
class MC12:
    """
    M.C.12 Pacient zařazený do intervenční klinické studie
    (opakovaná sada parametrů)
    """

    # M.C.12.1 (Povinné, 1..1)
    M_C_12_1: str = ""  
    """Název studie – text, povinné, 1..1"""

    # M.C.12.2 (Podmíněně povinné, 1..1) – {akademická, komerční}
    M_C_12_2: Optional[TypStudie] = None
    """Typ studie – {akademická, komerční}"""

    # M.C.12.3 (Podmíněně povinné, 0..*) – text
    M_C_12_3: List[str] = field(default_factory=list)
    """Rameno studie – text, 0..*"""

    # M.C.12.4 (Podmíněně povinné, 1..1) – datum
    M_C_12_4: Optional[date] = None
    """Datum zařazení – datum, 1..1"""

    # M.C.12.5 (Podmíněně povinné, 1..1) – datum
    M_C_12_5: Optional[date] = None
    """Datum vyřazení – datum, 1..1"""

    # M.C.12.6 (Volitelné, 0..1) – text
    M_C_12_6: Optional[str] = None
    """Volitelný komentář – text"""


#
# ============= END OF FILE =============
#

@dataclass
class PacientTemplateModuleC:
    """
    Main class for Module C that encapsulates all treatment-related data.
    """
        # M_B_2_1: Optional["MB21"] = None  # Nádory CNS

    M_C_2: Optional["MC2"] = None  # Chirurgická léčba
    M_C_3: Optional["MC3"] = None  # Chemoterapie
    M_C_4: Optional["MC4"] = None  # Radioterapie
    M_C_5: Optional["MC5"] = None  # Cílená léčba
    M_C_6: Optional["MC6"] = field(default_factory=list)  # Hormonoterapie
    M_C_7: Optional["MC7"] = field(default_factory=list)  # Imunoterapie
    M_C_8: Optional["MC8"] = field(default_factory=list)  # Cytokinová terapie
    M_C_9: Optional["MC9"] = field(default_factory=list)  # Jiné léčebné modifity
    M_C_10: Optional["MC10"] = field(default_factory=list)  # Léčebná odpověď
    M_C_11: Optional["MC11"] = field(default_factory=list)  # Závažná toxicita
    M_C_12: Optional["MC12"] = field(default_factory=list)  # Klinické studie
    