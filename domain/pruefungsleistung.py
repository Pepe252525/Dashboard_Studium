from dataclasses import dataclass
from datetime import date

from domain.enums import Pruefungsart


@dataclass
class Pruefungsleistung:
    bezeichnung: str
    pruefungsart: Pruefungsart
    pruefungsdatum: date | None = None
    note: float | None = None

    @property
    def bestanden(self) -> bool:
        return self.note is not None and self.note <= 4.0

    def ist_bewertet(self) -> bool:
        return self.note is not None