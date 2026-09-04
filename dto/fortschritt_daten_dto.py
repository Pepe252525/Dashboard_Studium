from dataclasses import dataclass
from datetime import date


@dataclass
class FortschrittDatenDTO:
    datum: date
    soll_fortschritt: float
    ist_fortschritt: float | None