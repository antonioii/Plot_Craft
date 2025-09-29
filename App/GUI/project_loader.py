''' # PROJECT LOADER MODULE

=================
IMPLEMENTATION (EN)
=================
Starting from the creation functions for new projects, pairs of load_* functions were created in each GUI module,
capable of reconstructing the screen using exclusively the data persisted in JSON (without triggering the LLM).
When the user selects a saved project, load_project identifies the project_phase and delegates to the corresponding
load_* function: title/summary, reference board, acts, chapters, beats, or final draft. This approach keeps the
original creation flow intact and provides a safe parallel path to reopen existing projects, reusing the already
implemented UI components.

=================
IMPLEMENTAÇÃO (PT-BR)
=================
A partir das funções de criação para novos projetos, foram criados pares de funções load_* em cada módulo GUI,
capazes de remontar a tela usando exclusivamente os dados persistidos no JSON (sem acionar o LLM). Quando o
usuário seleciona um projeto salvo, load_project identifica o project_phase e delega à função load_*
correspondente: título/resumo, quadro de referências, atos, capítulos, beats ou redação final. Essa abordagem
mantém o fluxo original de criação intacto e oferece um caminho paralelo seguro para reabrir projetos existentes,
reaproveitando os componentes de UI já implementados.
================================================================================================================'''

import json
from tkinter import filedialog, messagebox
from GUI.windows_header import create_default_header
from GUI.title_and_resume_window import load_title_and_resume_area
from GUI.schema_ref_board import load_ref_schema_board
from GUI.sugest_acts_window import load_acts_window
from GUI.sugest_chapters_window import load_chapters_window
from GUI.sugests_beats_window import load_beats_window
from GUI.finishing_writing_window import load_final_writing

# --- Function to load JSON saved files from old projects ---
def load_project(self):
    file_path = filedialog.askopenfilename(
        title="Open Project File",
        defaultextension=".json",
        filetypes=[("JSON files", "*.json")],
    )
    if not file_path:
        return

    try:
        with open(file_path, "r", encoding="utf-8") as file_obj:
            json_saved_file = json.load(file_obj)
    except (OSError, json.JSONDecodeError) as exc:
        messagebox.showerror("Error", f"Could not load the selected project:\n{exc}")
        return

    project_phase = str(json_saved_file.get("project_phase", "0"))

    if hasattr(self, "initial_content_area"):
        try:
            self.initial_content_area.destroy()
        except Exception:
            pass
    if hasattr(self, "footer_notes"):
        try:
            self.footer_notes.destroy()
        except Exception:
            pass

    create_default_header(self)

    loaders = {
        "0": load_title_and_resume_area,
        "1": load_ref_schema_board,
        "2": load_acts_window,
        "3": load_chapters_window,
        "4": load_beats_window,
        "5": load_final_writing,
    }

    loader = loaders.get(project_phase)
    if loader is None:
        messagebox.showwarning(
            "Warning",
            f"Unknown project phase '{project_phase}'. Opening the chapters editor instead.",
        )
        loader = load_chapters_window

    loader(self, json_saved_file, file_path)
    self.loaded_project_path = file_path

# --- Function to stub tests ---
def placeholder_for_upload(self):
    messagebox.showerror("Failed!", "Sorry, this feature is not working.")
    return