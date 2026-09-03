from datetime import date

from controllers.dashboard_controller import DashboardController
from domain.enums import Modulstatus, Pruefungsart
from domain.modul import Modul
from domain.pruefungsleistung import Pruefungsleistung
from domain.semester import Semester
from domain.studiengang import Studiengang
from repositories.sqlite_studien_repository import SQLiteStudienRepository
from services.studien_service import StudienService


def test_dashboard_controller(tmp_path):
    datenbank = tmp_path / "controller_test.db"

    repository = SQLiteStudienRepository(str(datenbank))
    service = StudienService()

    studienstart = date(2023, 7, 17)

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
        pruefungsleistungen=[pruefung]
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
        regulaeres_enddatum=date(2026, 7, 17),
        ziel_enddatum=date(2027, 7, 17),
        zielnote=2.0,
        semester=[semester]
    )

    repository.speichere_studiengang(studiengang)

    controller = DashboardController(
        service=service,
        repository=repository
    )

    dashboard_daten = controller.lade_dashboard()

    assert dashboard_daten.gesamt_ects == 180
    assert dashboard_daten.erreichte_ects == 10
    assert dashboard_daten.verbleibende_ects == 170
    assert dashboard_daten.fortschritt_prozent == 5.56
    assert dashboard_daten.notendurchschnitt == 2.0
    assert dashboard_daten.bestandene_module == 1
    assert dashboard_daten.laufende_module == 1