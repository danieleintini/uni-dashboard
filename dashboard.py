import os
import frontmatter
from textual.app import App, ComposeResult
from textual.containers import Container, Grid
from textual.widgets import Header, Footer, Static, DataTable, Digits, ProgressBar

# Configuration
DATA_FILE = "db.md"
REQUIRED_ECTS = 210 

# --- Helper: Date Sorting ---
def get_sortable_date(date_str):
    """Converts '02.02.2026' into sortable '2026-02-02'"""
    s = str(date_str).strip()
    if s in ["None", "-", "", "TBD", "null"]:
        return "9999-99-99" 
    
    # Try German/European format DD.MM.YYYY
    try:
        parts = s.split(".")
        if len(parts) == 3:
            return f"{parts[2]}-{parts[1]}-{parts[0]}"
    except:
        pass
    
    return s

def get_data():
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, DATA_FILE)
    
    stats = {
        "total_ects": 0,
        "passed_count": 0,
        "grades": [],
        "upcoming": [],     
        "transcript": [],   
        "current_sem": 1,
        "current_load": 0 
    }

    # Check if database exists
    if not os.path.exists(file_path):
        return {**stats, "upcoming": [{"status_label": "Error", "sem": 0, "module": "db.md not found. Please rename example_db.md to db.md!", "ects": 0, "date": "-", "sort_prio": 1}]}

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = frontmatter.load(f)
            
        stats["current_sem"] = data.metadata.get("current_semester", 1)
        exams = data.metadata.get("exams", [])

        for exam in exams:
            status = exam.get("status", "open").lower()
            ex_sem = exam.get("semester", 99)
            ects = exam.get("ects", 0)
            
            # --- 1. Passed Modules (Transcript) ---
            if status == "passed":
                stats["total_ects"] += ects
                stats["passed_count"] += 1
                
                grade_val = 0.0
                grade_str = "-"
                
                if exam.get("grade"):
                    grade_val = float(exam["grade"])
                    grade_str = str(grade_val)
                    stats["grades"].append(grade_val)
                else:
                    grade_str = "Pass"

                stats["transcript"].append({
                    "sem": ex_sem,
                    "module": exam["module"],
                    "ects": ects,
                    "grade": grade_str,
                    "grade_val": grade_val
                })
            
            # --- 2. Open / Planned Modules ---
            elif status in ["planned", "open", "angemeldet"]:
                status_label = "Open"
                # Sort Priority: 1=Registered, 2=Retake, 3=Current, 4=Future
                sort_prio = 4 
                
                # Case A: Registered (Highest Priority)
                if status in ["planned", "angemeldet"]:
                    status_label = "Registered"
                    stats["current_load"] += ects 
                    sort_prio = 1 
                
                # Case B: Retake (Past Semester)
                elif ex_sem < stats["current_sem"]:
                    status_label = "Retake"
                    sort_prio = 2 
                    
                # Case C: Current Semester
                elif ex_sem == stats["current_sem"]:
                    status_label = "Current"
                    stats["current_load"] += ects 
                    sort_prio = 3
                    
                # Case D: Future
                else:
                    status_label = "Future"
                    sort_prio = 4

                raw_date = str(exam.get("date", "-"))
                
                stats["upcoming"].append({
                    "status_label": status_label,
                    "sem": ex_sem,
                    "module": exam["module"],
                    "ects": ects,
                    "date": raw_date,
                    "sort_prio": sort_prio,
                    "sort_date": get_sortable_date(raw_date)
                })

    except Exception as e:
        print(f"Error reading file: {e}")
        return stats

    if stats["grades"]:
        stats["avg"] = sum(stats["grades"]) / len(stats["grades"])
    else:
        stats["avg"] = 0.0
        
    # Sort Upcoming: Priority -> Date
    stats["upcoming"].sort(key=lambda x: (x["sort_prio"], x["sort_date"]))
    # Sort Transcript: Semester -> Grade
    stats["transcript"].sort(key=lambda x: (x["sem"], x["grade_val"]))
    
    return stats

