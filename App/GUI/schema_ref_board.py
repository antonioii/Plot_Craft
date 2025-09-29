import tkinter, json
from tkinter import messagebox, filedialog
from GUI.sugest_acts_window import create_acts_window
from API.Internal_APIs.handler_apis import ask_LLM_for_schema

def create_ref_schema_board(self, json_saved_file, json_path):
    # --- Get title/resume and ask LLM for schema list ---
    book_title = json_saved_file.get("book_title", "")
    book_resume = json_saved_file.get("book_resume", "")
    place_obj_text, characters_text, noted_happenings_text = ask_LLM_for_schema(book_title, book_resume)

    # --- Re-Create the content area ---
    # Wipe title and resume content area
    self.title_and_resume_area.destroy()
    # Creates the reference schema board area and Button
    self.ref_board_area = tkinter.Frame(self.content_area)
    self.ref_board_area.pack()
    self.accept_ref_board_btn = tkinter.Button(self.content_area, text="Accept Schema", bg="black", fg="white",
                                               font="Arial 8 bold", command=lambda : accept_schema(self, json_saved_file, json_path))
    self.accept_ref_board_btn.pack(pady=5)
    self.window.resizable(0, 0) # This disable resize main window for better aesthetics
    # Creates an invisible label to be show after the btn be clicked
    self.loading_label = tkinter.Label(self.content_area, text="Please wait... generating your references...", fg="blue",
                                       font="Arial 9 italic")
    self.loading_label.pack_forget()

    ## Dimensions for text boxes
    _width = 30
    _height = 20
    _textbox_fg = "black"

    ## Place and Objects
    self.place_obj_area = tkinter.Frame(self.ref_board_area)
    self.place_obj_area.pack(side="left")
    self.place_obj_label = tkinter.Label(self.place_obj_area, text="Main places and objects", font="Arial 8 italic")
    self.place_obj_label.pack()
    self.place_obj_text = tkinter.Text(self.place_obj_area, font="Arial 10", width=_width, height=_height, fg=_textbox_fg,
                                       undo=True, maxundo=5, wrap="word")
    self.place_obj_text.insert("1.0", place_obj_text)
    self.place_obj_text.pack(padx=5)
    
    ## Characters
    self.characters_area = tkinter.Frame(self.ref_board_area)
    self.characters_area.pack(side="left")
    self.characters_label = tkinter.Label(self.characters_area, text="Main characters", font="Arial 8 italic")
    self.characters_label.pack()
    self.characters_text = tkinter.Text(self.characters_area, font="Arial 10", width=_width, height=_height, fg=_textbox_fg,
                                        undo=True, maxundo=5, wrap="word")
    self.characters_text.insert("1.0", characters_text)
    self.characters_text.pack()

    ## Happenings
    self.noted_haps_area = tkinter.Frame(self.ref_board_area)
    self.noted_haps_area.pack(side="left")
    self.noted_haps_label = tkinter.Label(self.noted_haps_area, text="Main Happenings", font="Arial 8 italic")
    self.noted_haps_label.pack()
    self.noted_haps_text = tkinter.Text(self.noted_haps_area, font="Arial 10", width=_width, height=_height, fg=_textbox_fg, 
                                        undo=True, maxundo=5, wrap="word")
    self.noted_haps_text.insert("1.0", noted_happenings_text)
    self.noted_haps_text.pack(padx=5)

