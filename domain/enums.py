from enum import Enum


class Modulstatus(Enum):
    GEPLANT = "Geplant"
    IN_BEARBEITUNG = "In Bearbeitung"


class Pruefungsart(Enum):
    KLAUSUR = "Klausur"
    PROJEKTARBEIT = "Projektarbeit"
    HAUSARBEIT = "Hausarbeit"
    PORTFOLIO = "Portfolio"
    PRAESENTATION = "Präsentation"
    SONSTIGE = "Sonstige"