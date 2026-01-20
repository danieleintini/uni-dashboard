---
current_semester: 3
exams:
  # --- SEMESTER 1 (Completed) ---
  - module: "Mathematics 1"
    ects: 5
    grade: 2.3
    status: passed
    date: 2024-02-15
    semester: 1

  - module: "Structural Mechanics 1"
    ects: 5
    grade: 1.7
    status: passed
    date: 2024-03-10
    semester: 1

  # --- SEMESTER 2 (Partially missed) ---
  - module: "Mechanics 2"
    ects: 5
    grade: null
    status: open  
    date: null
    semester: 2

  # --- SEMESTER 3 (Current) ---
  - module: "Building Physics"
    ects: 5
    grade: null
    status: planned  
    date: 2026-02-20
    semester: 3

  - module: "Hydromechanics"
    ects: 5
    grade: null
    status: open   
    date: null
    semester: 3

  # --- SEMESTER 4 (Future) ---
  - module: "Steel Construction"
    ects: 5
    grade: null
    status: open   
    date: null
    semester: 4
---

# University Dashboard Database
This file is the single source of truth for the Python Dashboard.
Edit the YAML block above to update your progress.

**Status Legend:**
- `passed`: Module completed (requires 'grade')
- `planned`: Registered for exam (requires 'date', will show as Green)
- `open`: Not yet passed or registered (will be categorized automatically based on semester)
