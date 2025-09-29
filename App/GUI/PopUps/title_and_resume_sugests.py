import tkinter
from tkinter import ttk
import GUI.text_editor_opt.text_editor_opt as teo
from API.Internal_APIs.handler_apis import ask_LLM as call_internal_api

def make_title_and_resume_sugests(self):
    # --- PopUp Windows config ---
    sugestions_window = tkinter.Toplevel()
    sugestions_window.title("Generate sugestions for Title and Resume")
    sugestions_window.geometry("800x330+300+125")
    sugestions_window.resizable(0,0)
    sugestions_window.iconbitmap(self._img_icon)

    # --- Frame: Setting parameters to sugest ---
    parameters_frame = tkinter.Frame(sugestions_window)
    parameters_frame.pack(side="left", padx=(15, 10), pady=0, fill="both")
    
    # Invisible label to display when we are making requests to external LLM APIs
    loading_label = tkinter.Label(parameters_frame, text="Loading suggestions, please wait...", fg="blue", font="Arial 9 italic")
    loading_label.pack_forget()

    parameters = [
        "Genre: ",
        "Book Market Category: ",
        "Secondary Genre: ",
        "Format: ",
        "Tone/Style: "
    ]
    placeholders = [
        'Science Fiction, Fantasy, etc...',
        'Beach Read, Young Adult, Self-Help, etc...',
        'Romance, Thriller, Historical Fiction, etc...',
        'Hardcover, Paperback, Ebook, etc...',
        'Humorous, Dark, Inspirational, etc...'
    ]
    # Dictionary for the entry boxes elements
    entry_boxes = {}
    # Creating the entry boxes with labels
    for index, param in enumerate(parameters):
        label = tkinter.Label(parameters_frame, text=param)
        label.pack(anchor="w", pady=(5, 0))
        entry = tkinter.Entry(parameters_frame, width=40)
        entry.pack(anchor="w", pady=(0, 5))
        entry_boxes[param] = entry
        # Place Holders:
        placeholder_text = placeholders[index]
        entry.insert(0, placeholder_text)
        entry.config(fg='grey')
        entry.bind("<FocusIn>", lambda event, e=entry, p=placeholder_text: teo.on_title_entry_click(event, p, entry=e))
        entry.bind("<FocusOut>", lambda event, e=entry, p=placeholder_text: teo.on_title_entry_focus_out(event, p, entry=e))


    # Creating give me sugestions button
    give_me_sugests_btn = tkinter.Button(parameters_frame, text=" Give me Sugestions ", bg="black", fg="white", 
                                         font="Arial 8 bold", command=lambda: handle_with_loading())    
    give_me_sugests_btn.pack(pady=15)
    ## Button action
    def handle_with_loading():
        give_me_sugests_btn.config(state="disabled", text="Please wait...", bg="#555555") # Change the btn color
        loading_label.pack(pady=(5, 5))                                                     # Display the invisible label
        sugestions_window.update_idletasks()                                                # Force popup update
        ask_LLM(self, entry_boxes, sugestions_textbox, real_suggestions_list)               # Make the external LLM request
        loading_label.pack_forget()                                                         # Make label invisible again
        give_me_sugests_btn.config(state="normal", text=" Give me Sugestions ", bg="black") # Change the btn color back


    #  --- Arrow separing the frame areas
    visual_arrow = tkinter.Label(sugestions_window, text=" ==> ")
    visual_arrow.pack(side="left", padx=5, pady=0, fill="both")

    # --- Frame: Sugestions from the LLM ---
    sugestions_frame = tkinter.Frame(sugestions_window)
    sugestions_frame.pack(side="left", padx=(15, 10), pady=0, fill="both")
    # Scroll Bar
    text_frame = tkinter.Frame(sugestions_frame)
    text_frame.pack(pady=(5, 10))
    scrollbar = tkinter.Scrollbar(text_frame)
    scrollbar.pack(side="right", fill="y")
    
    #Textbox to show suggestions
    sugestions_textbox = tkinter.Text(text_frame, width=60, height=15, wrap="word",
                                      bg="white", state="disabled", yscrollcommand=scrollbar.set)
    sugestions_textbox.pack(side="left", fill="both", expand=True, pady=(5, 10))

    scrollbar.config(command=sugestions_textbox.yview)
    
    #Frame for Option selection
    option_frame = tkinter.Frame(sugestions_frame)
    option_frame.pack(pady=(0, 5))
    # Option Label
    option_label = tkinter.Label(option_frame, text="Option:")
    option_label.pack(side="left", padx=(0,5))
    # Option Combobox
    option_combobox = ttk.Combobox(option_frame, width=5, state="readonly")
    option_combobox['values'] = list(range(1, 21))  # From 1 to 20
    option_combobox.current(0)
    option_combobox.pack(side="left", padx=(0,5))
    # Variables with the sugestions content:
    selected_suggestion = {"title": "", "resume": ""}
    real_suggestions_list = []
    # Choose Plot Button
    choose_plot_button = tkinter.Button(option_frame, text="Choose Plot", bg="black", fg="white", font="Arial 8 bold",
                                        command=lambda opts=option_combobox, selected=selected_suggestion, window=sugestions_window:
                                        choose_plot(opts, real_suggestions_list, selected, window))   
    choose_plot_button.pack(side="left") 

    # --- Block main window ---
    sugestions_window.grab_set()               
    self.window.wait_window(sugestions_window)

    # --- Return the variable with the sugestions content ---
    return selected_suggestion

