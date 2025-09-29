import tkinter
from tkinter import messagebox
import json

def add_new_beat(self, json_saved_file, json_file_path):
    # --- Create Pop-up ---
    add_beat_window = tkinter.Toplevel()
    add_beat_window.title("Add New Beat")
    add_beat_window.geometry("550x350+450+200")
    add_beat_window.resizable(0, 0)
    add_beat_window.iconbitmap(self._img_icon)

    # --- Main Frame ---
    main_popup_area = tkinter.Frame(add_beat_window)
    main_popup_area.pack(padx=10, pady=10)

    # ================================
    # Frame 1: beat_sets_frame
    # ================================
    beat_sets_frame = tkinter.Frame(main_popup_area)
    beat_sets_frame.pack(pady=(0, 10), anchor="w")

    tkinter.Label(beat_sets_frame, text="Beat Number:").grid(row=0, column=0, sticky="w", padx=5)
    beat_number_entry = tkinter.Entry(beat_sets_frame, width=10)
    beat_number_entry.grid(row=1, column=0, padx=5)

    # ================================
    # Frame 2: beat_resume_frame
    # ================================
    beat_resume_frame = tkinter.Frame(main_popup_area)
    beat_resume_frame.pack(pady=(0, 10), anchor="w")

    tkinter.Label(beat_resume_frame, text="Beat Content:").pack(anchor="w", padx=5)
    beat_content_text = tkinter.Text(beat_resume_frame, width=60, height=8, undo=True, maxundo=5)
    beat_content_text.pack()

    # ================================
    # Frame 3: new_beat_btn
    # ================================
    new_beat_btn = tkinter.Frame(main_popup_area)
    new_beat_btn.pack(pady=(10, 0))

    def save_and_insert_beat():
        try:
            beat_index = int(beat_number_entry.get()) - 1
            beat_content = beat_content_text.get("1.0", "end-1c").strip()

            if not beat_content:
                messagebox.showerror("Erro", "O conteúdo do beat não pode estar vazio.")
                return

            # Find the current chapter index
            selected_label = self.chapter_comboBox.get()
            chapter_index = self.chapter_label_to_index.get(selected_label)

            if chapter_index is None:
                messagebox.showerror("Erro", "Capítulo não selecionado.")
                return

            # Add a beat in the indicated place
            chapter = json_saved_file["Chapters"][chapter_index]
            if len(chapter) < 3:
                chapter.append([])  # Fallback: Create the list of beats if it doesn't exist

            beats = chapter[2]
            if beat_index < 0:
                beat_index = 0
            if beat_index > len(beats):
                beat_index = len(beats)

            beats.insert(beat_index, beat_content)

            # Save local JSON
            with open(json_file_path, 'w', encoding='utf-8') as f:
                json.dump(json_saved_file, f, indent=4, ensure_ascii=False)

            # Update beats screen
            self.beats_main_frame.destroy()
            from GUI.sugests_beats_window import create_beats_window
            create_beats_window(self, json_saved_file, json_file_path)

            # Close Pop-up
            add_beat_window.destroy()

        except ValueError:
            messagebox.showerror("Erro", "O número do beat deve ser um número inteiro.")

    tkinter.Button(
        new_beat_btn,
        text="Add this new beat",
        bg="black", fg="white", font="Arial 8 bold",
        command=save_and_insert_beat
    ).pack()

    # --- Blocking the main screen till Pop-up close ---
    add_beat_window.grab_set()
    self.window.wait_window(add_beat_window)
