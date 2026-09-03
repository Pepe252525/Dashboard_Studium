from dataclasses import dataclass, field
from datetime import date, timedelta

from domain.modul import Modul


@dataclass
class Semester:
    nummer: int
    bezeichnung: str
    studienstart: date
    module: list[Modul] = field(default_factory=list)

    @property
    def startdatum(self) -> date:
        monate = (self.nummer - 1) * 6
        jahr = self.studienstart.year + (
            self.studienstart.month - 1 + monate
        ) // 12
        monat = (
            self.studienstart.month - 1 + monate
        ) % 12 + 1

        return date(jahr, monat, self.studienstart.day)

    @property
    def enddatum(self) -> date:
        monate = self.nummer * 6
        jahr = self.studienstart.year + (
            self.studienstart.month - 1 + monate
        ) // 12
        monat = (
            self.studienstart.month - 1 + monate
        ) % 12 + 1

        naechstes_semester = date(
            jahr,
            monat,
            self.studienstart.day
        )

        return naechstes_semester - timedelta(days=1)