from datetime import date

from domain.enums import Modulstatus
from domain.studiengang import Studiengang


class StudienService:

    def berechne_erreichte_ects(self, studiengang: Studiengang) -> int:
        return sum(
            modul.ects
            for semester in studiengang.semester
            for modul in semester.module
            if modul.bestanden
        )

    def berechne_verbleibende_ects(self, studiengang: Studiengang) -> int:
        erreichte_ects = self.berechne_erreichte_ects(studiengang)
        return studiengang.gesamt_ects - erreichte_ects

    def berechne_fortschritt(self, studiengang: Studiengang) -> float:
        if studiengang.gesamt_ects == 0:
            return 0.0

        erreichte_ects = self.berechne_erreichte_ects(studiengang)

        return round(
            erreichte_ects / studiengang.gesamt_ects * 100,
            2
        )

    def berechne_notendurchschnitt(self, studiengang: Studiengang) -> float | None:
        noten = [
            pruefung.note
            for semester in studiengang.semester
            for modul in semester.module
            for pruefung in modul.pruefungsleistungen
            if pruefung.note is not None
        ]

        if not noten:
            return None

        return round(sum(noten) / len(noten), 2)

    def ermittle_bestandene_module(self, studiengang: Studiengang) -> int:
        return sum(
            1
            for semester in studiengang.semester
            for modul in semester.module
            if modul.bestanden
        )

    def ermittle_laufende_module(self, studiengang: Studiengang) -> int:
        return sum(
            1
            for semester in studiengang.semester
            for modul in semester.module
            if modul.status == Modulstatus.IN_BEARBEITUNG
            and not modul.bestanden
        )

    def berechne_soll_ist_abweichung(
        self,
        studiengang: Studiengang,
        datum: date
    ) -> float:
        gesamtdauer = (
            studiengang.ziel_enddatum - studiengang.startdatum
        ).days

        if gesamtdauer <= 0:
            return 0.0

        vergangene_tage = (
            datum - studiengang.startdatum
        ).days

        soll_fortschritt = max(
            0.0,
            min(
                vergangene_tage / gesamtdauer * 100,
                100.0
            )
        )

        ist_fortschritt = self.berechne_fortschritt(studiengang)

        return round(
            ist_fortschritt - soll_fortschritt,
            2
        )