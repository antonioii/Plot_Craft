import tkinter, json
from tkinter import ttk
from GUI.PopUps.add_chapters_window import add_new_chapter
from GUI.sugests_beats_window import create_beats_window
from API.Internal_APIs.handler_apis import ask_LLM_for_chapters
from tkinter import messagebox

def create_chapters_window(self, json_saved_file, json_file_path, regenerate=False):
    # --- Generate chapters if they do not exist, if regenerate=True ---
    chapters_list = json_saved_file.get("Chapters", [])
    if regenerate or not chapters_list:
        # Read the saved JSON file
        book_title     = json_saved_file.get("book_title", "")
        book_resume    = json_saved_file.get("book_resume", "")
        places_objects = json_saved_file.get("Places_Objects", "")
        characters     = json_saved_file.get("Characters", "")
        happenings     = json_saved_file.get("Happenings", "")
        act1           = json_saved_file.get("Act1", "")
        act2           = json_saved_file.get("Act2", "")
        act3           = json_saved_file.get("Act3", "")

        try:
            chapters_payload = ask_LLM_for_chapters(
                book_title, book_resume, places_objects, characters, happenings, act1, act2, act3
            ) or {}
        except Exception as e:
            chapters_payload = {"Chapters": [[f"Erro ao gerar capítulos: {e}", "Resumo indisponível.", []]]}

        chapters_list = chapters_payload.get("Chapters", [])
        if not isinstance(chapters_list, list):
            chapters_list = []

        json_saved_file["Chapters"] = chapters_list
        json_saved_file["project_phase"] = "3"
        if json_file_path:
            with open(json_file_path, 'w', encoding='utf-8') as f:
                json.dump(json_saved_file, f, indent=4, ensure_ascii=False)

    # --- Prepare the window UI (Wipe content area) ---
    if hasattr(self, "acts_main_frame") and self.acts_main_frame:
        try:
            self.acts_main_frame.destroy()
        except:
            pass


    # --- Settings for text areas, labels and buttons ---
    _text_box_width = 107
    _text_box_height = 22
    _text_box_fonts = "Arial 10"
    _text_box_pady = 5
    _label_pady = (5, 0)
    _btn_pady = (5, 0)
    _btn_padx = 5
    _btn_color = "black"
    _btn_fg = "white"
    _btn_font = "Arial 8 bold"

    # --- Helper Function: get list of chapter titles ---
    self.chapter_list_var = None
    def get_chapters_list():
        self.chapter_list_var = [f"CHAPTER {i+1} - {ch[0]}" for i, ch in enumerate(json_saved_file.get("Chapters", []))]
        return self.chapter_list_var

    # --- Helper Function: update resume text when chapter changes ---
    def on_chapter_select(event=None):
        if not getattr(self, "starting_window", False): # if starting_window is not True:
            prev_index = getattr(self, "current_chapter_index", 0)
            if 0 <= prev_index < len(json_saved_file.get("Chapters", [])):
                current_text = self.chapter_resume_text.get("1.0", tkinter.END).strip()
                json_saved_file["Chapters"][prev_index][1] = current_text

        index = self.chapters_list_box.current()
        self.current_chapter_index = index
        self.starting_window = False

        if 0 <= index < len(json_saved_file.get("Chapters", [])):
            resume_text = json_saved_file["Chapters"][index][1]
            self.chapter_resume_text.delete("1.0", tkinter.END)
            self.chapter_resume_text.insert(tkinter.END, resume_text)

    # --- Action Function: Delete chapter ---
    def delete_selected_chapter():
        index = self.chapters_list_box.current()
        if 0 <= index < len(json_saved_file.get("Chapters", [])):
            # Checking if user really wants to delete
            chapter_title = json_saved_file["Chapters"][index][0]
            confirm = messagebox.askyesno(
                "Confirm exclusion",
                f"Are you trying to delete the chapter: '\n\n{chapter_title}'?"
            )
            if not confirm:
                return
            
            # Get the text before delete
            current_text = self.chapter_resume_text.get("1.0", tkinter.END).strip()
            json_saved_file["Chapters"][index][1] = current_text

            # Delete chapter
            del json_saved_file["Chapters"][index]

            # Update JSON in disk
            if json_file_path:
                try:
                    with open(json_file_path, 'w', encoding='utf-8') as f:
                        json.dump(json_saved_file, f, indent=4, ensure_ascii=False)
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao salvar JSON: {e}")
                    return

            # Re-create combobox
            self.chapters_list_box['values'] = get_chapters_list()
            if json_saved_file["Chapters"]:
                new_index = min(index, len(json_saved_file["Chapters"]) - 1)
                self.chapters_list_box.current(new_index)
                self.current_chapter_index = new_index
                self.starting_window = False
                resume_text = json_saved_file["Chapters"][new_index][1]
                self.chapter_resume_text.delete("1.0", tkinter.END)
                self.chapter_resume_text.insert("1.0", resume_text)
            else:
                self.chapters_list_box.set("")
                self.chapter_resume_text.delete("1.0", tkinter.END)


    # --- Create the new window with sugested chapters main area---
    self.sugested_chapts_main_frame = tkinter.Frame(self.content_area)
    self.sugested_chapts_main_frame.pack()

    # --- Chapters List Area ---
    self.chapters_list_frame = tkinter.Frame(self.sugested_chapts_main_frame)
    self.chapters_list_frame.pack()

    self.chapters_list_label = tkinter.Label(self.chapters_list_frame, text="CHAPTERS:")
    self.chapters_list_label.pack(pady=_label_pady)

    self.chapters_list_box = ttk.Combobox(self.chapters_list_frame, values=get_chapters_list(), width=50, state="readonly")
    self.chapters_list_box.pack(padx=5, pady=_text_box_pady)
    self.chapters_list_box.bind("<<ComboboxSelected>>", on_chapter_select)
    ## Selects the first chapter to start, sets the chapter index, and signals that the window is in a maiden state
    self.chapters_list_box.current(0)
    self.current_chapter_index = 0
    self.starting_window = True

    # Chapters Resume Area
    self.chapter_resume_label = tkinter.Label(self.sugested_chapts_main_frame, text="CHAPTER RESUME:")
    self.chapter_resume_label.pack(pady=_label_pady)

    self.chapter_resume_text = tkinter.Text(self.sugested_chapts_main_frame, height=_text_box_height, width=_text_box_width,
                                            font=_text_box_fonts, undo=True, maxundo=5)
    self.chapter_resume_text.pack(padx=5, pady=_text_box_pady)

    # Initialize with the first resume
    on_chapter_select()

    # Buttons Area
    self.buttons_frame = tkinter.Frame(self.sugested_chapts_main_frame)
    self.buttons_frame.pack(pady=_btn_pady)

    self.add_chapter_button = tkinter.Button(self.buttons_frame, text="ADD CHAPTER", width=20, bg=_btn_color, fg=_btn_fg,
                                             font=_btn_font, command=lambda: add_new_chapter(self, json_saved_file, json_file_path))
    self.add_chapter_button.pack(side="left", padx=_btn_padx)

    self.delete_chapter_button = tkinter.Button(self.buttons_frame, text="DELETE SELECTED CHAPTER", width=25, bg=_btn_color, fg=_btn_fg,
                                                font=_btn_font, command=delete_selected_chapter)
    self.delete_chapter_button.pack(side="left", padx=_btn_padx)

    self.accept_structure_button = tkinter.Button(self.buttons_frame, text="ACCEPT CHAPTERS STRUCTURE", width=30, bg=_btn_color, fg=_btn_fg,
                                                  font=_btn_font, command= lambda : accept_chapters(self, json_saved_file, json_file_path))
    self.accept_structure_button.pack(side="left", padx=_btn_padx)


# --- Action to accept the chapters structure ---
def accept_chapters(self, json_saved_file, json_file_path):
    #Update the button status to show waiting message
    self.accept_structure_button.config(
        text="Wait, it's generating...",
        bg="white",
        fg="blue",
        font="Arial 9 italic"
    )
    self.accept_structure_button.update_idletasks()
    
    # Update the current chapter in JSON with the textbox content and update de JSON variable
    if hasattr(self, "chapter_resume_text") and hasattr(self, "current_chapter_index"):
        index = self.current_chapter_index
        if 0 <= index < len(json_saved_file.get("Chapters", [])):
            current_text = self.chapter_resume_text.get("1.0", tkinter.END).strip()
            json_saved_file["Chapters"][index][1] = current_text

    # Update JSON saved in disk
    try:
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(json_saved_file, f, indent=4, ensure_ascii=False)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao salvar JSON: {e}")
        return

    # Go to the next window
    create_beats_window(self, json_saved_file, json_file_path, regenerate=True)

# --- Loading function: Creat chapters window from a saved file ---
def load_chapters_window(self, json_saved_file, json_file_path):
    self.window.geometry("800x600+300+0")
    create_chapters_window(self, json_saved_file, json_file_path, regenerate=False)