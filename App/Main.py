import tkinter
from GUI.initial_window import create_initial_content_area
from dotenv import load_dotenv
import os

class Main_Window():
    def __init__(self):
        # --- Windows config ---
        self.window = tkinter.Tk()
        self.window.title("Plot Craft")
        self.window.geometry("600x380+400+150")
        self.window.resizable(0, 0)

        self._img_icon = "./Assets/icon.ico"
        self.window.iconbitmap(self._img_icon)        
        self._img_logo_medium = tkinter.PhotoImage(file="./Assets/logo_medium.png")
        self._img_logo_small = tkinter.PhotoImage(file="./Assets/logo_small.png")
    
        # --- Header config ---
        self.header = tkinter.Frame(self.window)
        self.header.pack(fill="x")
        self.header_logo_frame = tkinter.Frame(self.header)
        self.header_logo_frame.pack()
        self.header_logo_img = tkinter.Label(self.header_logo_frame, image=self._img_logo_medium)
        self.header_logo_img.pack()
        self.header_title_label = tkinter.Label(self.header_logo_frame, text=" Plot Craft by: Antonio Sérgio", font="Arial 10")
        self.header_title_label.pack()
        ## LLM model name initializing vars
        load_dotenv(dotenv_path="./config/.env")
        self.llm_model = os.getenv("LLM_MODEL") or "No LLM is working"

        
        # --- Basic Content Area Config ---
        self.content_area = tkinter.Frame(self.window)
        self.content_area.pack(fill="x")
        
        # Inicializa a área inicial:
        create_initial_content_area(self)

        
        # --- Maintaining the window running ---
        self.window.mainloop()       


# --- Executa a janela ---
Main_Window()
