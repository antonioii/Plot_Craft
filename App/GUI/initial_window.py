import tkinter
from API.set_API import configure_API
from GUI.project_loader import load_project
from GUI.PopUps import manual_functions


def create_initial_content_area(self):
        
        # --- Initial Content Area ---
        self.initial_content_area = tkinter.Frame(self.content_area)
        self.initial_content_area.pack(pady=(45,0))
        
        # Load Project Button
        self.load_project_btn = tkinter.Button(self.initial_content_area, text=" LOAD PROJECT ", bg="black", fg="white",
                                               font="Arial 8 bold", command=lambda: load_project(self))
        self.load_project_btn.pack(side="left", padx=10)

        # New Project Button
        self.new_project_btn = tkinter.Button(self.initial_content_area, text=" NEW PROJECT ", bg="black", fg="white",
                                              font="Arial 8 bold", command=lambda : configure_API(self, from_initial_window=True))
        self.new_project_btn.pack(side="left", padx=10)

        # Instructions Button
        self.default_instructions_btn = tkinter.Button(self.initial_content_area, text=" INSTRUCTIONS ", bg="black", fg="white",
                                                       font="Arial 8 bold",command=manual_functions.open_instructions_html)
        self.default_instructions_btn.pack(side="left", padx=10)

        # --- Footer Notes ---
        self.footer_notes = tkinter.Label(self.content_area, text="Take your time reading instructions, if it's your first time.",
                                          font="Arial 12 italic bold", bg="#EFD5B7")
        self.footer_notes.pack(side="bottom", fill="x", pady=(45,0))