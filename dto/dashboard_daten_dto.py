from dataclasses import dataclass


@dataclass
class DashboardDatenDTO:
    gesamt_ects: int
    erreichte_ects: int
    verbleibende_ects: int
    fortschritt_prozent: float
    notendurchschnitt: float | None
    bestandene_module: int
    laufende_module: int