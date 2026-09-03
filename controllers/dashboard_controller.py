from dto.dashboard_daten_dto import DashboardDatenDTO
from repositories.studien_repository import StudienRepository
from services.studien_service import StudienService


class DashboardController:
    def __init__(
        self,
        service: StudienService,
        repository: StudienRepository
    ):
        self.service = service
        self.repository = repository

    def lade_dashboard(self) -> DashboardDatenDTO:
        studiengang = self.repository.lade_studiengang()

        return DashboardDatenDTO(
            gesamt_ects=studiengang.gesamt_ects,
            erreichte_ects=self.service.berechne_erreichte_ects(
                studiengang
            ),
            verbleibende_ects=self.service.berechne_verbleibende_ects(
                studiengang
            ),
            fortschritt_prozent=self.service.berechne_fortschritt(
                studiengang
            ),
            notendurchschnitt=self.service.berechne_notendurchschnitt(
                studiengang
            ),
            bestandene_module=self.service.ermittle_bestandene_module(
                studiengang
            ),
            laufende_module=self.service.ermittle_laufende_module(
                studiengang
            )
        )

    def speichere_studiengang(self, studiengang) -> None:
        self.repository.speichere_studiengang(studiengang)