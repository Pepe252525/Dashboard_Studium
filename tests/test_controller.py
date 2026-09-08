from datetime import date

from controllers.dashboard_controller import (
    DashboardController,
)
from domain.enums import Modulstatus, Pruefungsart
from domain.modul import Modul
from domain.pruefungsleistung import Pruefungsleistung
from domain.semester import Semester
from domain.studiengang import Studiengang
from repositories.sqlite_studien_repository import (
    SQLiteStudienRepository,
)
from services.studien_service import StudienService


def test_dashboard_controller(
    tmp_path
):
    datenbank = (
        tmp_path
        / "controller_test.db"
    )

    repository = SQLiteStudienRepository(
        str(datenbank)
    )

    service = StudienService()

    studienstart = date(
        2023,
        7,
        17
    )

    pruefung = Pruefungsleistung(
        bezeichnung="Portfolio",
        pruefungsart=Pruefungsart.PORTFOLIO,
        note=2.0
    )

    bestandenes_modul = Modul(
        modulnummer="MOD01",
        bezeichnung="Bestandenes Modul",
        ects=10,
        status=Modulstatus.IN_BEARBEITUNG,
        pruefungsleistungen=[
            pruefung
        ]
    )

    laufendes_modul = Modul(
        modulnummer="MOD02",
        bezeichnung="Laufendes Modul",
        ects=5,
        status=Modulstatus.IN_BEARBEITUNG
    )

    semester = Semester(
        nummer=1,
        bezeichnung="1. Semester",
        studienstart=studienstart,
        module=[
            bestandenes_modul,
            laufendes_modul
        ]
    )

    studiengang = Studiengang(
        bezeichnung="Softwareentwicklung",
        gesamt_ects=180,
        startdatum=studienstart,
        regulaeres_enddatum=date(
            2026,
            7,
            17
        ),
        ziel_enddatum=date(
            2027,
            7,
            17
        ),
        zielnote=2.0,
        semester=[
            semester
        ]
    )

    repository.speichere_studiengang(
        studiengang
    )

    controller = DashboardController(
        service=service,
        repository=repository
    )

    dashboard_daten = (
        controller.lade_dashboard()
    )

    # ----------------------------------------------
    # Allgemeine Studiengangsdaten
    # ----------------------------------------------

    assert (
        dashboard_daten.studiengang_bezeichnung
        == "Softwareentwicklung"
    )

    assert (
        dashboard_daten.studienbeginn
        == date(2023, 7, 17)
    )

    assert (
        dashboard_daten.ziel_enddatum
        == date(2027, 7, 17)
    )

    assert (
        dashboard_daten.zielnote
        == 2.0
    )

    # ----------------------------------------------
    # Dashboard-Kennzahlen
    # ----------------------------------------------

    assert (
        dashboard_daten.gesamt_ects
        == 180
    )

    assert (
        dashboard_daten.erreichte_ects
        == 10
    )

    assert (
        dashboard_daten.verbleibende_ects
        == 170
    )

    assert (
        dashboard_daten.fortschritt_prozent
        == 5.56
    )

    assert (
        dashboard_daten.notendurchschnitt
        == 2.0
    )

    assert (
        dashboard_daten.bestandene_module
        == 1
    )

    assert (
        dashboard_daten.laufende_module
        == 1
    )

    # ----------------------------------------------
    # Modul-DTOs
    # ----------------------------------------------

    assert (
        len(
            dashboard_daten.module
        )
        == 2
    )

    erstes_modul = (
        dashboard_daten.module[0]
    )

    assert (
        erstes_modul.modulnummer
        == "MOD01"
    )

    assert (
        erstes_modul.bezeichnung
        == "Bestandenes Modul"
    )

    assert erstes_modul.semester == 1
    assert erstes_modul.ects == 10

    assert (
        erstes_modul.status
        == "Bestanden"
    )

    assert (
        erstes_modul.pruefungsleistungen
        == 1
    )

    assert erstes_modul.note == 2.0

    zweites_modul = (
        dashboard_daten.module[1]
    )

    assert (
        zweites_modul.modulnummer
        == "MOD02"
    )

    assert (
        zweites_modul.status
        == "In Bearbeitung"
    )

    assert (
        zweites_modul.note
        is None
    )

    # ----------------------------------------------
    # Soll-Ist-Verlauf
    # ----------------------------------------------

    assert (
        len(
            dashboard_daten.fortschritt_verlauf
        )
        > 0
    )

    assert (
        dashboard_daten.fortschritt_verlauf[0].datum
        == studienstart
    )