class UniDashboard(App):
    CSS = """
    Screen { background: #0d1117; color: #c9d1d9; }
    
    #header-info {
        content-align: center middle;
        background: #21262d;
        color: #f0f6fc;
        padding: 1;
        text-style: bold;
        border-bottom: solid #30363d;
    }

    #stats-grid {
        layout: grid;
        grid-size: 3;
        grid-gutter: 1;
        margin: 1;
        height: 10; 
    }

    .stat-box {
        background: #161b22;
        border: wide #30363d;
        height: 100%;
        align: center middle;
    }
    
    .label { color: #8b949e; margin-top: 1; margin-bottom: 0; text-align: center; }
    
    #val-ects { color: #3fb950; }  
    #val-grade { color: #a371f7; } 
    #val-pass { color: #58a6ff; }  

    DataTable {
        background: #161b22;
        border: wide #30363d;
        margin: 1;
        height: 1fr; 
    }
    
    .section-title {
        background: #21262d;
        color: #f0f6fc;
        padding-left: 1;
        text-style: bold;
        margin: 1 1 0 1;
    }
    
    ProgressBar { margin: 1; tint: #3fb950; }
    """

    def compose(self) -> ComposeResult:
        self.data = get_data()
        
        yield Header(show_clock=True)
        
        info_text = f"Semester {self.data['current_sem']}  |  Current Load: {self.data['current_load']} ECTS"
        yield Static(info_text, id="header-info")
        
        percent = (self.data["total_ects"] / REQUIRED_ECTS) * 100
        yield Static(f" Degree Progress: {int(percent)}%  ({self.data['total_ects']} / {REQUIRED_ECTS} ECTS)", classes="label")
        yield ProgressBar(total=REQUIRED_ECTS, show_eta=False, id="degree-bar")

        with Grid(id="stats-grid"):
            with Container(classes="stat-box"):
                yield Static("ECTS Collected", classes="label")
                yield Digits(str(self.data["total_ects"]), id="val-ects")
            
            with Container(classes="stat-box"):
                yield Static("Avg Grade", classes="label")
                yield Digits(f"{self.data['avg']:.2f}", id="val-grade")

            with Container(classes="stat-box"):
                yield Static("Passed Exams", classes="label")
                yield Digits(str(self.data["passed_count"]), id="val-pass")

        # --- TABLE 1: SCHEDULE ---
        yield Static(" Exam Schedule (Sorted by Priority & Date)", classes="section-title")
        table_plan = DataTable(id="table-plan")
        table_plan.cursor_type = "row"
        table_plan.zebra_stripes = True
        table_plan.add_columns("Status", "Sem", "Module", "ECTS", "Date")
        
        for item in self.data["upcoming"]:
            # Style Status Label
            status = item["status_label"]
            if "Registered" in status: status = f"[green]{status}[/]"
            elif "Retake" in status: status = f"[red]{status}[/]"
            elif "Current" in status: status = f"[blue]{status}[/]"
            
            table_plan.add_row(
                status,
                str(item["sem"]),
                item["module"], 
                str(item["ects"]), 
                item["date"]
            )
        yield table_plan

        # --- TABLE 2: TRANSCRIPT ---
        yield Static(" Transcript / Passed Modules", classes="section-title")
        table_done = DataTable(id="table-done")
        table_done.cursor_type = "row"
        table_done.zebra_stripes = True
        table_done.add_columns("Sem", "Grade", "Module", "ECTS")
        
        for item in self.data["transcript"]:
            table_done.add_row(
                str(item["sem"]),
                item["grade"],
                item["module"],
                str(item["ects"])
            )
        yield table_done
        
        yield Footer()

    def on_mount(self) -> None:
        try:
            bar = self.query_one("#degree-bar", ProgressBar)
            bar.advance(self.data["total_ects"])
        except:
            pass

if __name__ == "__main__":
    app = UniDashboard()
    app.run()
