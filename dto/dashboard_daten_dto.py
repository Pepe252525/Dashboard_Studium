from dataclasses import dataclass

from dto.fortschritt_daten_dto import FortschrittDatenDTO
from dto.modul_daten_dto import ModulDatenDTO


@dataclass
class DashboardDatenDTO:
    gesamt_ects: int
    erreichte_ects: int
    verbleibende_ects: int
    fortschritt_prozent: float
    notendurchschnitt: float | None
    bestandene_module: int
    laufende_module: int
    module: list[ModulDatenDTO]
    fortschritt_verlauf: list[FortschrittDatenDTO]