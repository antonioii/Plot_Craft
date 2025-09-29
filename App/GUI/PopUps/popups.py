import tkinter, os
from tkinter import ttk
from GUI.PopUps import manual_functions


# --- Setting API PopUp window ---
def Popup_set_API(self):
    # Windows settings
    windows_color = "#9A9A9A"
    API_popup_window = tkinter.Toplevel()
    API_popup_window.title("Set your API Key")
    API_popup_window.geometry("300x300+550+150")
    API_popup_window.resizable(0, 0)
    API_popup_window.config(background=windows_color)
    API_popup_window.iconbitmap(self._img_icon)

    popup_frame = tkinter.Frame(API_popup_window, bg=windows_color)
    popup_frame.pack()

    # Choose a models section
    model_name_label = tkinter.Label(popup_frame, text="Choose a LLM Model:", font="Arial 11 bold", bg=windows_color)
    model_name_label.pack(padx=5, pady=5)
    model_name = ttk.Combobox(popup_frame, values=get_avaiable_LLMs(), width=25, state="readonly")
    model_name.pack(padx=5, pady=(5, 15))
    model_name.current(0)

    # API Key Section
    model_key_label = tkinter.Label(popup_frame, text="Your API Key:", font="Arial 11 bold", bg=windows_color)
    model_key_label.pack(padx=5, pady=5)
    model_key = tkinter.Entry(popup_frame, width=30, show='*')
    model_key.pack(padx=5, pady=(5, 15))

    # Buttons section
    save_API = tkinter.Button(popup_frame, text=" SAVE PREFERENCES ", bg="black", fg="white",
                              font="Arial 8 bold", command=lambda : save_preferences(self, API_popup_window, model_name.get(), model_key.get()))
    save_API.pack(padx=5, pady=(20, 10))
    instructions_btn = tkinter.Button(popup_frame, text=" INSTRUCTIONS ", bg="black", fg="white",
                              font="Arial 8 bold", command=manual_functions.open_instructions_html)
    instructions_btn.pack(padx=5, pady=5)

    # Block the main window till popup exits
    API_popup_window.grab_set()               
    self.window.wait_window(API_popup_window) 

# --- A list of the Avaiable LLMs ---
def get_avaiable_LLMs():
    values = (
        "gpt-4.1-nano",
        "Gemini-2.5-flash (Google)",
        ". . ."
    )

    return values

# --- Saving the API KEY preferences --
def save_preferences(self, pop_up_window, model_name, model_key):
    # Create folder config/.env:
    folder_path = os.path.join(os.getcwd(), "config")
    os.makedirs(folder_path, exist_ok=True)

    env_file = os.path.join(folder_path, ".env")

    # Delete old env files with APIs, comment to persist them:
    if os.path.exists(env_file):                                
        os.remove(env_file)     

    # Save the variables in .env
    with open(env_file, 'w') as f:
        f.write(f"LLM_MODEL={model_name}\n")
        f.write(f"API_KEY={model_key}\n")

    # Update the LLM model name in header
    self.llm_model = model_name
    if hasattr(self, 'llm_info_label'):
        self.llm_info_label.config(text=f"You are using: {model_name}")


    # Close popup window
    pop_up_window.destroy()

    '''
    To import these saved keys:
    
    from dotenv import load_dotenv
    import os

    load_dotenv(dotenv_path="./config/.env")

    api_key = os.getenv("API_KEY")
    llm_model = os.getenv("LLM_MODEL")
    '''

    


