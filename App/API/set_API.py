from GUI.PopUps.popups import Popup_set_API
from GUI.title_and_resume_window import create_title_and_resume_area
from GUI.project_loader import load_project

# --- Configure internal API calling for the first time ---
def configure_API(self, from_initial_window=False):
    Popup_set_API(self)
    
    if from_initial_window:
                create_title_and_resume_area(self)
    else:
            #placeholder_for_upload(self)
            load_project(self)

    