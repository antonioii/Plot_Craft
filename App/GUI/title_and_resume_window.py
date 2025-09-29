import json, tkinter
from tkinter import filedialog, messagebox
from GUI.windows_header import create_default_header
from GUI.PopUps.title_and_resume_sugests import back_to_title_and_resume_window
from GUI.text_editor_opt.text_editor_opt import (
        on_title_entry_click, on_title_entry_focus_out,
        on_description_text_click, on_description_text_focus_out,
        entry_undo, entry_redo, on_entry_key
)
from GUI.schema_ref_board import create_ref_schema_board

# --- Create new area for titles and resume --- 
def create_title_and_resume_area(self):
             
        # --- New Window Configurations ---
        self.window.resizable(1,1)
        self.window.geometry("800x600+300+0")

        #  --- Recreates the header ---        
        create_default_header(self)

        # --- Recreates the content area ---
        self.initial_content_area.destroy()
        self.footer_notes.destroy()
        self.title_and_resume_area = tkinter.Frame(self.content_area)
        self.title_and_resume_area.pack(pady=20)

        # Checkbox
        self.checkbox_var = tkinter.IntVar()
        self.checkbox = tkinter.Checkbutton(self.title_and_resume_area, text="Mark this checkbox if you don’t already have a title or a description for your book.",
                                        variable=self.checkbox_var, command=lambda : check_box_action(self))
        self.checkbox.pack(pady=(15,10))

        # Title Field
        self.title_entry_label = tkinter.Label(self.title_and_resume_area, text="Title: ", font="Arial 11 bold")
        self.title_entry_label.pack(anchor="w")
        self.title_entry = tkinter.Entry(self.title_and_resume_area, font="Arial 10", width=60, fg='grey')
        title_place_holder = "Title..."
        self.title_entry.insert(0, title_place_holder)
        self.title_entry.bind('<FocusIn>', lambda event: on_title_entry_click(event, title_place_holder, self.title_entry))
        self.title_entry.bind('<FocusOut>', lambda event: on_title_entry_focus_out(event, title_place_holder, self.title_entry))
        ## Undo/redo functions in the title field
        self.title_entry_undo_stack = []
        self.title_entry_redo_stack = []
        self.title_entry.bind('<Key>', lambda event: on_entry_key(event, self.title_entry, self.title_entry_undo_stack, self.title_entry_redo_stack))
        self.title_entry.bind('<Control-z>', lambda event: entry_undo(event, self.title_entry, self.title_entry_undo_stack, self.title_entry_redo_stack))
        self.title_entry.bind('<Control-y>', lambda event: entry_redo(event, self.title_entry, self.title_entry_undo_stack, self.title_entry_redo_stack))
        self.title_entry.pack(pady=(5, 20))

        # Resume Field
        self.description_text_label = tkinter.Label(self.title_and_resume_area, text="Resume: ", font="Arial 11 bold")
        self.description_text_label.pack(anchor="w")
        self.description_text = tkinter.Text(self.title_and_resume_area, font="Arial 10", width=60, height=15, fg='grey',
                                             undo=True, maxundo=5, wrap="word")
        self.description_text.insert("1.0", "Book brief description...")
        self.description_text.bind('<FocusIn>', lambda event: on_description_text_click(event, self.description_text))
        self.description_text.bind('<FocusOut>', lambda event: on_description_text_focus_out(event, self.description_text))      
        self.description_text.pack(pady=5)

        # Outline button
        self.bottom_bar = tkinter.Frame(self.title_and_resume_area)
        self.bottom_bar.pack(pady=15)
        self.outline_btn = tkinter.Button(self.bottom_bar, text="OUTLINE MY PLOT", bg="black", fg="white", font="Arial 8 bold",
                                          command=lambda: handle_outline_btn_with_feedback(self))
        self.outline_btn.pack(side="left", padx=20)
        ## Invisite label to display loading
        self.loading_label = tkinter.Label(self.bottom_bar, text="Please wait... generating your references...", fg="blue", font="Arial 9 italic")
        self.loading_label.pack_forget()

