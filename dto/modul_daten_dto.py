from dataclasses import dataclass


@dataclass
class ModulDatenDTO:
    modulnummer: str
    bezeichnung: str
    semester: int
    ects: int
    status: str
    pruefungsleistungen: int
    note: float | None