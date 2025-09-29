import tkinter, json, math
from tkinter import filedialog, messagebox
from API.Internal_APIs.handler_apis import ask_LLM_for_final_block

def create_final_writing(self, json_saved_file, json_file_path):
    # --- Settings for text areas, labels and buttons ---
    _text_box_width = 107
    _text_box_height = 20
    _text_box_fonts = "Arial 10"
    _btn_pady = (5, 5)
    _btn_padx = 5
    _btn_color = "black"
    _btn_fg = "white"
    _btn_font = "Arial 8 bold"

    # --- Action Function: Copy btn ---
    def copy_text():
        content = self.writing_text_area.get("1.0", "end-1c")
        self.window.clipboard_clear()
        self.window.clipboard_append(content)
        self.window.update() # Update UI interface, some systems demands it to ensure the copy
        tkinter.messagebox.showinfo("Copied!", "Text copied to clipboard!")

    # --- Action Function: Save btn ---
    def save_text_as():
        content = self.writing_text_area.get("1.0", "end-1c")
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[
                ("Text file", "*.txt"),
                ("Rich Text Format", "*.rtf"),
                ("Word Document", "*.doc"),
                ("All files", "*.*")
            ]
        )

        if filepath:
            try:
                # Save as .RTF
                if filepath.endswith(".rtf"):
                    rtf_content = "{\\rtf1\\ansi\n" + content.replace("\n", "\\par\n") + "\n}"
                    with open(filepath, "w", encoding="utf-8") as file:
                        file.write(rtf_content)

                # Save as .DOC (plane text with no formatation)
                elif filepath.endswith(".doc"):
                    with open(filepath, "w", encoding="utf-8") as file:
                        file.write(content)

                # Save as .TXT
                else:
                    with open(filepath, "w", encoding="utf-8") as file:
                        file.write(content)

                messagebox.showinfo("S U C C E S S!", f"Text SAVED successfully to:\n{filepath}")

            except Exception as e:
                messagebox.showerror("E r r o r", f"Could not save file:\n{e}")

    # --- Re-create content area and resize window ---
    # Wipe content area
    self.beats_main_frame.destroy()
    # New area
    self.final_writing_area = tkinter.Frame(self.content_area)    
    self.final_writing_area.pack()  
    
    # --- Final writing area content ---
    # Text area
    self.texts_frame = tkinter.Frame(self.final_writing_area)
    self.texts_frame.pack()
    ## Label
    self.wait_label = tkinter.Label(self.texts_frame,text="Your book is being written below: 0.0% done.", fg="blue", font="Arial 10 italic")
    self.wait_label.pack(pady=(10, 0))
    
    ## Frame to Text + Scrollbar
    text_scroll_frame = tkinter.Frame(self.texts_frame)
    text_scroll_frame.pack()
    ### Scrollbar
    scrollbar = tkinter.Scrollbar(text_scroll_frame)
    scrollbar.pack(side="right", fill="y")
    ### Text area with scrollbar
    self.writing_text_area = tkinter.Text(
        text_scroll_frame,
        width=_text_box_width,
        height=_text_box_height,
        font=_text_box_fonts,
        undo=True,
        maxundo=5,
        yscrollcommand=scrollbar.set
    )
    self.writing_text_area.pack(side="left")
    ### Linking scrollbar to text area
    scrollbar.config(command=self.writing_text_area.yview)

    # Forcing a UI initial update
    self.window.update_idletasks()
    self.window.update()
    
    # Buttons area
    self.btns_frame = tkinter.Frame(self.final_writing_area)
    self.btns_frame.pack()
    ## Copy Btn
    self.copy_btn = tkinter.Button(self.btns_frame, text=" Copy to clipboard ", width=20, bg=_btn_color, fg=_btn_fg, 
                                   font=_btn_font, command=copy_text)
    self.copy_btn.pack(side="left", pady=_btn_pady, padx=_btn_padx)
    ## Save as Btn
    self.saveAs_btn = tkinter.Button(self.btns_frame, text=" Save As ... ", width=20, bg=_btn_color, fg=_btn_fg, 
                                   font=_btn_font, command=save_text_as)
    self.saveAs_btn.pack(side="left", pady=_btn_pady, padx=_btn_padx)

    # --- Call LLM from the given beats---
    # Read the current JSON saved file
    book_title     = json_saved_file.get("book_title", "")
    book_resume    = json_saved_file.get("book_resume", "")
    places_objects = json_saved_file.get("Places_Objects", "")
    characters     = json_saved_file.get("Characters", "")
    happenings     = json_saved_file.get("Happenings", "")
    chapters       = json_saved_file.get("Chapters", []) or []
    ## Extracting chapter titles and resumes
    self.chapters_data = [
        {"title": ch[0], "resume": ch[1], "beats": ch[2] if len(ch) > 2 else []}
        for ch in json_saved_file.get("Chapters", [])
    ]
    ## Creating a new key in the saved JSON file where we'll put the entire generated book text
    final_parts: list[str] = []

    # Counting total of beats (in pairs and parse to percentage %)
    def _count_total_pairs(chapters_list):
        total = 0
        for ch in chapters_list:
            beats = (ch[2] if len(ch) > 2 else []) or []
            total += math.ceil(len(beats) / 2)
        return total
    total_pairs = max(1, _count_total_pairs(chapters))  # avoid division by 0 (div/0)

    # Update the UI with the initial 'waiting label 0% done' and turn off the buttons
    self.wait_label.config(text="Your book is being written below: 0% done.")
    self.window.update_idletasks()
    try:
        self.copy_btn.config(state="disabled")
        self.saveAs_btn.config(state="disabled")
    except Exception:
        pass

    # Multithread importing: thread + queue + after
    import threading
    from queue import Queue, Empty

    self._q = Queue()
    self._stop = False  # Stop flag

    # Helper function: avoid the thread to keep making results after closing the window
    def _on_close():
        self._stop = True
        try:
            self.window.destroy()
        except Exception:
            pass
    ## Calling the helper function above when the 'X' is clicked to close the window
    try:
        self.window.protocol("WM_DELETE_WINDOW", _on_close)
    except Exception:
        pass

    # Helper function: Worker in thread which never touch the UI (UI is running in another thread)
    def _worker_generate_blocks():
        done_pairs = 0
        try:
            chapter_counter = 1 # A counter to iterate over the chapters_data in order to generate chapter headers in the final text
            for chap_idx, ch in enumerate(chapters, start=1): 
                # ch = [title, resume, beats]
                beats = (ch[2] if len(ch) > 2 else []) or []
                chap_title  = ch[0] if len(ch) > 0 else f"Capítulo {chap_idx}"
                chap_resume = ch[1] if len(ch) > 1 else ""

                # Write a header before start the beat of this chapter
                header = (
                    f"======================\n"
                    f"• CAPITULUM LIBRI {chapter_counter} - {chap_title}:\n"
                    f"Resume: [{chap_resume}].\n\n"
                )
                self._q.put(("append_text", header))
                chapter_counter += 1

                # Iterates  in pairs
                for i in range(0, len(beats), 2):
                    if self._stop:
                        '''
                        trigger to close/stop thread
                        '''
                        self._q.put(("stopped", None))
                        return

                    pair = beats[i:i+2]  # Last pair of beats can have one result only (dont be a pair)
                    try:
                        # CALLING THE LLM API TO GENERATE A TEXT CHUNCK
                        block_text = ask_LLM_for_final_block(
                            book_title, book_resume, places_objects, characters, happenings,
                            chap_idx, chap_title, chap_resume, pair
                        )
                    except Exception:
                        block_text = "Error during the iteration in the final writing window.\n"

                    done_pairs += 1
                    pct = int(round(100 * (done_pairs / total_pairs)))

                    # Queue results for the UI to apply with after
                    self._q.put(("append_text", block_text))
                    self._q.put(("progress", pct))

            self._q.put(("done", None))

        except Exception as e:
            self._q.put(("error", f"{e}"))
            self._q.put(("done", None))

    # Remove from thread queue and apply to UI (main thread)
    def _pump_queue():
        try:
            while True:
                kind, payload = self._q.get_nowait()

                if kind == "append_text":
                    # Update text area
                    final_parts.append(payload)
                    self.writing_text_area.insert("end", payload + "\n\n")
                    self.writing_text_area.see("end")

                elif kind == "progress":
                    # Update percentage in waiting label
                    self.wait_label.config(text=f"Your book is being written below: {payload}% done.")

                elif kind == "error":
                    self.writing_text_area.insert("end", f"\n[ERROR] {payload}\n")
                    self.writing_text_area.see("end")

                elif kind == "stopped":
                    '''
                    Stop trigger: dont save or change phase
                    '''
                    self.wait_label.config(text="Generation cancelled.", fg="black", font="Arial 10 italic")
                    try:
                        self.copy_btn.config(state="normal")
                        self.saveAs_btn.config(state="normal")
                    except Exception:
                        pass
                    return

                elif kind == "done":
                    # Update phase and save final project
                    final_text = "\n".join(final_parts).strip()
                    json_saved_file["Final_Story"] = final_text
                    json_saved_file["project_phase"] = "5"

                    if json_file_path:
                        try:
                            with open(json_file_path, 'w', encoding='utf-8') as f:
                                json.dump(json_saved_file, f, indent=4, ensure_ascii=False)
                        except Exception as e:
                            messagebox.showerror("Error", f"Error saving JSON: {e}")

                    # Waiting label final message (100% Done)
                    self.wait_label.config(text="Your book is being written below: 100% done.")
                    self.window.update_idletasks() # Forcing new update
                    self.wait_label.config(text="100% Done! The full story generated by the beats is below.",
                                          fg="black", font="Arial 12 bold")

                    # Turn-On buttons
                    try:
                        self.copy_btn.config(state="normal")
                        self.saveAs_btn.config(state="normal")
                    except Exception:
                        pass
                    return

        except Empty:
            pass

        # 'Schedule' next queue
        if not getattr(self, "_stop", False):
            self.window.after(50, _pump_queue)

    # Initializing thread and queue emptying
    t = threading.Thread(target=_worker_generate_blocks, daemon=True)
    t.start()
    _pump_queue()

