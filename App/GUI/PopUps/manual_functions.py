import sys, os, subprocess, webbrowser
from pathlib import Path
from tkinter import messagebox

def open_instructions_html():
    base = Path(__file__).resolve().parent.parent.parent
    html_path = base / "Assets" / "index.html"

    if not html_path.exists():
        messagebox.showerror("File not found", f"Not found!:\n{html_path}")
        return

    try:
        if sys.platform.startswith("win"):  # Windows
            os.startfile(str(html_path))    
            return
        elif sys.platform == "darwin":      # macOS
            subprocess.run(["open", str(html_path)], check=False)
            return
        else:                               # Linux, etc
            subprocess.run(["xdg-open", str(html_path)], check=False)
            return
    except Exception:
        
        # Fallback to some systems: try to open directly through webbrowser (URI files)
        try:
            webbrowser.open(html_path.as_uri(), new=2)
        except Exception as e:
            messagebox.showerror("Error opening HTML", f"An error has occurred:\n{e}")