# --- Loading function: Create area from a saved file ---
def load_title_and_resume_area(self, json_saved_file, json_path):
        create_title_and_resume_area(self)

        self.checkbox_var.set(0)

        saved_title = json_saved_file.get("book_title", "")
        saved_resume = json_saved_file.get("book_resume", "")

        self.title_entry.config(state="normal", fg="black")
        self.title_entry.delete(0, "end")
        if saved_title:
                self.title_entry.insert(0, saved_title)

        self.description_text.config(state="normal", fg="black")
        self.description_text.delete("1.0", "end")
        if saved_resume:
                self.description_text.insert("1.0", saved_resume)

        def _continue_outline():
                json_saved_file["book_title"] = self.title_entry.get()
                json_saved_file["book_resume"] = self.description_text.get("1.0", "end-1c")
                json_saved_file["project_phase"] = "0"
                try:
                        with open(json_path, "w", encoding="utf-8") as file_obj:
                                json.dump(json_saved_file, file_obj, indent=4, ensure_ascii=False)
                except Exception as exc:
                        messagebox.showerror("Error", f"Failed to update the project file: {exc}")
                        return
                create_ref_schema_board(self, json_saved_file, json_path)

        self.outline_btn.config(
                state="normal",
                text="OUTLINE MY PLOT",
                bg="black",
                fg="white",
                command=_continue_outline,
        )
        self.loading_label.pack_forget()

# --- Checkbox action---
def check_box_action(self):
        # Reset Place Holders
        self.title_entry.config(state="normal", fg='grey')
        self.title_entry.delete(0, 'end')
        self.title_entry.insert(0, "Title...")
        self.description_text.config(state="normal", fg='grey')
        self.description_text.delete("1.0", "end")
        self.description_text.insert("1.0", "Book brief description...")
        # Disable/Enable entry and text fields
        if self.checkbox_var.get():
                self.title_entry.config(state="disabled")
                self.description_text.config(state="disabled")
        else:
                self.title_entry.config(state="normal")
                self.description_text.config(state="normal")
                self.checkbox.focus_set()


# --- Outline button action ---
def handle_outline_btn_with_feedback(self):
    if self.checkbox_var.get() == 1:
        back_to_title_and_resume_window(self)
        return

    self.outline_btn.config(state="disabled", text="Please wait...", bg="#555555")
    self.loading_label.pack(side="left", padx=10)
    self.window.update_idletasks()

    title = str(self.title_entry.get())
    resume = str(self.description_text.get("1.0", "end-1c"))
    json_saved_file = {
        "project_phase": "0",
        "book_title": title,
        "book_resume": resume,
        "Places_Objects": "",
        "Characters": "",
        "Happenings": "",
        "Act1": "",
        "Act2": "",
        "Act3": "",
        "Chapters": []
    }

    file_path = Save_JSON(json_saved_file)
    if file_path:
        create_ref_schema_board(self, json_saved_file, file_path)
        return
    else:
        self.loading_label.pack_forget()
        self.outline_btn.config(state="normal", text="OUTLINE MY PLOT", bg="black")
        messagebox.showerror("Error", f"Refferences weren't loaded!")
                        

# --- Save Json ---
def Save_JSON(json_saved_file):  
        # Saving the JSON file
        file_path = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("JSON files", "*.json")],
        title="Save Project File"
        )

        if file_path:  # if user didn't cancel the saving proccess
                try:
                        with open(file_path, 'w', encoding='utf-8') as json_file:
                                json.dump(json_saved_file, json_file, ensure_ascii=False, indent=4)
                                return file_path
                except Exception:
                        messagebox.showerror("Error", f"Project was not saved!")
                        return None
                else:
                        messagebox.showwarning("Canceled", "No file was saved!")
                        return None
