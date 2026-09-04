from datetime import date

from domain.enums import Modulstatus, Pruefungsart
from domain.modul import Modul
from domain.pruefungsleistung import Pruefungsleistung
from domain.semester import Semester
from domain.studiengang import Studiengang
from services.studien_service import StudienService


def erstelle_test_studiengang() -> Studiengang:
    studienstart = date(2023, 7, 17)

    bestandene_pruefung = Pruefungsleistung(
        bezeichnung="Portfolio",
        pruefungsart=Pruefungsart.PORTFOLIO,
        note=2.0
    )

    laufende_pruefung = Pruefungsleistung(
        bezeichnung="Klausur",
        pruefungsart=Pruefungsart.KLAUSUR
    )

    bestandenes_modul = Modul(
        modulnummer="MOD01",
        bezeichnung="Bestandenes Modul",
        ects=10,
        status=Modulstatus.IN_BEARBEITUNG,
        pruefungsleistungen=[bestandene_pruefung]
    )

    laufendes_modul = Modul(
        modulnummer="MOD02",
        bezeichnung="Laufendes Modul",
        ects=5,
        status=Modulstatus.IN_BEARBEITUNG,
        pruefungsleistungen=[laufende_pruefung]
    )

    semester = Semester(
        nummer=1,
        bezeichnung="1. Semester",
        studienstart=studienstart,
        module=[bestandenes_modul, laufendes_modul]
    )

    return Studiengang(
        bezeichnung="Softwareentwicklung",
        gesamt_ects=180,
        startdatum=studienstart,
        regulaeres_enddatum=date(2026, 7, 17),
        ziel_enddatum=date(2027, 7, 17),
        zielnote=2.0,
        semester=[semester]
    )


def test_berechne_erreichte_ects():
    service = StudienService()
    studiengang = erstelle_test_studiengang()

    assert service.berechne_erreichte_ects(studiengang) == 10


def test_berechne_verbleibende_ects():
    service = StudienService()
    studiengang = erstelle_test_studiengang()

    assert service.berechne_verbleibende_ects(studiengang) == 170


def test_berechne_fortschritt():
    service = StudienService()
    studiengang = erstelle_test_studiengang()

    assert service.berechne_fortschritt(studiengang) == 5.56


def test_berechne_notendurchschnitt():
    service = StudienService()
    studiengang = erstelle_test_studiengang()

    assert service.berechne_notendurchschnitt(studiengang) == 2.0


def test_ermittle_bestandene_module():
    service = StudienService()
    studiengang = erstelle_test_studiengang()

    assert service.ermittle_bestandene_module(studiengang) == 1


def test_ermittle_laufende_module():
    service = StudienService()
    studiengang = erstelle_test_studiengang()

    assert service.ermittle_laufende_module(studiengang) == 1


def test_berechne_soll_ist_abweichung():
    service = StudienService()
    studiengang = erstelle_test_studiengang()

    abweichung = service.berechne_soll_ist_abweichung(
        studiengang,
        date(2024, 7, 17)
    )

    assert isinstance(abweichung, float)
    
def test_erreichte_ects_am_datum():
    service = StudienService()

    studienstart = date(2023, 7, 17)

    pruefung = Pruefungsleistung(
        bezeichnung="Portfolio",
        pruefungsart=Pruefungsart.PORTFOLIO,
        pruefungsdatum=date(2024, 1, 10),
        note=2.0
    )

    modul = Modul(
        modulnummer="MOD01",
        bezeichnung="Testmodul",
        ects=10,
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

    assert (
        service.berechne_erreichte_ects_am_datum(
            studiengang,
            date(2024, 1, 9)
        )
        == 0
    )

    assert (
        service.berechne_erreichte_ects_am_datum(
            studiengang,
            date(2024, 1, 10)
        )
        == 10
    )


def test_modul_mit_mehreren_pruefungen():
    service = StudienService()

    studienstart = date(2023, 7, 17)

    pruefung_1 = Pruefungsleistung(
        bezeichnung="Klausur",
        pruefungsart=Pruefungsart.KLAUSUR,
        pruefungsdatum=date(2024, 1, 10),
        note=2.0
    )

    pruefung_2 = Pruefungsleistung(
        bezeichnung="Projekt",
        pruefungsart=Pruefungsart.PROJEKTARBEIT,
        pruefungsdatum=date(2024, 2, 15),
        note=2.3
    )

    modul = Modul(
        modulnummer="MOD02",
        bezeichnung="Testmodul",
        ects=10,
        pruefungsleistungen=[
            pruefung_1,
            pruefung_2
        ]
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

    assert (
        service.berechne_erreichte_ects_am_datum(
            studiengang,
            date(2024, 2, 14)
        )
        == 0
    )

    assert (
        service.berechne_erreichte_ects_am_datum(
            studiengang,
            date(2024, 2, 15)
        )
        == 10
    )


def test_soll_fortschritt():
    service = StudienService()

    studiengang = Studiengang(
        bezeichnung="Test",
        gesamt_ects=180,
        startdatum=date(2024, 1, 1),
        regulaeres_enddatum=date(2025, 1, 1),
        ziel_enddatum=date(2025, 1, 1),
        zielnote=2.0
    )

    assert (
        service.berechne_soll_fortschritt(
            studiengang,
            date(2024, 1, 1)
        )
        == 0.0
    )

    assert (
        service.berechne_soll_fortschritt(
            studiengang,
            date(2025, 1, 1)
        )
        == 100.0
    )