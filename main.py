from datetime import date

from domain.studiengang import Studiengang
from domain.semester import Semester


studienstart = date(2023, 7, 17)

semester_1 = Semester(
    nummer=1,
    bezeichnung="1. Semester",
    studienstart=studienstart
)

semester_2 = Semester(
    nummer=2,
    bezeichnung="2. Semester",
    studienstart=studienstart
)

studiengang = Studiengang(
    bezeichnung="Softwareentwicklung",
    gesamt_ects=180,
    startdatum=studienstart,
    regulaeres_enddatum=date(2026, 7, 17),
    ziel_enddatum=date(2027, 7, 17),
    zielnote=2.0,
    semester=[semester_1, semester_2]
)

print(studiengang)
print()

for semester in studiengang.semester:
    print(
        semester.bezeichnung,
        semester.startdatum,
        semester.enddatum
    )