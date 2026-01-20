# University Dashboard (Python TUI)

A terminal-based dashboard for students to track ECTS credits, average grades, and exam schedules. Designed for seamless integration with Obsidian, it parses data directly from a local Markdown file.

## Features

- **Obsidian Integration:** Reads module data from a simple Markdown file (`db.md`).
- **Progress Tracking:** Visual degree progress bar (defaults to 210 ECTS).
- **Exam Schedule:** Automatically sorts exams by priority:
    1. Registered Exams (Green)
    2. Retake Exams / Past Semesters (Red)
    3. Current Semester Modules (Blue)
    4. Future Modules (Grey)
- **Transcript View:** Separate list for all passed modules and grades.
- **Modern UI:** Built with Python Textual for a clean terminal interface.

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/danieleintini/uni-dashboard.git
   cd uni-dashboard
   ```

2. **Install requirements**
   ```bash
   pip install textual python-frontmatter
   ```


3. **Setup Database**
* Rename `example_db.md` to `db.md`.
* Open `db.md` in any text editor or Obsidian and enter your own modules in the YAML header.



## Usage

Run the dashboard from your terminal:

```bash
python dashboard.py
```

## Configuration

**Adjusting total ECTS:**
The dashboard defaults to 210 ECTS (common for 7-semester Bachelor programs). To change this, edit the configuration variable in `dashboard.py`:

```python
REQUIRED_ECTS = 180  # Change to your requirement
```

**Status Logic:**

* `status: passed` -> Adds to ECTS total and Transcript.
* `status: planned` -> Marks as "Registered" (High Priority).
* `status: open` -> Categorized as Retake, Current, or Future based on `current_semester`.

## Tech Stack

* **Python 3.13+**
* **Textual** (TUI Framework)
* **Frontmatter** (YAML Parsing)
