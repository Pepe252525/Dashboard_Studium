import sqlite3
from datetime import date
from pathlib import Path

from domain.enums import Modulstatus, Pruefungsart
from domain.modul import Modul
from domain.pruefungsleistung import Pruefungsleistung
from domain.semester import Semester
from domain.studiengang import Studiengang
from repositories.studien_repository import StudienRepository


class SQLiteStudienRepository(StudienRepository):

    def __init__(self, dateipfad: str = "data/studypilot.db"):
        self.dateipfad = dateipfad

        Path(self.dateipfad).parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self._erstelle_tabellen()

    def _verbinde(self) -> sqlite3.Connection:
        verbindung = sqlite3.connect(self.dateipfad)
        verbindung.row_factory = sqlite3.Row
        return verbindung

    def _erstelle_tabellen(self) -> None:
        with self._verbinde() as verbindung:
            cursor = verbindung.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS studiengang (
                    id INTEGER PRIMARY KEY,
                    bezeichnung TEXT NOT NULL,
                    gesamt_ects INTEGER NOT NULL,
                    startdatum TEXT NOT NULL,
                    regulaeres_enddatum TEXT NOT NULL,
                    ziel_enddatum TEXT NOT NULL,
                    zielnote REAL NOT NULL
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS semester (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    studiengang_id INTEGER NOT NULL,
                    nummer INTEGER NOT NULL,
                    bezeichnung TEXT NOT NULL,
                    studienstart TEXT NOT NULL,
                    FOREIGN KEY (studiengang_id)
                        REFERENCES studiengang(id)
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS modul (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    semester_id INTEGER NOT NULL,
                    modulnummer TEXT NOT NULL,
                    bezeichnung TEXT NOT NULL,
                    ects INTEGER NOT NULL,
                    status TEXT NOT NULL,
                    FOREIGN KEY (semester_id)
                        REFERENCES semester(id)
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS pruefungsleistung (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    modul_id INTEGER NOT NULL,
                    bezeichnung TEXT NOT NULL,
                    pruefungsart TEXT NOT NULL,
                    pruefungsdatum TEXT,
                    note REAL,
                    FOREIGN KEY (modul_id)
                        REFERENCES modul(id)
                )
            """)

    def speichere_studiengang(
        self,
        studiengang: Studiengang
    ) -> None:

        with self._verbinde() as verbindung:
            cursor = verbindung.cursor()

            # Für den Prototypen wird genau ein Studiengang verwaltet.
            # Deshalb werden vorhandene Daten vor dem Speichern ersetzt.
            cursor.execute("DELETE FROM pruefungsleistung")
            cursor.execute("DELETE FROM modul")
            cursor.execute("DELETE FROM semester")
            cursor.execute("DELETE FROM studiengang")

            cursor.execute(
                """
                INSERT INTO studiengang (
                    id,
                    bezeichnung,
                    gesamt_ects,
                    startdatum,
                    regulaeres_enddatum,
                    ziel_enddatum,
                    zielnote
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    1,
                    studiengang.bezeichnung,
                    studiengang.gesamt_ects,
                    studiengang.startdatum.isoformat(),
                    studiengang.regulaeres_enddatum.isoformat(),
                    studiengang.ziel_enddatum.isoformat(),
                    studiengang.zielnote
                )
            )

            for semester in studiengang.semester:
                cursor.execute(
                    """
                    INSERT INTO semester (
                        studiengang_id,
                        nummer,
                        bezeichnung,
                        studienstart
                    )
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        1,
                        semester.nummer,
                        semester.bezeichnung,
                        semester.studienstart.isoformat()
                    )
                )

                semester_id = cursor.lastrowid

                for modul in semester.module:
                    cursor.execute(
                        """
                        INSERT INTO modul (
                            semester_id,
                            modulnummer,
                            bezeichnung,
                            ects,
                            status
                        )
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (
                            semester_id,
                            modul.modulnummer,
                            modul.bezeichnung,
                            modul.ects,
                            modul.status.name
                        )
                    )

                    modul_id = cursor.lastrowid

                    for pruefung in modul.pruefungsleistungen:
                        cursor.execute(
                            """
                            INSERT INTO pruefungsleistung (
                                modul_id,
                                bezeichnung,
                                pruefungsart,
                                pruefungsdatum,
                                note
                            )
                            VALUES (?, ?, ?, ?, ?)
                            """,
                            (
                                modul_id,
                                pruefung.bezeichnung,
                                pruefung.pruefungsart.name,
                                (
                                    pruefung.pruefungsdatum.isoformat()
                                    if pruefung.pruefungsdatum
                                    else None
                                ),
                                pruefung.note
                            )
                        )

    def lade_studiengang(self) -> Studiengang:
        with self._verbinde() as verbindung:
            cursor = verbindung.cursor()

            studiengang_daten = cursor.execute(
                "SELECT * FROM studiengang LIMIT 1"
            ).fetchone()

            if studiengang_daten is None:
                raise ValueError(
                    "Es ist noch kein Studiengang gespeichert."
                )

            semester_liste = []

            semester_daten = cursor.execute(
                """
                SELECT *
                FROM semester
                WHERE studiengang_id = ?
                ORDER BY nummer
                """,
                (studiengang_daten["id"],)
            ).fetchall()

            for semester_zeile in semester_daten:
                modul_liste = []

                modul_daten = cursor.execute(
                    """
                    SELECT *
                    FROM modul
                    WHERE semester_id = ?
                    ORDER BY id
                    """,
                    (semester_zeile["id"],)
                ).fetchall()

                for modul_zeile in modul_daten:
                    pruefungen = []

                    pruefungsdaten = cursor.execute(
                        """
                        SELECT *
                        FROM pruefungsleistung
                        WHERE modul_id = ?
                        ORDER BY id
                        """,
                        (modul_zeile["id"],)
                    ).fetchall()

                    for pruefungszeile in pruefungsdaten:
                        pruefungen.append(
                            Pruefungsleistung(
                                bezeichnung=pruefungszeile[
                                    "bezeichnung"
                                ],
                                pruefungsart=Pruefungsart[
                                    pruefungszeile["pruefungsart"]
                                ],
                                pruefungsdatum=(
                                    date.fromisoformat(
                                        pruefungszeile[
                                            "pruefungsdatum"
                                        ]
                                    )
                                    if pruefungszeile[
                                        "pruefungsdatum"
                                    ]
                                    else None
                                ),
                                note=pruefungszeile["note"]
                            )
                        )

                    modul_liste.append(
                        Modul(
                            modulnummer=modul_zeile[
                                "modulnummer"
                            ],
                            bezeichnung=modul_zeile[
                                "bezeichnung"
                            ],
                            ects=modul_zeile["ects"],
                            status=Modulstatus[
                                modul_zeile["status"]
                            ],
                            pruefungsleistungen=pruefungen
                        )
                    )

                semester_liste.append(
                    Semester(
                        nummer=semester_zeile["nummer"],
                        bezeichnung=semester_zeile[
                            "bezeichnung"
                        ],
                        studienstart=date.fromisoformat(
                            semester_zeile["studienstart"]
                        ),
                        module=modul_liste
                    )
                )

            return Studiengang(
                bezeichnung=studiengang_daten["bezeichnung"],
                gesamt_ects=studiengang_daten["gesamt_ects"],
                startdatum=date.fromisoformat(
                    studiengang_daten["startdatum"]
                ),
                regulaeres_enddatum=date.fromisoformat(
                    studiengang_daten["regulaeres_enddatum"]
                ),
                ziel_enddatum=date.fromisoformat(
                    studiengang_daten["ziel_enddatum"]
                ),
                zielnote=studiengang_daten["zielnote"],
                semester=semester_liste
            )