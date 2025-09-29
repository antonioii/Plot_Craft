import tkinter, json
from tkinter import ttk, messagebox
from GUI.PopUps.add_beats_window import add_new_beat
from GUI.finishing_writing_window import create_final_writing
from API.Internal_APIs.handler_apis import ask_LLM_for_beats


def create_beats_window(self, json_saved_file, json_file_path, regenerate=False):
    # --- Generate beats if they do not exist, if regenerate=True ---
    def _needs_generation(book_json: dict) -> bool:
        for ch in book_json.get("Chapters", []):
            beats = ch[2] if len(ch) > 2 else []
            if not beats:
                return True
        return False

    if regenerate or _needs_generation(json_saved_file):
        try:
            beats_payload = ask_LLM_for_beats(json_saved_file) or {}
        except Exception as e:
            beats_payload = {"Chapters": [[f"Erro ao gerar beats: {e}", "", [f"CAP1-BEAT{j}-CONTENT{j}-ATUALIZADO" for j in range(1,13)]]]}

        chapters_list = beats_payload.get("Chapters", [])
        if isinstance(chapters_list, list) and chapters_list:
            json_saved_file["Chapters"] = chapters_list
            json_saved_file["project_phase"] = "4"  # Update the project phase

            if json_file_path:
                with open(json_file_path, 'w', encoding='utf-8') as f:
                    json.dump(json_saved_file, f, indent=4, ensure_ascii=False)

    # --- Settings for text areas, labels and buttons ---
    _text_box_width = 107
    _text_box_height = 12
    _text_box_fonts = "Arial 10"
    _btn_pady = (5, 5)
    _btn_padx = 5
    _btn_color = "black"
    _btn_fg = "white"
    _btn_font = "Arial 8 bold"

    # --- Helper Function: get list of beats ---
    self.beats_list_var = None
    def get_beats_list():
        selected_label = self.chapter_comboBox.get()
        chapter_index = self.chapter_label_to_index.get(selected_label)

        if chapter_index is not None:
            beats = json_saved_file["Chapters"][chapter_index][2]
            self.beats_list_var = beats
            return [f"BEAT {i+1}" for i in range(len(beats))]
        else:
            self.beats_list_var = []
            return []


    # --- Helper Function: update comboBox beats per selected chapter ---
    def update_beats_comboBox(event=None):        
        beat_labels = get_beats_list()
        self.beats_comboBox["values"] = beat_labels
        if beat_labels:
            self.beats_comboBox.current(0)
            load_selected_beat()
        else:
            self.beats_comboBox.set("")
            self.resume_beats_text_area.delete("1.0", tkinter.END)

    # --- Helper Functions: save JSON ---
    self.curr_text_indication_beat_box = None  # (chapter_index, beat_index)
    def save_current_beat_text():
        if self.curr_text_indication_beat_box is not None:
            chapter_index, beat_index = self.curr_text_indication_beat_box
            if 0 <= chapter_index < len(json_saved_file["Chapters"]):
                beats = json_saved_file["Chapters"][chapter_index][2]
                if 0 <= beat_index < len(beats):
                    current_text = self.resume_beats_text_area.get("1.0", tkinter.END).strip()
                    json_saved_file["Chapters"][chapter_index][2][beat_index] = current_text
                    try:
                        with open(json_file_path, 'w', encoding='utf-8') as f:
                            json.dump(json_saved_file, f, indent=4, ensure_ascii=False)
                    except Exception as e:
                        messagebox.showerror("Error", f"Error saving the JSON file: {e}")


    # --- Helper Function: Load selected beat into the TextBox and save the previous one ---
    def load_selected_beat(event=None):
        # Save the current text using the self.curr_text... refference
        save_current_beat_text()

        # Get chapter index
        selected_chapter_label = self.chapter_comboBox.get()
        chapter_index = self.chapter_label_to_index.get(selected_chapter_label)
        if chapter_index is None:
            return

        # Within current chapter, get the beat index
        beat_index = self.beats_comboBox.current()
        beats = json_saved_file["Chapters"][chapter_index][2]
        
        if 0 <= beat_index < len(beats): # If a valid index, we load is content
            selected_beat_text = beats[beat_index]
            self.resume_beats_text_area.delete("1.0", tkinter.END)
            self.resume_beats_text_area.insert("1.0", selected_beat_text)

            '''
            Update the refference variable with the new position in order to
            the next saving know where to save the edited text: '''
            self.curr_text_indication_beat_box = (chapter_index, beat_index)

    # --- Helper Function: Accept Btn Action: ---
    def accept_all_beats(self, json_saved_file, json_file_path):
        try:
            save_current_beat_text()
        except Exception as e:
            messagebox.showerror("Error", f"Error saving the current beat: {e}")
            return
        
        #Update button to show waiting message to user
        self.accept_all_beats.config(
            text="Wait, it's generating...",
            bg="white",
            fg="blue",
            font="Arial 9 italic"
        )
        self.accept_all_beats.update_idletasks()

        # Ensure the project phase update and persistence
        json_saved_file["project_phase"] = "4"
        if json_file_path:
            try:
                with open(json_file_path, 'w', encoding='utf-8') as f:
                    json.dump(json_saved_file, f, indent=4, ensure_ascii=False)
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar JSON: {e}")
                return

        # Going to the final window (finishing_writing_window)
        create_final_writing(self, json_saved_file, json_file_path)
    
    # --- Action Function: get explanations about what is a beat ---
    def what_is_a_beat():
        messagebox.showinfo(
            "What is a (Story) Beat?",
            "A story beat is a specific moment or event in a narrative that represents a change, decision, action, or important revelation.\n\n"
            "These moments structure the story, marking plot progressions and character development. They are the fundamental building blocks that keep the story moving forward.\n\n"
            "You can think of story beats as subchapters or the essential parts that make up a chapter."
        )

    # --- Action Function: delete a selected beat ---
    def delete_selected_beat():
        selected_chapter_label = self.chapter_comboBox.get()
        chapter_index = self.chapter_label_to_index.get(selected_chapter_label)
        beat_index = self.beats_comboBox.current()

        if chapter_index is None or beat_index < 0:
            messagebox.showwarning("Warning", "Select a chapter and a beat to delete.")
            return

        beats = json_saved_file["Chapters"][chapter_index][2]
        if beat_index >= len(beats):
            messagebox.showerror("Error", "Invalid or Non-existent Beat.")
            return

        confirm = messagebox.askyesno("Confirmation", f"Do you want to delete the BEAT: {beat_index + 1}?")
        if not confirm:
            return

        # Delete the selected beat
        del beats[beat_index]

        # Save JSON in disc
        try:
            with open(json_file_path, 'w', encoding='utf-8') as f:
                json.dump(json_saved_file, f, indent=4, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("Error", f"Error saving the JSON file: {e}")
            return

        # Update the combobox beats
        updated_beats_labels = get_beats_list()
        self.beats_comboBox['values'] = updated_beats_labels

        if updated_beats_labels:
            new_index = min(beat_index, len(updated_beats_labels) - 1)
            self.beats_comboBox.current(new_index)
            self.curr_text_indication_beat_box = (chapter_index, new_index)
            self.resume_beats_text_area.delete("1.0", tkinter.END)
            self.resume_beats_text_area.insert("1.0", beats[new_index])
        else:
            self.beats_comboBox.set("")
            self.resume_beats_text_area.delete("1.0", tkinter.END)
            self.curr_text_indication_beat_box = None


    # --- Re-create content area and resize window ---
    # Wipe content area
    if hasattr(self, "sugested_chapts_main_frame") and self.sugested_chapts_main_frame:
        try:
            self.sugested_chapts_main_frame.destroy()
        except:
            pass

    # New area
    self.beats_main_frame = tkinter.Frame(self.content_area)    
    self.beats_main_frame.pack()  
    # New window size
    self.window.geometry("800x500+300+0")
    
    # --- Chapter/Beats Selection area ---
    # Main
    self.selection_area = tkinter.Frame(self.beats_main_frame)
    self.selection_area.pack(pady=(15,0))

    ## Chapters ComboBox
    self.chapters_area = tkinter.Frame(self.selection_area)
    self.chapters_area.pack(side="left")
    self.chapters_label = tkinter.Label(self.chapters_area, text=" CHAPTERS: ")
    self.chapters_label.pack()
    ### Maping the chapters: e.g, "CHAPTER 1 - XYZ" => 0, etc.
    self.chapter_label_to_index = {
        f"CHAPTER {i+1} - {ch[0]}": i for i, ch in enumerate(json_saved_file.get("Chapters", []))
    }
    ### Create the comboBox with the mapped chapters
    self.chapter_comboBox = ttk.Combobox(self.chapters_area, values=list(self.chapter_label_to_index.keys()), width=50, state="readonly")
    self.chapter_comboBox.pack()
    self.chapter_comboBox.current(0)
    ### ComboBox Bind
    self.chapter_comboBox.bind("<<ComboboxSelected>>", update_beats_comboBox)
    ## Beats ComboBox
    self.beats_area = tkinter.Frame(self.selection_area)
    self.beats_area.pack(side="left")
    self.beats_label = tkinter.Label(self.chapters_area, text=" SELECT A STORY BEAT: ")
    self.beats_label.pack()
    self.beats_comboBox = ttk.Combobox(self.chapters_area, values=get_beats_list(), width=50, state="readonly")
    self.beats_comboBox.pack()
    ### ComboBox Bind
    self.beats_comboBox.bind("<<ComboboxSelected>>", load_selected_beat)
    ## Explanation
    self.what_is_a_beat_btn = tkinter.Button(self.selection_area, text=" What is a BEAT? ", width=20, bg=_btn_color, fg=_btn_fg,
                                             font=_btn_font, command=what_is_a_beat)
    self.what_is_a_beat_btn.pack(padx=30, pady=(30, 0))

    # --- Beats Resume area ---
    self.resume_beats_area = tkinter.Frame(self.beats_main_frame)
    self.resume_beats_area.pack(pady=20)    
    self.resume_beats_label = tkinter.Label(self.resume_beats_area, text=" RESUME: ")
    self.resume_beats_label.pack()
    self.resume_beats_text_area = tkinter.Text(self.resume_beats_area, height=_text_box_height, width=_text_box_width,
                                            font=_text_box_fonts, undo=True, maxundo=5)
    self.resume_beats_text_area.pack()

    # --- Buttons area ---
    self.resume_beats_btn_area = tkinter.Frame(self.beats_main_frame)
    self.resume_beats_btn_area.pack()

    # Add new beat btn
    self.add_new_beat = tkinter.Button(self.resume_beats_btn_area, text=" ADD A NEW BEAT ", width=20, bg=_btn_color, fg=_btn_fg,
                                             font=_btn_font, command=lambda: add_new_beat(self, json_saved_file, json_file_path))
    self.add_new_beat.pack(side="left", padx=_btn_padx, pady=_btn_pady)

    # Delete selected beat btn
    self.delete_beat = tkinter.Button(self.resume_beats_btn_area, text=" DELETE THIS BEAT ", width=20, bg=_btn_color, fg=_btn_fg,
                                             font=_btn_font, command=delete_selected_beat)
    self.delete_beat.pack(side="left", padx=_btn_padx, pady=_btn_pady)
    
    # Acc all beats btn
    self.accept_all_beats = tkinter.Button(
        self.resume_beats_btn_area,
        text=" ACCEPT ALL ",
        width=20, bg=_btn_color, fg=_btn_fg, font=_btn_font,
        command=lambda: accept_all_beats(self, json_saved_file, json_file_path)
    )
    self.accept_all_beats.pack(side="left", padx=_btn_padx, pady=_btn_pady)

# --- Loading function: Creat beats from a saved file ---
def load_beats_window(self, json_saved_file, json_file_path):
    create_beats_window(self, json_saved_file, json_file_path, regenerate=False)