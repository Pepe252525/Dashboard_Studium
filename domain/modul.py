from dataclasses import dataclass, field

from domain.enums import Modulstatus
from domain.pruefungsleistung import Pruefungsleistung


@dataclass
class Modul:
    modulnummer: str
    bezeichnung: str
    ects: int
    status: Modulstatus = Modulstatus.GEPLANT
    pruefungsleistungen: list[Pruefungsleistung] = field(default_factory=list)

    @property
    def bestanden(self) -> bool:
        return (
            len(self.pruefungsleistungen) > 0
            and all(pruefung.bestanden for pruefung in self.pruefungsleistungen)
        )