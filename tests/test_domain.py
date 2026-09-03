from datetime import date

from domain.enums import Modulstatus, Pruefungsart
from domain.modul import Modul
from domain.pruefungsleistung import Pruefungsleistung
from domain.semester import Semester
from domain.studiengang import Studiengang


def test_pruefungsleistung_bestanden():
    pruefung = Pruefungsleistung(
        bezeichnung="Portfolio",
        pruefungsart=Pruefungsart.PORTFOLIO,
        note=2.0
    )

    assert pruefung.ist_bewertet() is True
    assert pruefung.bestanden is True


def test_pruefungsleistung_nicht_bestanden():
    pruefung = Pruefungsleistung(
        bezeichnung="Klausur",
        pruefungsart=Pruefungsart.KLAUSUR,
        note=5.0
    )

    assert pruefung.ist_bewertet() is True
    assert pruefung.bestanden is False


def test_unbewertete_pruefungsleistung():
    pruefung = Pruefungsleistung(
        bezeichnung="Hausarbeit",
        pruefungsart=Pruefungsart.HAUSARBEIT
    )

    assert pruefung.ist_bewertet() is False
    assert pruefung.bestanden is False


def test_modul_bestanden():
    pruefung = Pruefungsleistung(
        bezeichnung="Portfolio",
        pruefungsart=Pruefungsart.PORTFOLIO,
        note=2.0
    )

    modul = Modul(
        modulnummer="TEST01",
        bezeichnung="Testmodul",
        ects=5,
        status=Modulstatus.IN_BEARBEITUNG,
        pruefungsleistungen=[pruefung]
    )

    assert modul.bestanden is True


def test_modul_ohne_pruefungsleistung_nicht_bestanden():
    modul = Modul(
        modulnummer="TEST02",
        bezeichnung="Testmodul",
        ects=5
    )

    assert modul.bestanden is False


def test_semester_daten():
    studienstart = date(2023, 7, 17)

    semester = Semester(
        nummer=2,
        bezeichnung="2. Semester",
        studienstart=studienstart
    )

    assert semester.startdatum == date(2024, 1, 17)
    assert semester.enddatum == date(2024, 7, 16)


def test_studiengang_enthaelt_semester():
    studienstart = date(2023, 7, 17)

    semester = Semester(
        nummer=1,
        bezeichnung="1. Semester",
        studienstart=studienstart
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

    assert len(studiengang.semester) == 1
    assert studiengang.semester[0].nummer == 1