# --- Loading saved JSON function ---
def load_final_writing(self, json_saved_file, json_file_path):
    self.window.resizable(1,1)
    self.window.geometry("800x540+300+0")
    _text_box_width = 107
    _text_box_height = 20
    _text_box_fonts = "Arial 10"
    _btn_pady = (5, 5)
    _btn_padx = 5
    _btn_color = "black"
    _btn_fg = "white"
    _btn_font = "Arial 8 bold"

    def copy_text():
        content = self.writing_text_area.get("1.0", "end-1c")
        self.window.clipboard_clear()
        self.window.clipboard_append(content)
        self.window.update()
        tkinter.messagebox.showinfo("Copied!", "Text copied to clipboard!")

    def save_text_as():
        content = self.writing_text_area.get("1.0", "end-1c")
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[
                ("Text file", "*.txt"),
                ("Rich Text Format", "*.rtf"),
                ("Word Document", "*.doc"),
                ("All files", "*.*"),
            ],
        )
        if filepath:
            try:
                if filepath.endswith(".rtf"):
                    rtf_content = "{\\rtf1\\ansi\n" + content.replace("\n", "\\par\n") + "\n}"
                    with open(filepath, "w", encoding="utf-8") as file:
                        file.write(rtf_content)
                elif filepath.endswith(".doc"):
                    with open(filepath, "w", encoding="utf-8") as file:
                        file.write(content)
                else:
                    with open(filepath, "w", encoding="utf-8") as file:
                        file.write(content)
                messagebox.showinfo("S U C C E S S!", f"Text SAVED successfully to:\n{filepath}")
            except Exception as e:
                messagebox.showerror("E r r o r", f"Could not save file:\n{e}")

    if hasattr(self, "beats_main_frame"):
        try:
            self.beats_main_frame.destroy()
        except Exception:
            pass

    self.final_writing_area = tkinter.Frame(self.content_area)
    self.final_writing_area.pack()

    self.texts_frame = tkinter.Frame(self.final_writing_area)
    self.texts_frame.pack()
    self.wait_label = tkinter.Label(
        self.texts_frame,
        text="100% Done! The full story generated by the beats is below.",
        fg="black",
        font="Arial 12 bold",
    )
    self.wait_label.pack(pady=(10, 0))

    text_scroll_frame = tkinter.Frame(self.texts_frame)
    text_scroll_frame.pack()
    scrollbar = tkinter.Scrollbar(text_scroll_frame)
    scrollbar.pack(side="right", fill="y")
    self.writing_text_area = tkinter.Text(
        text_scroll_frame,
        width=_text_box_width,
        height=_text_box_height,
        font=_text_box_fonts,
        undo=True,
        maxundo=5,
        yscrollcommand=scrollbar.set,
    )
    self.writing_text_area.pack(side="left")
    scrollbar.config(command=self.writing_text_area.yview)

    final_text = json_saved_file.get("Final_Story", "").strip()
    if final_text:
        self.writing_text_area.insert("1.0", final_text)
    else:
        self.writing_text_area.insert("1.0", "This project does not contain a stored final story yet.")
    self.window.update_idletasks()

    self.btns_frame = tkinter.Frame(self.final_writing_area)
    self.btns_frame.pack()
    self.copy_btn = tkinter.Button(
        self.btns_frame,
        text=" Copy to clipboard ",
        width=20,
        bg=_btn_color,
        fg=_btn_fg,
        font=_btn_font,
        command=copy_text,
    )
    self.copy_btn.pack(side="left", pady=_btn_pady, padx=_btn_padx)
    self.saveAs_btn = tkinter.Button(
        self.btns_frame,
        text=" Save As ... ",
        width=20,
        bg=_btn_color,
        fg=_btn_fg,
        font=_btn_font,
        command=save_text_as,
    )
    self.saveAs_btn.pack(side="left", pady=_btn_pady, padx=_btn_padx)