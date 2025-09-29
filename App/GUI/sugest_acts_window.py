import tkinter, json
from tkinter import messagebox
from GUI.sugest_chapters_window import create_chapters_window
from API.Internal_APIs.handler_apis import ask_LLM_for_acts

def create_acts_window(self, json_saved_file, json_file_path):
    # --- Wipe content area ---
    self.ref_board_area.destroy()
    self.accept_ref_board_btn.destroy()

    # --- Create the window for suggested acts ---
    # Main Area
    self.acts_main_frame = tkinter.Frame(self.content_area)
    self.acts_main_frame.pack()

    # Settings for textbox and labels
    _text_box_width =107
    _text_box_height = 7
    _text_box_fonts = "Arial 10"
    _text_box_pady = 5
    _label_pady = (5, 0)
    _btn_pady = (5, 0)

    # Act 1 Frame
    self.act1_frame = tkinter.Frame(self.acts_main_frame)
    self.act1_frame.pack()
    ## Label
    self.act1_label = tkinter.Label(self.act1_frame, text=" Act One: ")
    self.act1_label.pack(anchor="w", pady=_label_pady)
    ## Text Box
    self.act1_text = tkinter.Text(self.act1_frame, width=_text_box_width, height=_text_box_height, font=_text_box_fonts,
                                  fg="black", undo=True, maxundo=5)
    self.act1_text.pack(pady=_text_box_pady)

    # Act 2 Frame
    self.act2_frame = tkinter.Frame(self.acts_main_frame)
    self.act2_frame.pack()
    ## Label
    self.act2_label = tkinter.Label(self.act2_frame, text=" Act Two: ")
    self.act2_label.pack(anchor="w", pady=_label_pady)
    ## Text Box
    self.act2_text = tkinter.Text(self.act2_frame, width=_text_box_width, height=_text_box_height, font=_text_box_fonts,
                                  fg="black", undo=True, maxundo=5)
    self.act2_text.pack(pady=_text_box_pady)
   
    # Act 3 Frame
    self.act3_frame = tkinter.Frame(self.acts_main_frame)
    self.act3_frame.pack()
    ## Label
    self.act3_label = tkinter.Label(self.act3_frame, text=" Act Three: ")
    self.act3_label.pack(anchor="w", pady=_label_pady)
    ## Text Box
    self.act3_text = tkinter.Text(self.act3_frame, width=_text_box_width, height=_text_box_height, font=_text_box_fonts,
                                  fg="black", undo=True, maxundo=5)
    self.act3_text.pack(pady=_text_box_pady)

    # Accept acts Button
    self.accept_acts_btn = tkinter.Button(self.acts_main_frame, text="Accept Main Acts", bg="black", fg="white",
                                          font="Arial 8 bold", command= lambda : accept_acts(self, json_saved_file, json_file_path))
    self.accept_acts_btn.pack(pady=_btn_pady)

    # --- Generates the acts ---
    # Take info from the actual JSON
    book_title     = json_saved_file.get("book_title", "")
    book_resume    = json_saved_file.get("book_resume", "")
    places_objects = json_saved_file.get("Places_Objects", "")
    characters     = json_saved_file.get("Characters", "")
    happenings     = json_saved_file.get("Happenings", "")

    # Call LLM to generate acts
    try:
        acts_list = ask_LLM_for_acts(
            book_title,
            book_resume,
            places_objects,
            characters,
            happenings
        ) or []
    except Exception as e:
        acts_list = [f"Erro ao gerar atos: {e}", "", ""]

    while len(acts_list) < 3:
        acts_list.append("")

    act1_gen, act2_gen, act3_gen = acts_list[:3]

    # Fill the acts textboxes
    self.act1_text.delete("1.0", "end")
    self.act1_text.insert("1.0", act1_gen)

    self.act2_text.delete("1.0", "end")
    self.act2_text.insert("1.0", act2_gen)

    self.act3_text.delete("1.0", "end")
    self.act3_text.insert("1.0", act3_gen)

    # Automatic save the JSON after loading
    json_saved_file["project_phase"] = "2"
    json_saved_file["Act1"] = act1_gen
    json_saved_file["Act2"] = act2_gen
    json_saved_file["Act3"] = act3_gen
    try:
        with open(json_file_path, "w", encoding="utf-8") as f:
            import json as _json
            _json.dump(json_saved_file, f, indent=4, ensure_ascii=False)
    except Exception as _e:
        pass
 
