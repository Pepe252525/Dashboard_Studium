from datetime import date

from domain.enums import Modulstatus, Pruefungsart
from domain.modul import Modul
from domain.pruefungsleistung import Pruefungsleistung
from domain.semester import Semester
from domain.studiengang import Studiengang
from repositories.sqlite_studien_repository import SQLiteStudienRepository


def test_studiengang_speichern_und_laden(tmp_path):
    datenbank = tmp_path / "test_studypilot.db"

    repository = SQLiteStudienRepository(str(datenbank))

    studienstart = date(2023, 7, 17)

    pruefung = Pruefungsleistung(
        bezeichnung="Portfolio",
        pruefungsart=Pruefungsart.PORTFOLIO,
        pruefungsdatum=date(2024, 1, 10),
        note=2.0
    )

    modul = Modul(
        modulnummer="DLBDSOOFPP01",
        bezeichnung="Objektorientierte Programmierung mit Python",
        ects=5,
        status=Modulstatus.IN_BEARBEITUNG,
        pruefungsleistungen=[pruefung]
    )

    semester = Semester(
        nummer=1,
        bezeichnung="1. Semester",
        studienstart=studienstart,
        module=[modul]
    )

    studiengang = Studiengang(
        bezeichnung="Softwareentwicklung",
        gesamt_ects=180,
        startdatum=studienstart,
        regulaeres_enddatum=date(2026, 7, 17),
        ziel_enddatum=date(2027, 7, 17),
        zielnote=2.0,
        semester=[semester]
    )

    repository.speichere_studiengang(studiengang)

    geladener_studiengang = repository.lade_studiengang()

    assert geladener_studiengang.bezeichnung == "Softwareentwicklung"
    assert geladener_studiengang.gesamt_ects == 180
    assert geladener_studiengang.startdatum == date(2023, 7, 17)
    assert geladener_studiengang.regulaeres_enddatum == date(2026, 7, 17)
    assert geladener_studiengang.ziel_enddatum == date(2027, 7, 17)
    assert geladener_studiengang.zielnote == 2.0

    assert len(geladener_studiengang.semester) == 1

    geladenes_semester = geladener_studiengang.semester[0]

    assert geladenes_semester.nummer == 1
    assert geladenes_semester.bezeichnung == "1. Semester"
    assert geladenes_semester.studienstart == studienstart
    assert geladenes_semester.startdatum == date(2023, 7, 17)
    assert geladenes_semester.enddatum == date(2024, 1, 16)

    assert len(geladenes_semester.module) == 1

    geladenes_modul = geladenes_semester.module[0]

    assert geladenes_modul.modulnummer == "DLBDSOOFPP01"
    assert geladenes_modul.bezeichnung == (
        "Objektorientierte Programmierung mit Python"
    )
    assert geladenes_modul.ects == 5
    assert geladenes_modul.status == Modulstatus.IN_BEARBEITUNG
    assert geladenes_modul.bestanden is True

    assert len(geladenes_modul.pruefungsleistungen) == 1

    geladene_pruefung = geladenes_modul.pruefungsleistungen[0]

    assert geladene_pruefung.bezeichnung == "Portfolio"
    assert geladene_pruefung.pruefungsart == Pruefungsart.PORTFOLIO
    assert geladene_pruefung.pruefungsdatum == date(2024, 1, 10)
    assert geladene_pruefung.note == 2.0
    assert geladene_pruefung.bestanden is True