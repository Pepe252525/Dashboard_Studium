from PySide6.QtCore import Qt, QRectF, QPointF
from PySide6.QtGui import (
    QColor,
    QFont,
    QPainter,
    QPainterPath,
    QPen,
)
from PySide6.QtWidgets import (
    QAbstractItemView,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMainWindow,
    QSizePolicy,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from dto.dashboard_daten_dto import DashboardDatenDTO


# ==========================================================
# Runder Fortschrittsindikator
# ==========================================================

class CircularProgress(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self._wert = 0.0

        self.setMinimumSize(190, 190)
        self.setMaximumSize(220, 220)

        self.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Fixed
        )

    def set_wert(self, wert: float) -> None:
        self._wert = max(
            0.0,
            min(wert, 100.0)
        )

        self.update()

    def paintEvent(self, event) -> None:
        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )

        breite = min(
            self.width(),
            self.height()
        )

        rand = 18

        rechteck = QRectF(
            rand,
            rand,
            breite - rand * 2,
            breite - rand * 2
        )

        # Hintergrundkreis
        hintergrund_stift = QPen(
            QColor("#334155"),
            16
        )

        hintergrund_stift.setCapStyle(
            Qt.PenCapStyle.RoundCap
        )

        painter.setPen(
            hintergrund_stift
        )

        painter.drawArc(
            rechteck,
            0,
            360 * 16
        )

        # Fortschritt
        fortschritt_stift = QPen(
            QColor("#3B82F6"),
            16
        )

        fortschritt_stift.setCapStyle(
            Qt.PenCapStyle.RoundCap
        )

        painter.setPen(
            fortschritt_stift
        )

        winkel = int(
            -360 * 16
            * self._wert
            / 100
        )

        painter.drawArc(
            rechteck,
            90 * 16,
            winkel
        )

        # Prozentwert
        painter.setPen(
            QColor("#F8FAFC")
        )

        font = QFont("Segoe UI")
        font.setPointSize(22)
        font.setBold(True)

        painter.setFont(font)

        prozent_rechteck = QRectF(
            rechteck.left(),
            rechteck.top() + 45,
            rechteck.width(),
            55
        )

        painter.drawText(
            prozent_rechteck,
            Qt.AlignmentFlag.AlignCenter,
            f"{self._wert:.1f} %"
        )

        # Text unter Prozentwert
        painter.setPen(
            QColor("#94A3B8")
        )

        font.setPointSize(10)
        font.setBold(False)

        painter.setFont(font)

        text_rechteck = QRectF(
            rechteck.left(),
            rechteck.top() + 95,
            rechteck.width(),
            35
        )

        painter.drawText(
            text_rechteck,
            Qt.AlignmentFlag.AlignCenter,
            "Fortschritt"
        )


# ==========================================================
# Soll-Ist-Diagramm
# ==========================================================