# --- Loading function: create acts window from a saved file ---
def load_acts_window(self, json_saved_file, json_file_path):
    for attr in ("ref_board_area", "accept_ref_board_btn"):
        if hasattr(self, attr):
            try:
                getattr(self, attr).destroy()
            except Exception:
                pass

    self.acts_main_frame = tkinter.Frame(self.content_area)
    self.acts_main_frame.pack()
    self.window.resizable(1,1)
    self.window.geometry("800x600+300+0")

    _text_box_width = 107
    _text_box_height = 7
    _text_box_fonts = "Arial 10"
    _text_box_pady = 5
    _label_pady = (5, 0)
    _btn_pady = (5, 0)

    self.act1_frame = tkinter.Frame(self.acts_main_frame)
    self.act1_frame.pack()
    self.act1_label = tkinter.Label(self.act1_frame, text=" Act One: ")
    self.act1_label.pack(anchor="w", pady=_label_pady)
    self.act1_text = tkinter.Text(self.act1_frame, width=_text_box_width, height=_text_box_height, font=_text_box_fonts,
                                  fg="black", undo=True, maxundo=5)
    self.act1_text.insert("1.0", json_saved_file.get("Act1", ""))
    self.act1_text.pack(pady=_text_box_pady)

    self.act2_frame = tkinter.Frame(self.acts_main_frame)
    self.act2_frame.pack()
    self.act2_label = tkinter.Label(self.act2_frame, text=" Act Two: ")
    self.act2_label.pack(anchor="w", pady=_label_pady)
    self.act2_text = tkinter.Text(self.act2_frame, width=_text_box_width, height=_text_box_height, font=_text_box_fonts,
                                  fg="black", undo=True, maxundo=5)
    self.act2_text.insert("1.0", json_saved_file.get("Act2", ""))
    self.act2_text.pack(pady=_text_box_pady)

    self.act3_frame = tkinter.Frame(self.acts_main_frame)
    self.act3_frame.pack()
    self.act3_label = tkinter.Label(self.act3_frame, text=" Act Three: ")
    self.act3_label.pack(anchor="w", pady=_label_pady)
    self.act3_text = tkinter.Text(self.act3_frame, width=_text_box_width, height=_text_box_height, font=_text_box_fonts,
                                  fg="black", undo=True, maxundo=5)
    self.act3_text.insert("1.0", json_saved_file.get("Act3", ""))
    self.act3_text.pack(pady=_text_box_pady)

    self.accept_acts_btn = tkinter.Button(
        self.acts_main_frame,
        text="Accept Main Acts",
        bg="black",
        fg="white",
        font="Arial 8 bold",
        command=lambda: accept_acts(self, json_saved_file, json_file_path),
    )
    self.accept_acts_btn.pack(pady=_btn_pady)

# --- Function to accept the acts ---
def accept_acts(self, json_saved_file, json_file_path):
    # Change the button text to inform about processing
    self.accept_acts_btn.config(
        text="Wait, generating...",
        bg="white",
        fg="blue",
        font="Arial 9 italic"
    )
    # Force the btn to update its visual
    self.accept_acts_btn.update_idletasks()

    # Get the Acts content
    act1_content = self.act1_text.get("1.0", "end-1c")
    act2_content = self.act2_text.get("1.0", "end-1c")
    act3_content = self.act3_text.get("1.0", "end-1c")

    # Update JSON file
    json_saved_file["project_phase"] = "2"
    json_saved_file["Act1"] = act1_content
    json_saved_file["Act2"] = act2_content
    json_saved_file["Act3"] = act3_content

    try:
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(json_saved_file, f, indent=4, ensure_ascii=False)

        ## GOING TO THE NEXT WINDOW
        create_chapters_window(self, json_saved_file, json_file_path)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save file: {str(e)}")