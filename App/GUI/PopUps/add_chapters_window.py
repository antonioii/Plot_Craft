import tkinter
from tkinter import messagebox
import json

def add_new_chapter(self, json_saved_file, json_file_path):
    # --- Before opens the popup, save the current text box content and update the JSON ---
    if hasattr(self, "chapter_resume_text") and hasattr(self, "current_chapter_index"):
        index = self.current_chapter_index
        if 0 <= index < len(json_saved_file.get("Chapters", [])):
            current_text = self.chapter_resume_text.get("1.0", tkinter.END).strip()
            json_saved_file["Chapters"][index][1] = current_text

    # --- Create the popup window ---
    add_window = tkinter.Toplevel()
    add_window.title("Add New Chapter")
    add_window.geometry("550x400+450+200")
    add_window.resizable(0, 0)
    add_window.iconbitmap(self._img_icon)

    # --- PopUp Content Area ---
    main_frame = tkinter.Frame(add_window)
    main_frame.pack(padx=10, pady=10)

    # --- Chapter Data ---
    frame_data = tkinter.Frame(main_frame)
    frame_data.pack(pady=(5, 10))
    ## Chap. Number
    tkinter.Label(frame_data, text="CHAPTER NUMBER:").grid(row=0, column=0, padx=5, sticky="w")
    chapter_number_entry = tkinter.Entry(frame_data, width=5)
    chapter_number_entry.grid(row=1, column=0, padx=5)
    ## Chap. Name
    tkinter.Label(frame_data, text="CHAPTER NAME:").grid(row=0, column=1, padx=5, sticky="w")
    chapter_name_entry = tkinter.Entry(frame_data, width=30)
    chapter_name_entry.grid(row=1, column=1, padx=5)

    # --- Instructional label ---
    frame_explanation = tkinter.Frame(main_frame)
    frame_explanation.pack(pady=(0, 10))
    explanation = ("Note: The chosen number will be the new position of the chapter.\n"
                   "The following chapters will be pushed down automatically.")
    tkinter.Label(frame_explanation, text=explanation, wraplength=500, justify="left", fg="grey").pack()

    # --- Chapter resume ---
    frame_resume = tkinter.Frame(main_frame)
    frame_resume.pack(pady=(5, 10))
    tkinter.Label(frame_resume, text="CHAPTER RESUME:").pack(anchor="w")
    chapter_resume_text = tkinter.Text(frame_resume, width=60, height=8, undo=True, maxundo=5)
    chapter_resume_text.pack()

    # --- Helper Function: Save and Update ---
    def save_and_reload():
        try:
            idx = int(chapter_number_entry.get()) - 1
            name = chapter_name_entry.get().strip()
            resume = chapter_resume_text.get("1.0", "end-1c").strip()

            if not name or not resume:
                messagebox.showerror("Error", "Nome or resume can't be empty.")
                return

            # Add stub (placeholder) story-beats and create the chapter structure
            beats_stub = [f"CAP{(idx+1)}-BEAT{j}-CONTENT{j}" for j in range(1, 13)]
            new_chapter = [name, resume, beats_stub]

            # Insert new chapter in the correct position
            chapters = json_saved_file.get("Chapters", [])
            if idx < 0: idx = 0
            if idx > len(chapters): idx = len(chapters)
            chapters.insert(idx, new_chapter)

            json_saved_file["Chapters"] = chapters

            # Save JSON
            with open(json_file_path, 'w', encoding='utf-8') as f:
                json.dump(json_saved_file, f, indent=4, ensure_ascii=False)

            # Re-create the chapters window with the new data
            self.sugested_chapts_main_frame.destroy()
            from GUI.sugest_chapters_window import create_chapters_window
            create_chapters_window(self, json_saved_file, json_file_path)

            # Exit
            add_window.destroy()

        except ValueError:
            messagebox.showerror("Error", "The chapter number must be an integer number.")

    # --- Save Button ---
    frame_button = tkinter.Frame(main_frame)
    frame_button.pack(pady=(10, 0))
    save_button = tkinter.Button(frame_button, text="ADD CHAPTER TO LIST", bg="black", fg="white",
                                 font="Arial 8 bold", command=save_and_reload)
    save_button.pack()

    # --- Block the main window till popup exits ---
    add_window.grab_set()               
    self.window.wait_window(add_window) 