class FortschrittChart(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self._daten = []

        self.setMinimumHeight(220)

    def set_daten(self, daten) -> None:
        self._daten = daten
        self.update()

    def paintEvent(self, event) -> None:

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )

        if not self._daten:
            painter.setPen(
                QColor("#64748B")
            )

            painter.drawText(
                self.rect(),
                Qt.AlignmentFlag.AlignCenter,
                "Keine Verlaufsdaten vorhanden"
            )

            return

        links = 50
        rechts = 20
        oben = 25
        unten = 40

        breite = (
            self.width()
            - links
            - rechts
        )

        hoehe = (
            self.height()
            - oben
            - unten
        )

        # --------------------------------------------------
        # Gitternetz / Y-Achse
        # --------------------------------------------------

        grid_pen = QPen(
            QColor("#263445"),
            1
        )

        painter.setPen(
            grid_pen
        )

        schrift = QFont(
            "Segoe UI",
            8
        )

        painter.setFont(
            schrift
        )

        for prozent in [
            0,
            25,
            50,
            75,
            100
        ]:
            y = (
                oben
                + hoehe
                - hoehe
                * prozent
                / 100
            )

            painter.drawLine(
                QPointF(
                    links,
                    y
                ),
                QPointF(
                    links + breite,
                    y
                )
            )

            painter.setPen(
                QColor("#64748B")
            )

            painter.drawText(
                QRectF(
                    0,
                    y - 10,
                    links - 8,
                    20
                ),
                Qt.AlignmentFlag.AlignRight
                | Qt.AlignmentFlag.AlignVCenter,
                f"{prozent} %"
            )

            painter.setPen(
                grid_pen
            )

        # --------------------------------------------------
        # Datumsbereich
        # --------------------------------------------------

        erstes_datum = (
            self._daten[0].datum
        )

        letztes_datum = (
            self._daten[-1].datum
        )

        gesamt_tage = (
            letztes_datum
            - erstes_datum
        ).days

        if gesamt_tage <= 0:
            return

        def x_position(datum):
            tage = (
                datum
                - erstes_datum
            ).days

            return (
                links
                + breite
                * tage
                / gesamt_tage
            )

        def y_position(prozent):
            return (
                oben
                + hoehe
                - hoehe
                * prozent
                / 100
            )

        # --------------------------------------------------
        # Soll-Linie
        # --------------------------------------------------

        soll_pfad = QPainterPath()

        erstes_element = True

        for punkt in self._daten:

            x = x_position(
                punkt.datum
            )

            y = y_position(
                punkt.soll_fortschritt
            )

            if erstes_element:
                soll_pfad.moveTo(
                    x,
                    y
                )

                erstes_element = False

            else:
                soll_pfad.lineTo(
                    x,
                    y
                )

        soll_pen = QPen(
            QColor("#64748B"),
            2
        )

        soll_pen.setStyle(
            Qt.PenStyle.DashLine
        )

        painter.setPen(
            soll_pen
        )

        painter.drawPath(
            soll_pfad
        )

        # --------------------------------------------------
        # Ist-Linie
        # --------------------------------------------------

        ist_pfad = QPainterPath()

        erstes_element = True

        letzter_ist_punkt = None

        for punkt in self._daten:

            if (
                punkt.ist_fortschritt
                is None
            ):
                continue

            x = x_position(
                punkt.datum
            )

            y = y_position(
                punkt.ist_fortschritt
            )

            if erstes_element:
                ist_pfad.moveTo(
                    x,
                    y
                )

                erstes_element = False

            else:
                ist_pfad.lineTo(
                    x,
                    y
                )

            letzter_ist_punkt = (
                x,
                y
            )

        ist_pen = QPen(
            QColor("#3B82F6"),
            3
        )

        ist_pen.setCapStyle(
            Qt.PenCapStyle.RoundCap
        )

        painter.setPen(
            ist_pen
        )

        painter.drawPath(
            ist_pfad
        )

        # Aktuellen Ist-Punkt markieren
        if letzter_ist_punkt:

            painter.setBrush(
                QColor("#3B82F6")
            )

            painter.setPen(
                QColor("#60A5FA")
            )

            painter.drawEllipse(
                QPointF(
                    letzter_ist_punkt[0],
                    letzter_ist_punkt[1]
                ),
                5,
                5
            )

        # --------------------------------------------------
        # X-Achsenbeschriftungen
        # --------------------------------------------------

        painter.setPen(
            QColor("#64748B")
        )

        label_indices = {
            0,
            len(self._daten) // 4,
            len(self._daten) // 2,
            3 * len(self._daten) // 4,
            len(self._daten) - 1
        }

        for index in sorted(
            label_indices
        ):

            punkt = self._daten[
                index
            ]

            x = x_position(
                punkt.datum
            )

            text = (
                f"{punkt.datum.month:02d}/"
                f"{str(punkt.datum.year)[2:]}"
            )

            painter.drawText(
                QRectF(
                    x - 30,
                    oben + hoehe + 8,
                    60,
                    20
                ),
                Qt.AlignmentFlag.AlignCenter,
                text
            )

        # --------------------------------------------------
        # Legende
        # --------------------------------------------------

        painter.setPen(
            QPen(
                QColor("#3B82F6"),
                3
            )
        )

        painter.drawLine(
            65,
            12,
            90,
            12
        )

        painter.setPen(
            QColor("#CBD5E1")
        )

        painter.drawText(
            96,
            16,
            "Ist"
        )

        soll_legende = QPen(
            QColor("#64748B"),
            2
        )

        soll_legende.setStyle(
            Qt.PenStyle.DashLine
        )

        painter.setPen(
            soll_legende
        )

        painter.drawLine(
            135,
            12,
            160,
            12
        )

        painter.setPen(
            QColor("#CBD5E1")
        )

        painter.drawText(
            166,
            16,
            "Soll"
        )


