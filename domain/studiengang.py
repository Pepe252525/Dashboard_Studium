from dataclasses import dataclass, field
from datetime import date

from domain.semester import Semester


@dataclass
class Studiengang:
    bezeichnung: str
    gesamt_ects: int
    startdatum: date
    regulaeres_enddatum: date
    ziel_enddatum: date
    zielnote: float
    semester: list[Semester] = field(default_factory=list)