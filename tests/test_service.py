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