# ==========================================================
# Dashboard
# ==========================================================

class DashboardView(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "StudyPilot"
        )

        self.resize(
            1350,
            850
        )

        self._erstelle_oberflaeche()
        self._setze_styles()

    def _erstelle_oberflaeche(
        self
    ) -> None:

        zentral_widget = QWidget()

        root_layout = QHBoxLayout(
            zentral_widget
        )

        root_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        root_layout.setSpacing(
            0
        )

        root_layout.addWidget(
            self._erstelle_sidebar()
        )

        root_layout.addWidget(
            self._erstelle_hauptbereich(),
            1
        )

        self.setCentralWidget(
            zentral_widget
        )

    # ======================================================
    # Sidebar
    # ======================================================

    def _erstelle_sidebar(
        self
    ) -> QFrame:

        sidebar = QFrame()

        sidebar.setObjectName(
            "sidebar"
        )

        sidebar.setFixedWidth(
            210
        )

        layout = QVBoxLayout(
            sidebar
        )

        layout.setContentsMargins(
            14,
            18,
            14,
            18
        )

        layout.setSpacing(
            8
        )

        logo_layout = QHBoxLayout()

        logo_icon = QLabel(
            "🎓"
        )

        logo_icon.setObjectName(
            "logo_icon"
        )

        logo_text = QLabel(
            "StudyPilot"
        )

        logo_text.setObjectName(
            "logo_text"
        )

        logo_layout.addWidget(
            logo_icon
        )

        logo_layout.addWidget(
            logo_text
        )

        logo_layout.addStretch()

        layout.addLayout(
            logo_layout
        )

        layout.addSpacing(
            22
        )

        navigation = [
            ("🏠", "Dashboard", True),
            ("📖", "Module", False),
            ("📋", "Prüfungsleistungen", False),
            ("📅", "Semester", False),
            ("🎯", "Ziele", False),
            ("📊", "Statistiken", False),
        ]

        for icon, text, aktiv in navigation:

            layout.addWidget(
                self._erstelle_nav_element(
                    icon,
                    text,
                    aktiv
                )
            )

        layout.addSpacing(
            14
        )

        trennlinie = QFrame()

        trennlinie.setObjectName(
            "trennlinie"
        )

        trennlinie.setFixedHeight(
            1
        )

        layout.addWidget(
            trennlinie
        )

        layout.addSpacing(
            14
        )

        layout.addWidget(
            self._erstelle_nav_element(
                "⚙️",
                "Einstellungen"
            )
        )

        layout.addStretch()

        layout.addWidget(
            self._erstelle_nav_element(
                "ℹ️",
                "Über StudyPilot"
            )
        )

        return sidebar

    def _erstelle_nav_element(
        self,
        icon: str,
        text: str,
        aktiv: bool = False
    ) -> QFrame:

        element = QFrame()

        element.setObjectName(
            "nav_aktiv"
            if aktiv
            else "nav_element"
        )

        layout = QHBoxLayout(
            element
        )

        layout.setContentsMargins(
            12,
            10,
            12,
            10
        )

        layout.setSpacing(
            10
        )

        icon_label = QLabel(
            icon
        )

        icon_label.setFixedWidth(
            24
        )

        icon_label.setObjectName(
            "nav_icon"
        )

        text_label = QLabel(
            text
        )

        text_label.setObjectName(
            "nav_text"
        )

        layout.addWidget(
            icon_label
        )

        layout.addWidget(
            text_label
        )

        layout.addStretch()

        return element

    # ======================================================
    # Hauptbereich
    # ======================================================

    def _erstelle_hauptbereich(
        self
    ) -> QWidget:

        container = QWidget()

        container.setObjectName(
            "hauptbereich"
        )

        layout = QVBoxLayout(
            container
        )

        layout.setContentsMargins(
            28,
            22,
            28,
            24
        )

        layout.setSpacing(
            14
        )

        # --------------------------------------------------
        # Header
        # --------------------------------------------------

        topbar = QHBoxLayout()

        titel_layout = QVBoxLayout()
        titel_layout.setSpacing(2)

        titel = QLabel(
            "Dashboard"
        )

        titel.setObjectName(
            "haupttitel"
        )

        untertitel = QLabel(
            "Übersicht Ihres Studienverlaufs "
            "und Ihrer Leistungen."
        )

        untertitel.setObjectName(
            "untertitel"
        )

        titel_layout.addWidget(
            titel
        )

        titel_layout.addWidget(
            untertitel
        )

        topbar.addLayout(
            titel_layout
        )

        topbar.addStretch()

        auswahl = QLabel(
            "🎓  Studiengang auswählen    ▾"
        )

        auswahl.setObjectName(
            "studiengang_auswahl"
        )

        topbar.addWidget(
            auswahl
        )

        layout.addLayout(
            topbar
        )

        # --------------------------------------------------
        # Studieninformationen
        # --------------------------------------------------

        info_karte = QFrame()

        info_karte.setObjectName(
            "karte"
        )

        info_layout = QHBoxLayout(
            info_karte
        )

        info_layout.setContentsMargins(
            18,
            12,
            18,
            12
        )

        info_layout.setSpacing(
            18
        )

        infos = [
            (
                "🎓",
                "Studiengang",
                "Softwareentwicklung"
            ),
            (
                "📅",
                "Studienbeginn",
                "--"
            ),
            (
                "🚩",
                "Geplantes Abschlussdatum",
                "--"
            ),
            (
                "📚",
                "Gesamtumfang",
                "180 ECTS"
            )
        ]

        for index, info in enumerate(
            infos
        ):
            info_layout.addWidget(
                self._erstelle_info_element(
                    *info
                )
            )

            info_layout.setStretch(
                index,
                1
            )

        layout.addWidget(
            info_karte
        )

        # --------------------------------------------------
        # KPI-Karten
        # --------------------------------------------------

        kpi_layout = QGridLayout()

        kpi_layout.setSpacing(
            14
        )

        self.ects_wert = QLabel("-")
        self.noten_wert = QLabel("-")
        self.bestandene_module_wert = QLabel("-")
        self.laufende_module_wert = QLabel("-")

        self.ects_detail = QLabel("-")
        self.noten_detail = QLabel(
            "Aktueller Durchschnitt"
        )
        self.bestanden_detail = QLabel("-")
        self.laufend_detail = QLabel(
            "aktuell in Bearbeitung"
        )

        kpis = [
            (
                "🎓",
                "ECTS-Fortschritt",
                self.ects_wert,
                self.ects_detail
            ),
            (
                "📈",
                "Notendurchschnitt",
                self.noten_wert,
                self.noten_detail
            ),
            (
                "✅",
                "Bestandene Module",
                self.bestandene_module_wert,
                self.bestanden_detail
            ),
            (
                "🕒",
                "Laufende Module",
                self.laufende_module_wert,
                self.laufend_detail
            )
        ]

        for index, kpi in enumerate(
            kpis
        ):

            kpi_layout.addWidget(
                self._erstelle_kpi_karte(
                    *kpi
                ),
                0,
                index
            )

        layout.addLayout(
            kpi_layout
        )

        # --------------------------------------------------
        # Fortschritt + Diagramm
        # --------------------------------------------------

        dashboard_layout = QGridLayout()

        dashboard_layout.setSpacing(
            14
        )

        # ECTS
        fortschritt_karte = QFrame()

        fortschritt_karte.setObjectName(
            "karte"
        )

        fortschritt_layout = QVBoxLayout(
            fortschritt_karte
        )

        fortschritt_layout.setContentsMargins(
            18,
            16,
            18,
            16
        )

        titel = QLabel(
            "ECTS-Fortschritt"
        )

        titel.setObjectName(
            "karten_titel"
        )

        fortschritt_layout.addWidget(
            titel
        )

        fortschritt_inhalt = QHBoxLayout()

        self.circular_progress = (
            CircularProgress()
        )

        fortschritt_inhalt.addWidget(
            self.circular_progress
        )

        werte_layout = QVBoxLayout()

        self.erreicht_wert = QLabel("-")
        self.verbleibend_wert = QLabel("-")
        self.gesamt_wert = QLabel("-")

        werte = [
            (
                "Erreichte ECTS",
                self.erreicht_wert
            ),
            (
                "Verbleibende ECTS",
                self.verbleibend_wert
            ),
            (
                "Gesamt",
                self.gesamt_wert
            )
        ]

        werte_layout.addStretch()

        for beschriftung, wert in werte:

            label = QLabel(
                beschriftung
            )

            label.setObjectName(
                "detail_text"
            )

            wert.setObjectName(
                "fortschritt_info_wert"
            )

            werte_layout.addWidget(
                label
            )

            werte_layout.addWidget(
                wert
            )

            werte_layout.addSpacing(
                7
            )

        werte_layout.addStretch()

        fortschritt_inhalt.addLayout(
            werte_layout
        )

        fortschritt_layout.addLayout(
            fortschritt_inhalt
        )

        dashboard_layout.addWidget(
            fortschritt_karte,
            0,
            0
        )

        # Soll-Ist
        chart_karte = QFrame()

        chart_karte.setObjectName(
            "karte"
        )

        chart_layout = QVBoxLayout(
            chart_karte
        )

        chart_layout.setContentsMargins(
            18,
            16,
            18,
            12
        )

        chart_titel = QLabel(
            "Soll-Ist-Vergleich "
            "(zeitlicher Verlauf)"
        )

        chart_titel.setObjectName(
            "karten_titel"
        )

        self.fortschritt_chart = (
            FortschrittChart()
        )

        chart_layout.addWidget(
            chart_titel
        )

        chart_layout.addWidget(
            self.fortschritt_chart,
            1
        )

        dashboard_layout.addWidget(
            chart_karte,
            0,
            1
        )

        dashboard_layout.setColumnStretch(
            0,
            1
        )

        dashboard_layout.setColumnStretch(
            1,
            2
        )

        layout.addLayout(
            dashboard_layout
        )

        # --------------------------------------------------
        # Modulübersicht
        # --------------------------------------------------

        modul_karte = QFrame()

        modul_karte.setObjectName(
            "karte"
        )

        modul_layout = QVBoxLayout(
            modul_karte
        )

        modul_layout.setContentsMargins(
            18,
            14,
            18,
            14
        )

        modul_titel = QLabel(
            "Modulübersicht"
        )

        modul_titel.setObjectName(
            "karten_titel"
        )

        modul_layout.addWidget(
            modul_titel
        )

        self.modul_tabelle = (
            QTableWidget()
        )

        self.modul_tabelle.setColumnCount(
            7
        )

        self.modul_tabelle.setHorizontalHeaderLabels(
            [
                "Modulnummer",
                "Modul",
                "Semester",
                "ECTS",
                "Status",
                "Prüfungen",
                "Note"
            ]
        )

        self.modul_tabelle.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )

        self.modul_tabelle.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )

        self.modul_tabelle.verticalHeader().setVisible(
            False
        )

        header = (
            self.modul_tabelle.horizontalHeader()
        )

        header.setSectionResizeMode(
            0,
            QHeaderView.ResizeMode.ResizeToContents
        )

        header.setSectionResizeMode(
            1,
            QHeaderView.ResizeMode.Stretch
        )

        for spalte in range(
            2,
            7
        ):
            header.setSectionResizeMode(
                spalte,
                QHeaderView.ResizeMode.ResizeToContents
            )

        modul_layout.addWidget(
            self.modul_tabelle
        )

        layout.addWidget(
            modul_karte,
            1
        )

        return container

    # ======================================================
    # UI-Helfer
    # ======================================================

    def _erstelle_info_element(
        self,
        icon,
        titel_text,
        wert_text
    ):

        widget = QWidget()

        widget.setObjectName(
            "transparent"
        )

        layout = QHBoxLayout(
            widget
        )

        layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        layout.setSpacing(
            8
        )

        icon_label = QLabel(
            icon
        )

        icon_label.setFixedWidth(
            28
        )

        text_layout = QVBoxLayout()

        text_layout.setSpacing(
            2
        )

        titel = QLabel(
            titel_text
        )

        titel.setObjectName(
            "info_titel"
        )

        wert = QLabel(
            wert_text
        )

        wert.setObjectName(
            "info_wert"
        )

        text_layout.addWidget(
            titel
        )

        text_layout.addWidget(
            wert
        )

        layout.addWidget(
            icon_label
        )

        layout.addLayout(
            text_layout
        )

        layout.addStretch()

        return widget

    def _erstelle_kpi_karte(
        self,
        icon,
        titel_text,
        wert_label,
        detail_label
    ):

        karte = QFrame()

        karte.setObjectName(
            "karte"
        )

        layout = QVBoxLayout(
            karte
        )

        layout.setContentsMargins(
            16,
            13,
            16,
            13
        )

        kopf = QHBoxLayout()

        kopf.setSpacing(
            7
        )

        icon_label = QLabel(
            icon
        )

        icon_label.setFixedWidth(
            28
        )

        titel = QLabel(
            titel_text
        )

        titel.setObjectName(
            "karten_titel"
        )

        kopf.addWidget(
            icon_label
        )

        kopf.addWidget(
            titel
        )

        kopf.addStretch()

        wert_label.setObjectName(
            "kpi_wert"
        )

        detail_label.setObjectName(
            "detail_text"
        )

        layout.addLayout(
            kopf
        )

        layout.addWidget(
            wert_label
        )

        layout.addWidget(
            detail_label
        )

        return karte

    # ======================================================
    # DTO anzeigen
    # ======================================================

    def zeige_dashboard(
        self,
        daten: DashboardDatenDTO
    ) -> None:

        self.ects_wert.setText(
            f"{daten.fortschritt_prozent:.1f} %"
        )

        self.ects_detail.setText(
            f"{daten.erreichte_ects} / "
            f"{daten.gesamt_ects} ECTS erreicht"
        )

        if daten.notendurchschnitt is None:
            self.noten_wert.setText("-")
        else:
            self.noten_wert.setText(
                f"{daten.notendurchschnitt:.2f}"
            )

        self.bestandene_module_wert.setText(
            str(
                daten.bestandene_module
            )
        )

        self.laufende_module_wert.setText(
            str(
                daten.laufende_module
            )
        )

        self.bestanden_detail.setText(
            f"{daten.bestandene_module} "
            "erfolgreich abgeschlossen"
        )

        self.circular_progress.set_wert(
            daten.fortschritt_prozent
        )

        self.erreicht_wert.setText(
            str(
                daten.erreichte_ects
            )
        )

        self.verbleibend_wert.setText(
            str(
                daten.verbleibende_ects
            )
        )

        self.gesamt_wert.setText(
            str(
                daten.gesamt_ects
            )
        )

        # Diagramm
        self.fortschritt_chart.set_daten(
            daten.fortschritt_verlauf
        )

        # Modultabelle
        self.modul_tabelle.setRowCount(
            len(daten.module)
        )

        for zeile, modul in enumerate(
            daten.module
        ):

            note = (
                "-"
                if modul.note is None
                else f"{modul.note:.2f}"
            )

            werte = [
                modul.modulnummer,
                modul.bezeichnung,
                str(modul.semester),
                str(modul.ects),
                modul.status,
                str(
                    modul.pruefungsleistungen
                ),
                note
            ]

            for spalte, wert in enumerate(
                werte
            ):

                item = QTableWidgetItem(
                    wert
                )

                if spalte in [
                    2,
                    3,
                    5,
                    6
                ]:
                    item.setTextAlignment(
                        Qt.AlignmentFlag.AlignCenter
                    )

                self.modul_tabelle.setItem(
                    zeile,
                    spalte,
                    item
                )

        self.modul_tabelle.resizeRowsToContents()

    # ======================================================
    # Styling
    # ======================================================

    def _setze_styles(
        self
    ) -> None:

        self.setStyleSheet("""
            QMainWindow {
                background-color: #0B111A;
            }

            QWidget {
                background-color: #0B111A;
                color: #E5E7EB;
                font-family: "Segoe UI";
            }

            QWidget#transparent {
                background: transparent;
            }

            QFrame#sidebar {
                background-color: #101721;
                border-right: 1px solid #1F2937;
            }

            QLabel#logo_text {
                font-size: 20px;
                font-weight: 700;
                color: #F9FAFB;
                background: transparent;
            }

            QLabel#logo_icon {
                font-size: 22px;
                background: transparent;
            }

            QFrame#nav_element {
                background: transparent;
                border-radius: 7px;
            }

            QFrame#nav_aktiv {
                background-color: #1E3A66;
                border-radius: 7px;
            }

            QLabel#nav_icon,
            QLabel#nav_text {
                background: transparent;
                font-size: 14px;
            }

            QFrame#nav_aktiv QLabel#nav_text {
                font-weight: 600;
                color: white;
            }

            QFrame#trennlinie {
                background-color: #243041;
            }

            QWidget#hauptbereich {
                background-color: #0B111A;
            }

            QLabel#haupttitel {
                font-size: 26px;
                font-weight: 700;
                color: #F9FAFB;
            }

            QLabel#untertitel {
                font-size: 13px;
                color: #9CA3AF;
            }

            QLabel#studiengang_auswahl {
                background-color: #121B27;
                border: 1px solid #263445;
                border-radius: 7px;
                padding: 10px 14px;
            }

            QFrame#karte {
                background-color: #121B27;
                border: 1px solid #263445;
                border-radius: 9px;
            }

            QLabel#karten_titel {
                font-size: 13px;
                font-weight: 600;
                color: #D1D5DB;
                background: transparent;
            }

            QLabel#info_titel {
                font-size: 11px;
                color: #94A3B8;
                background: transparent;
            }

            QLabel#info_wert {
                font-size: 13px;
                font-weight: 600;
                background: transparent;
            }

            QLabel#kpi_wert {
                font-size: 25px;
                font-weight: 700;
                color: #F8FAFC;
                background: transparent;
            }

            QLabel#detail_text {
                font-size: 12px;
                color: #94A3B8;
                background: transparent;
            }

            QLabel#fortschritt_info_wert {
                font-size: 18px;
                font-weight: 700;
                background: transparent;
            }

            QTableWidget {
                background-color: #121B27;
                alternate-background-color: #101923;
                border: none;
                gridline-color: #263445;
                color: #D1D5DB;
                font-size: 12px;
                selection-background-color: #1E3A66;
            }

            QTableWidget::item {
                padding: 7px;
            }

            QHeaderView::section {
                background-color: #192432;
                color: #94A3B8;
                border: none;
                border-bottom: 1px solid #334155;
                padding: 7px;
                font-weight: 600;
            }
        """)