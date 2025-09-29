import tkinter
from GUI.PopUps.popups import Popup_set_API
from GUI.PopUps import manual_functions

def create_default_header(self):
        # --- Header re-config ---
        ## Destroy old logo frame
        self.header_logo_frame.destroy()

        ## Create header buttons
        self.header_buttons_frame = tkinter.Frame(self.header, bd=0)
        self.header_buttons_frame.pack(side="left", pady=0)
        self.instructions_btn = tkinter.Button(self.header_buttons_frame, text="INSTRUCTIONS", bg="black", fg="white",
                                               font="Arial 8 bold", command=manual_functions.open_instructions_html)
        self.instructions_btn.pack(side="left", padx=5, pady=0)

        self.change_model_btn = tkinter.Button(self.header_buttons_frame, text="CHANGE MODEL", bg="black", fg="white",
                                               font="Arial 8 bold", command=lambda:Popup_set_API(self))
        self.change_model_btn.pack(side="left", padx=5)

        ## Create a new header logo frame
        self.header_logo_frame = tkinter.Frame(self.header, bd=0)
        self.header_logo_frame.pack(side="left", padx=105)
        self.header_logo_img = tkinter.Label(self.header_logo_frame, image=self._img_logo_small)
        self.header_logo_img.pack()
        self.header_title_label = tkinter.Label(self.header_logo_frame, text=" Plot Craft by: Antonio Sérgio", font="Arial 8 italic")
        self.header_title_label.pack()

        ## Change header color
        self.header_color = "#9A9A9A"
        self.header.config(background=self.header_color)
        self.header_buttons_frame.config(background=self.header_color)
        self.header_logo_frame.config(background=self.header_color)
        self.header_logo_img.config(background=self.header_color)
        self.header_title_label.config(background=self.header_color)

        ## LLM name Label
        self.llm_info_label = tkinter.Label(self.header_logo_frame, text=f"You are using: {self.llm_model}",
                                            font="Arial 8 bold", bg=self.header_color)
        self.llm_info_label.pack(pady=3)


# --- Unitary test ---
if __name__ == "__main__":
    class App:
        def __init__(self, root):
            self.window = root
            self.window.title("Test Window")
            self.window.geometry("500x200+500+300")

            # Create header frame
            self.header = tkinter.Frame(self.window, height=50)
            self.header.pack(fill="x", side="top")

            # Positioning an image (dummy) inside header
            self._img_logo_small = tkinter.PhotoImage(file="./Assets/logo_small.png")

            # Create an initial logo frame to be destroyed [it's necessary bc of the .destroy() function]
            self.header_logo_frame = tkinter.Frame(self.header)
            self.header_logo_frame.pack()

            # Btn to start unitary test
            start_button = tkinter.Button(
                self.window,
                text="Testar Header",
                command=lambda: create_default_header(self)
            )
            start_button.pack(pady=10)

    root = tkinter.Tk()
    app = App(root)
    root.mainloop()