# --- Loading function: Create ref. board schema from a saved file ---
def load_ref_schema_board(self, json_saved_file, json_file_path):
    if hasattr(self, "title_and_resume_area"):
        try:
            self.title_and_resume_area.destroy()
        except Exception:
            pass

    self.ref_board_area = tkinter.Frame(self.content_area)
    self.ref_board_area.pack()

    self.accept_ref_board_btn = tkinter.Button(
        self.content_area,
        text="Accept Schema",
        bg="black",
        fg="white",
        font="Arial 8 bold",
        command=lambda: accept_schema(self, json_saved_file, json_file_path),
    )
    self.accept_ref_board_btn.pack(pady=5)

    self.window.resizable(0, 0)
    self.window.geometry("800x600+300+0")
    self.loading_label = tkinter.Label(
        self.content_area,
        text="Adjust your references and click Accept to continue.",
        fg="blue",
        font="Arial 9 italic",
    )
    self.loading_label.pack_forget()

    _width = 30
    _height = 20
    _textbox_fg = "black"

    self.place_obj_area = tkinter.Frame(self.ref_board_area)
    self.place_obj_area.pack(side="left")
    self.place_obj_label = tkinter.Label(self.place_obj_area, text="Main places and objects", font="Arial 8 italic")
    self.place_obj_label.pack()
    self.place_obj_text = tkinter.Text(
        self.place_obj_area,
        font="Arial 10",
        width=_width,
        height=_height,
        fg=_textbox_fg,
        undo=True,
        maxundo=5,
        wrap="word",
    )
    self.place_obj_text.insert("1.0", json_saved_file.get("Places_Objects", ""))
    self.place_obj_text.pack(padx=5)

    self.characters_area = tkinter.Frame(self.ref_board_area)
    self.characters_area.pack(side="left")
    self.characters_label = tkinter.Label(self.characters_area, text="Main characters", font="Arial 8 italic")
    self.characters_label.pack()
    self.characters_text = tkinter.Text(
        self.characters_area,
        font="Arial 10",
        width=_width,
        height=_height,
        fg=_textbox_fg,
        undo=True,
        maxundo=5,
        wrap="word",
    )
    self.characters_text.insert("1.0", json_saved_file.get("Characters", ""))
    self.characters_text.pack()

    self.noted_haps_area = tkinter.Frame(self.ref_board_area)
    self.noted_haps_area.pack(side="left")
    self.noted_haps_label = tkinter.Label(self.noted_haps_area, text="Main Happenings", font="Arial 8 italic")
    self.noted_haps_label.pack()
    self.noted_haps_text = tkinter.Text(
        self.noted_haps_area,
        font="Arial 10",
        width=_width,
        height=_height,
        fg=_textbox_fg,
        undo=True,
        maxundo=5,
        wrap="word",
    )
    self.noted_haps_text.insert("1.0", json_saved_file.get("Happenings", ""))
    self.noted_haps_text.pack(padx=5)

def accept_schema(self, json_saved_file, json_file_path):
    # Show loading message
    self.loading_label.pack(pady=2)
    self.bottom_bar.update_idletasks()

    # Get the text boxes content
    places_objects = self.place_obj_text.get("1.0", "end-1c")
    characters = self.characters_text.get("1.0", "end-1c")
    happenings = self.noted_haps_text.get("1.0", "end-1c")

    # Update JSON file
    json_saved_file["project_phase"] = "1"
    json_saved_file["Places_Objects"] = places_objects
    json_saved_file["Characters"] = characters
    json_saved_file["Happenings"] = happenings

    try:
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(json_saved_file, f, indent=4, ensure_ascii=False)

        # GO TO NEXT WINDOW
        self.loading_label.destroy() # Destroys the invisible loading label
        create_acts_window(self, json_saved_file, json_file_path)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to save file: {str(e)}")

# --- An Unitary test ---
if __name__ == "__main__":
    import os

    class DummyApp:
        def __init__(self, root):
            self.window = root
            self.content_area = tkinter.Frame(self.window)
            self.content_area.pack()
            self.title_and_resume_area = tkinter.Frame(self.content_area)
            self.title_and_resume_area.pack()

            # Loading a JSON for tests
            sample_json_path = "sample_json.json"
            if os.path.exists(sample_json_path):
                with open(sample_json_path, "r", encoding="utf-8") as f:
                    json_data = json.load(f)
            else:
                json_data = {
                    "project_phase": "0",
                    "book_title": "1: The Mystery of the 1th Star",
                    "book_resume": "1: In a world where science fiction shapes destinies, a new hero rises."
                }
                with open(sample_json_path, "w", encoding="utf-8") as f:
                    json.dump(json_data, f, indent=4, ensure_ascii=False)

            # Btn to start tests
            start_button = tkinter.Button(
                self.window,
                text="Start test",
                command=lambda: create_ref_schema_board(self, json_data, sample_json_path)
            )
            start_button.pack(pady=20)

    root = tkinter.Tk()
    root.title("Schema Ref Test")
    root.geometry("700x400+300+200")

    app = DummyApp(root)
    root.mainloop()



