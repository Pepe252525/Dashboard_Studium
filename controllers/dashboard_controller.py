from datetime import date

from dto.dashboard_daten_dto import DashboardDatenDTO
from dto.fortschritt_daten_dto import FortschrittDatenDTO
from dto.modul_daten_dto import ModulDatenDTO
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

        module = self._erstelle_modul_daten(
            studiengang
        )

        fortschritt_verlauf = (
            self._erstelle_fortschritt_verlauf(
                studiengang
            )
        )

        return DashboardDatenDTO(
            gesamt_ects=studiengang.gesamt_ects,

            erreichte_ects=(
                self.service.berechne_erreichte_ects(
                    studiengang
                )
            ),

            verbleibende_ects=(
                self.service.berechne_verbleibende_ects(
                    studiengang
                )
            ),

            fortschritt_prozent=(
                self.service.berechne_fortschritt(
                    studiengang
                )
            ),

            notendurchschnitt=(
                self.service.berechne_notendurchschnitt(
                    studiengang
                )
            ),

            bestandene_module=(
                self.service.ermittle_bestandene_module(
                    studiengang
                )
            ),

            laufende_module=(
                self.service.ermittle_laufende_module(
                    studiengang
                )
            ),

            module=module,

            fortschritt_verlauf=fortschritt_verlauf
        )

    def speichere_studiengang(
        self,
        studiengang
    ) -> None:
        self.repository.speichere_studiengang(
            studiengang
        )

    def _erstelle_modul_daten(
        self,
        studiengang
    ) -> list[ModulDatenDTO]:

        module = []

        for semester in studiengang.semester:
            for modul in semester.module:

                noten = [
                    pruefung.note
                    for pruefung
                    in modul.pruefungsleistungen
                    if pruefung.note is not None
                ]

                note = None

                if noten:
                    note = round(
                        sum(noten) / len(noten),
                        2
                    )

                if modul.bestanden:
                    status = "Bestanden"
                else:
                    status = modul.status.value

                module.append(
                    ModulDatenDTO(
                        modulnummer=modul.modulnummer,
                        bezeichnung=modul.bezeichnung,
                        semester=semester.nummer,
                        ects=modul.ects,
                        status=status,
                        pruefungsleistungen=len(
                            modul.pruefungsleistungen
                        ),
                        note=note
                    )
                )

        return module

    def _erstelle_fortschritt_verlauf(
        self,
        studiengang
    ) -> list[FortschrittDatenDTO]:

        verlauf = []

        aktuelles_datum = (
            studiengang.startdatum
        )

        heute = date.today()

        enddatum = (
            studiengang.ziel_enddatum
        )

        while aktuelles_datum <= enddatum:

            soll_fortschritt = (
                self.service.berechne_soll_fortschritt(
                    studiengang,
                    aktuelles_datum
                )
            )

            if aktuelles_datum <= heute:
                ist_fortschritt = (
                    self.service.berechne_fortschritt_am_datum(
                        studiengang,
                        aktuelles_datum
                    )
                )
            else:
                ist_fortschritt = None

            verlauf.append(
                FortschrittDatenDTO(
                    datum=aktuelles_datum,
                    soll_fortschritt=soll_fortschritt,
                    ist_fortschritt=ist_fortschritt
                )
            )

            aktuelles_datum = (
                self._naechster_monat(
                    aktuelles_datum
                )
            )

        # Falls das heutige Datum nicht genau auf einen
        # monatlichen Stichtag fällt, wird es zusätzlich
        # in den Verlauf aufgenommen.
        if (
            studiengang.startdatum
            <= heute
            <= studiengang.ziel_enddatum
            and all(
                punkt.datum != heute
                for punkt in verlauf
            )
        ):
            verlauf.append(
                FortschrittDatenDTO(
                    datum=heute,

                    soll_fortschritt=(
                        self.service.berechne_soll_fortschritt(
                            studiengang,
                            heute
                        )
                    ),

                    ist_fortschritt=(
                        self.service.berechne_fortschritt_am_datum(
                            studiengang,
                            heute
                        )
                    )
                )
            )

            verlauf.sort(
                key=lambda punkt: punkt.datum
            )

        return verlauf

    def _naechster_monat(
        self,
        datum: date
    ) -> date:

        jahr = datum.year
        monat = datum.month + 1

        if monat > 12:
            monat = 1
            jahr += 1

        tag = datum.day

        while True:
            try:
                return date(
                    jahr,
                    monat,
                    tag
                )

            except ValueError:
                tag -= 1