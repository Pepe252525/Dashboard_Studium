from datetime import date

from domain.enums import Modulstatus
from domain.modul import Modul
from domain.studiengang import Studiengang


class StudienService:

    def berechne_erreichte_ects(
        self,
        studiengang: Studiengang
    ) -> int:
        return sum(
            modul.ects
            for semester in studiengang.semester
            for modul in semester.module
            if modul.bestanden
        )

    def berechne_verbleibende_ects(
        self,
        studiengang: Studiengang
    ) -> int:
        erreichte_ects = self.berechne_erreichte_ects(
            studiengang
        )

        return max(
            studiengang.gesamt_ects - erreichte_ects,
            0
        )

    def berechne_fortschritt(
        self,
        studiengang: Studiengang
    ) -> float:
        if studiengang.gesamt_ects <= 0:
            return 0.0

        erreichte_ects = self.berechne_erreichte_ects(
            studiengang
        )

        return round(
            erreichte_ects
            / studiengang.gesamt_ects
            * 100,
            2
        )

    def berechne_notendurchschnitt(
        self,
        studiengang: Studiengang
    ) -> float | None:
        noten = [
            pruefung.note
            for semester in studiengang.semester
            for modul in semester.module
            for pruefung in modul.pruefungsleistungen
            if pruefung.note is not None
        ]

        if not noten:
            return None

        return round(
            sum(noten) / len(noten),
            2
        )

    def ermittle_bestandene_module(
        self,
        studiengang: Studiengang
    ) -> int:
        return sum(
            1
            for semester in studiengang.semester
            for modul in semester.module
            if modul.bestanden
        )

    def ermittle_laufende_module(
        self,
        studiengang: Studiengang
    ) -> int:
        return sum(
            1
            for semester in studiengang.semester
            for modul in semester.module
            if (
                modul.status
                == Modulstatus.IN_BEARBEITUNG
                and not modul.bestanden
            )
        )

    # --------------------------------------------------
    # Historischer Studienfortschritt
    # --------------------------------------------------

    def berechne_erreichte_ects_am_datum(
        self,
        studiengang: Studiengang,
        datum: date
    ) -> int:
        erreichte_ects = 0

        for semester in studiengang.semester:
            for modul in semester.module:

                abschlussdatum = (
                    self._ermittle_modul_abschlussdatum(
                        modul
                    )
                )

                if (
                    abschlussdatum is not None
                    and abschlussdatum <= datum
                ):
                    erreichte_ects += modul.ects

        return erreichte_ects

    def berechne_fortschritt_am_datum(
        self,
        studiengang: Studiengang,
        datum: date
    ) -> float:
        if studiengang.gesamt_ects <= 0:
            return 0.0

        erreichte_ects = (
            self.berechne_erreichte_ects_am_datum(
                studiengang,
                datum
            )
        )

        return round(
            erreichte_ects
            / studiengang.gesamt_ects
            * 100,
            2
        )

    def berechne_soll_fortschritt(
        self,
        studiengang: Studiengang,
        datum: date
    ) -> float:
        gesamtdauer = (
            studiengang.ziel_enddatum
            - studiengang.startdatum
        ).days

        if gesamtdauer <= 0:
            return 0.0

        vergangene_tage = (
            datum - studiengang.startdatum
        ).days

        anteil = vergangene_tage / gesamtdauer

        anteil = max(
            0.0,
            min(
                anteil,
                1.0
            )
        )

        return round(
            anteil * 100,
            2
        )

    def berechne_soll_ist_abweichung(
        self,
        studiengang: Studiengang,
        datum: date
    ) -> float:
        soll_fortschritt = (
            self.berechne_soll_fortschritt(
                studiengang,
                datum
            )
        )

        ist_fortschritt = (
            self.berechne_fortschritt_am_datum(
                studiengang,
                datum
            )
        )

        return round(
            ist_fortschritt
            - soll_fortschritt,
            2
        )

    # --------------------------------------------------
    # Private Hilfsmethode
    # --------------------------------------------------

    def _ermittle_modul_abschlussdatum(
        self,
        modul: Modul
    ) -> date | None:

        if not modul.pruefungsleistungen:
            return None

        pruefungsdaten = []

        for pruefung in modul.pruefungsleistungen:

            if not pruefung.bestanden:
                return None

            if pruefung.pruefungsdatum is None:
                return None

            pruefungsdaten.append(
                pruefung.pruefungsdatum
            )

        return max(
            pruefungsdaten
        )