import sys

from PySide6.QtWidgets import QApplication

from controllers.dashboard_controller import DashboardController
from data.beispieldaten import erstelle_beispiel_studiengang
from repositories.sqlite_studien_repository import SQLiteStudienRepository
from services.studien_service import StudienService
from views.dashboard_view import DashboardView


class StudyPilotApp:

    def start(self) -> None:
        app = QApplication(sys.argv)

        repository = SQLiteStudienRepository()
        service = StudienService()

        try:
            repository.lade_studiengang()
        except ValueError:
            beispiel_studiengang = erstelle_beispiel_studiengang()
            repository.speichere_studiengang(beispiel_studiengang)

        controller = DashboardController(
            service=service,
            repository=repository
        )

        view = DashboardView()

        dashboard_daten = controller.lade_dashboard()
        view.zeige_dashboard(dashboard_daten)

        view.show()

        sys.exit(app.exec())