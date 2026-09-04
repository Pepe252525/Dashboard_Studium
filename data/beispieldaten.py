from datetime import date

from domain.enums import Modulstatus, Pruefungsart
from domain.modul import Modul
from domain.pruefungsleistung import Pruefungsleistung
from domain.semester import Semester
from domain.studiengang import Studiengang


def erstelle_beispiel_studiengang() -> Studiengang:
    studienstart = date(2023, 7, 17)

    pruefung_1 = Pruefungsleistung(
        bezeichnung="Portfolio",
        pruefungsart=Pruefungsart.PORTFOLIO,
        pruefungsdatum=date(2024, 1, 10),
        note=2.0
    )

    pruefung_2 = Pruefungsleistung(
        bezeichnung="Klausur",
        pruefungsart=Pruefungsart.KLAUSUR,
        pruefungsdatum=date(2024, 6, 20),
        note=2.3
    )

    pruefung_3 = Pruefungsleistung(
        bezeichnung="Projektarbeit",
        pruefungsart=Pruefungsart.PROJEKTARBEIT
    )

    modul_1 = Modul(
        modulnummer="DLBDSOOFPP01",
        bezeichnung="Objektorientierte Programmierung mit Python",
        ects=5,
        status=Modulstatus.IN_BEARBEITUNG,
        pruefungsleistungen=[pruefung_1]
    )

    modul_2 = Modul(
        modulnummer="DLBSE",
        bezeichnung="Software Engineering",
        ects=5,
        status=Modulstatus.IN_BEARBEITUNG,
        pruefungsleistungen=[pruefung_2]
    )

    modul_3 = Modul(
        modulnummer="DLBPROG",
        bezeichnung="Programmierung",
        ects=5,
        status=Modulstatus.IN_BEARBEITUNG,
        pruefungsleistungen=[pruefung_3]
    )

    semester_1 = Semester(
        nummer=1,
        bezeichnung="1. Semester",
        studienstart=studienstart,
        module=[
            modul_1,
            modul_2
        ]
    )

    semester_2 = Semester(
        nummer=2,
        bezeichnung="2. Semester",
        studienstart=studienstart,
        module=[
            modul_3
        ]
    )

    return Studiengang(
        bezeichnung="Softwareentwicklung",
        gesamt_ects=180,
        startdatum=studienstart,
        regulaeres_enddatum=date(2026, 7, 17),
        ziel_enddatum=date(2027, 7, 17),
        zielnote=2.0,
        semester=[
            semester_1,
            semester_2
        ]
    )