def choose_plot(option_combobox, suggestions_list, selected_suggestion, sugestions_window):
    try:
        option_index = int(option_combobox.get()) - 1
        if option_index < 0 or option_index >= len(suggestions_list):
            raise IndexError("Option number is out of the given range!")

        chosen = suggestions_list[option_index]
        lines = chosen.split("\n", 1)
        selected_suggestion["title"] = lines[0].strip()
        selected_suggestion["resume"] = lines[1].strip() if len(lines) > 1 else ""
        sugestions_window.destroy()
    except Exception as e:
        print("Error choosing suggestion:", e)

def ask_LLM(self, entry_boxes, sugestions_textbox, real_suggestions_list=None):
    # Get parameters from interface
    parameters = {
        "Genre": entry_boxes["Genre: "].get(),
        "Book Market Category": entry_boxes["Book Market Category: "].get(),
        "Secondary Genre": entry_boxes["Secondary Genre: "].get(),
        "Format": entry_boxes["Format: "].get(),
        "Tone/Style": entry_boxes["Tone/Style: "].get()
    }

    # Call the internal API Handler
    suggestions = call_internal_api(parameters)

    # Complete the list with the real suggestions (which will be used to the choose_plot function)
    if real_suggestions_list is not None:
        real_suggestions_list.clear()
        real_suggestions_list.extend(suggestions)

    # Display interface
    sugestions_textbox.config(state="normal")
    sugestions_textbox.delete(1.0, "end")
    sugestions_textbox.insert("end", "\n\n".join(suggestions))
    sugestions_textbox.config(state="disabled")

def back_to_title_and_resume_window(self):
    suggestion = make_title_and_resume_sugests(self)
    
    if suggestion["title"] and suggestion["resume"]:
        # Enable the fields
        self.title_entry.config(state="normal", fg="black")
        self.description_text.config(state="normal", fg="black")

        # Insert title
        self.title_entry.delete(0, "end")
        self.title_entry.insert(0, suggestion["title"])

        # Insert resume
        self.description_text.delete("1.0", "end")
        self.description_text.insert("1.0", suggestion["resume"])

        # Disable checkbox
        self.checkbox_var.set(0)

''' Unitary test '''
if __name__ == "__main__":
    class App:
        def __init__(self, root):
            self.window = root
            self._img_icon = None  

            # Start test button
            start_button = tkinter.Button(
                root,
                text="Start test",
                command=self.start_test
            )
            start_button.pack(pady=20)

        # Start test action
        def start_test(self):
            make_title_and_resume_sugests(self)

    root = tkinter.Tk()
    root.title("Test Window")
    root.geometry("300x150+500+300")

    app = App(root)
    root.mainloop()