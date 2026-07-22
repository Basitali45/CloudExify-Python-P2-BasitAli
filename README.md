# Student Grade Management System

**CloudExify Python Internship 2026 — Month 1, Project 2**

## Student Information

- **Name:** [Basit Ali]
- **Registration Number:** [CX-INT-2026-PY-0160]

## Project Overview

A command-line Student Grade Management System built in Python. It stores student
records (name, subject-wise grades, attendance) in memory, lets you manage them
through a menu, and persists everything to a CSV file so data survives between
runs.

## How to Run

```bash
python3 grade_system.py
```

On start it automatically loads `students.csv` if one exists in the same folder.
Choose an option from the menu (1–9), or `0` to save and exit.

## Features Implemented

### Core Features
- **Add Student** — name + grade for every subject, with duplicate-name check and
  0–100 input validation (keeps re-asking on bad input instead of crashing).
- **View All Students** — a neatly aligned table with every subject, average,
  letter grade, pass/fail status, and attendance.
- **Class Report** — total students, class average, highest/lowest average,
  pass/fail counts, and a ranked leaderboard (1st, 2nd, 3rd...).
- **Search Student** — case-insensitive name search that prints a full report
  card, including class rank.
- **Edit Grades** — pick a student by ID, then update any subject grade or their
  attendance.
- **Delete Student** — remove a record by ID, with a yes/no confirmation.
- **Save / Load CSV** — all records are saved to `students.csv` and reloaded
  automatically the next time the program starts.

### Bonus Features (all implemented)
| Bonus | Details |
|---|---|
| Grade letters (A–F) | Every average and subject mark is converted to a letter grade (90+=A, 80+=B, 70+=C, 60+=D, 50+=E, below 50=F). |
| Subject-wise class average | Class Report shows the average mark per subject across all students. |
| Individual report card | Dedicated menu option (5) — enter a Student ID or Name to instantly get their full report card (subjects, average, letter grade, status, class rank, attendance). Also reachable from Search. |
| Export report as text file | Option 8 writes a formatted summary to `class_report.txt`. |
| Attendance tracking per student | Attendance % is captured when a student is added, editable later, shown in the table/report card/class report, and flagged with **(Low!)** when below 75%. |
| Custom subjects (not a fixed list) | Option 7 lets you add or remove subjects at runtime; existing students automatically get the new subject (default 0, editable) or lose the removed one. |

## Sample Output

**View All Students:**
```
--- ALL STUDENTS ---
ID   Name                Math    Physic  Englis  Comput  Urdu    Avg     Grade  Status  Attend
----------------------------------------------------------------------------------------------
1    Ahmed Khan          85.0    78.0    92.0    88.0    75.0    83.6    B      PASS    88.0%
2    Sara Ali            90.0    95.0    88.0    92.0    80.0    89.0    B      PASS    95.0%
3    Bilal Ahmed         55.0    48.0    62.0    70.0    58.0    58.6    E      PASS    60.0%  (Low!)
4    Fatima Noor         72.0    80.0    68.0    75.0    90.0    77.0    C      PASS    82.0%
5    Hamza Tariq         40.0    35.0    45.0    50.0    38.0    41.6    F      FAIL    55.0%  (Low!)
```

**Class Report (with rankings and subject-wise average):**
```
=== CLASS REPORT ===
Total Students  : 5
Class Average   : 69.96
Highest Average : 89.00
Lowest Average  : 41.60
Passed          : 4
Failed          : 1
Avg Attendance  : 76.0%
Low Attendance  : Bilal Ahmed, Hamza Tariq (below 75%)

--- SUBJECT-WISE CLASS AVERAGE ---
  Math        : 68.40
  Physics     : 67.20
  English     : 71.00
  Computer    : 75.00
  Urdu        : 68.20

--- RANKINGS ---
  1st   Sara Ali             89.00 (B)
  2nd   Ahmed Khan           83.60 (B)
  3rd   Fatima Noor          77.00 (C)
  4th   Bilal Ahmed          58.60 (E)
  5th   Hamza Tariq          41.60 (F)
```

**Search → Individual Report Card:**
```
--- REPORT CARD: Sara Ali (ID 2) ---
  Math        : 90.0  (A)
  Physics     : 95.0  (A)
  English     : 88.0  (B)
  Computer    : 92.0  (A)
  Urdu        : 80.0  (B)
  Average     : 89.00  (B)
  Status : PASS
  Class Rank : 1 out of 5
  Attendance : 95.0%
```

## Challenges Faced & How I Solved Them

- **Keeping the subject list flexible.** The base project uses a fixed subject
  list, but I wanted the "custom subjects" bonus to actually work end-to-end —
  including CSV save/load. I solved this by writing the subject names as CSV
  header columns instead of hardcoding them, so `load_from_csv()` rebuilds the
  subject list from whatever columns are in the file.
- **Adding attendance without breaking old CSV files.** Once I added the
  Attendance column, loading an older CSV (without that column) would crash.
  I fixed this with a safe lookup (`row.get`/conditional check) that defaults
  missing attendance to `0.0` instead of raising a `KeyError`.
- **Validating user input cleanly.** Grades and attendance both need a number
  between 0–100, and typing a letter by mistake shouldn't crash the program.
  I wrote one reusable `get_valid_grade()` helper with a `try/except` +
  range check loop, and used it everywhere a percentage is needed, so the
  validation logic only exists in one place.
- **Showing a student's class rank inside the report card.** Ranking is
  normally only calculated for the whole class. I reused the same
  `ranked_students()` sorting function and located the individual student's
  position in that sorted list, so rank stays consistent everywhere it's shown.

## Brief Report

**What was the hardest part to implement?**
Attendance tracking, since it touched almost every function in the program —
add, view, edit, the class report, the report card, and both CSV read/write —
and each of those needed to stay backward-compatible with data saved before
attendance existed.

**What would I add if given more time?**
- A GPA/CGPA style weighted-grade system where subjects can have different
  credit hours.
- A simple menu option to bulk-import students from an existing CSV/Excel
  file instead of typing them one at a time.
- Basic input for multiple exams per subject (e.g. midterm + final) instead
  of a single grade per subject.
- Colored terminal output (using `colorama`) to make PASS/FAIL and low
  attendance warnings stand out visually.

## Files in This Repository

- `grade_system.py` — the full application.
- `students.csv` — sample data (5 students) so the program has something to
  load on first run.
- `README.md` — this file.
