import tkinter

'''
This module contains functions to improve the writing in entry boxes and text fields
'''

# --- Funções de placeholder para o Entry ---
def on_title_entry_click(event, title, entry='enable'): # Title is the string to be set in placeholder
    if entry['state'] == 'disabled':                    # Usefull if a checkbox to disable the field is set on               
        return 
    if entry.get() == title:
        entry.delete(0, tkinter.END)
        entry.config(fg='black')

def on_title_entry_focus_out(event, title, entry):     # Title is the string to be set in placeholder
    if entry.get() == '':
        entry.insert(0, title)
        entry.config(fg='grey')

# --- Funções de placeholder para o Text ---
def on_description_text_click(event, text_widget='enable'):
    if text_widget['state'] == 'disabled':         # Usefull if a checkbox to disable the field is set on  
        return  
    if text_widget.get("1.0", tkinter.END).strip() == 'Book brief description...':
        text_widget.delete("1.0", tkinter.END)
        text_widget.config(fg='black')

def on_description_text_focus_out(event, text_widget):
    if text_widget.get("1.0", tkinter.END).strip() == '':
        text_widget.insert("1.0", 'Book brief description...')
        text_widget.config(fg='grey')

# --- Funções de UNDO/REDO do Entry ---
def entry_undo(event, entry, undo_stack, redo_stack):
    if undo_stack:
        last_text = undo_stack.pop()
        redo_stack.append(entry.get())
        entry.delete(0, tkinter.END)
        entry.insert(0, last_text)

def entry_redo(event, entry, undo_stack, redo_stack):
    if redo_stack:
        next_text = redo_stack.pop()
        undo_stack.append(entry.get())
        entry.delete(0, tkinter.END)
        entry.insert(0, next_text)

def on_entry_key(event, entry, undo_stack, redo_stack):
    if event.keysym not in ["Control_L", "Control_R", "z", "y"]:
        undo_stack.append(entry.get())
        redo_stack.clear()
