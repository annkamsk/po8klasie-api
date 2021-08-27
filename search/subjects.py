from dataclasses import dataclass
from enum import Enum, IntEnum
from typing import Dict, Any, Optional

from django.core.exceptions import ValidationError


class SubjectName(Enum):
    BIOL = "biol", "biologia"
    CHEM = "chem", "chemia"
    FILOZ = "filoz", "filozofia"
    FIZ = "fiz", "fizyka"
    GEOGR = "geogr", "geografia"
    HIST = "hist", "historia"
    HMUZ = "h.muz.", "historia muzyki"
    HSZT = "h.szt.", "historia sztuki"
    INF = "inf", "informatyka"
    POL = "pol", "język polski"
    MAT = "mat", "matematyka"
    WOS = "wos", "wiedza o społeczeństwie"
    OBCY = "obcy", "język obcy"


class LanguageName(Enum):
    ANG = "ang", "język angielski"
    FRA = "fra", "język francuski"
    HISZ = "hisz", "język hiszpański"
    NIEM = "niem", "język niemiecki"
    POR = "por", "język portugalski"
    ROS = "ros", "język rosyjski"
    WLO = "wlo", "język włoski"
    LAT = "lat", "język łaciński i kultura antyczna"
    BIA = "bia", "język białoruski"
    LIT = "lit", "język litewski"
    UKR = "ukr", "język ukraiński"
    LEM = "lem", "język łemkowski"
    KAS = "kas", "język kaszubski"


class LanguageLevel(Enum):
    ZERO = "0", "rozpoczynający naukę"
    P = "P", "kontynuujący naukę, poziom podstawowy"
    R = "R", "kontynuujący naukę, poziom rozszerzony"
    DJ = "DJ", "dwujęzyczny"


class LanguageNr(IntEnum):
    FIRST = 1
    SECOND = 2


@dataclass
class Language:
    nr: Optional[LanguageNr]
    level: Optional[LanguageLevel]
    name: LanguageName

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Language":
        if "name" not in data or data["name"] not in LanguageName.values():
            raise ValidationError(
                f"Language must have a 'name' key with one of values: {LanguageName.values()}."
            )
        if "nr" in data and str(data["nr"]) not in [
            str(val) for val in LanguageNr.values()
        ]:
            raise ValidationError(
                f"Optional 'nr' key must be one of: {LanguageNr.values()}."
            )
        if "level" in data and data["level"] not in LanguageLevel.values():
            raise ValidationError(
                f"Optional 'level' key must be one of: {LanguageLevel.values()}."
            )

        return Language(data.get("nr"), data.get("level"), data.get("name"))
