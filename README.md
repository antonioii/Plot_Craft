# PlotCraft

**PlotCraft** is a Python application developed as part of my Computer Science graduation project at UNIVERSIDADE PAULISTA  (UNIP).  It is a **creative-writing assistant powered by Large Language Models (LLMs)** that helps authors structure and generate long-form fiction (novels, novellas, etc.) with coherence, creativity, and flexibility.

The project is written in **English** in order to maximize the project’s visibility within the international developer community on GitHub. By doing so, contributors, researchers, and developers worldwide can understand, test, and possibly expand the project.

---


## 📦 Installation

Follow these steps to install and run PlotCraft locally.
    
**Note**: You must have an OpenAI API KEY to run the software after the installation. Read the full manual for more information: https://antonioii.github.io/Plot_Craft/

### 1. Clone the repository
```bash
git clone https://github.com/antonioii/Plot_Craft.git
cd PlotCraft
```

### 2. Set up a virtual environment
It is **highly** recommended to use a virtual environment to isolate dependencies.

```bash
python -m venv venv
venv\Scripts\activate      # On Windows
source venv/bin/activate   # On Linux, or macOS / not yet tested
```

### 3. Install dependencies
Within the project files obtained from github (through the cloning process), find the "App" folder and install the requirements:
```bash
pip install -r requirements.txt
```

### 4. Run the program
```bash
python Main.py
```

This will open the **PlotCraft GUI**, where you can start a new project or load an existing one.


---


## ✨ Features

PlotCraft offers a step-by-step workflow that guides writers from initial idea to final draft:

- **Title & Resume Window**  
  Generate or manually define a book title and summary as the foundation of the project.

- **Reference Schema Board**  
  Automatically extract and organize **places/objects**, **characters**, and **main happenings** that will support the narrative.

- **Three-Act Structure**  
  Suggests **Acts I, II, III** to create the backbone of the story.

- **Chapters Generator**  
  Expands the acts into **12 chapters**, each with a title and summary.

- **Story Beats**  
  Creates **12 detailed beats per chapter** to ensure plot consistency.

- **Final Draft Writing**  
  Automatically writes the book chapter by chapter, in coherent blocks, based on the beats.  
  Includes **progress tracking**, **copy-to-clipboard**, and **Save As (.txt, .rtf, .doc)** options.

- **Project Persistence**  
  All progress is stored in a JSON file, making it possible to **load projects at any stage** (title/resume, schema, acts, chapters, beats, or final draft).

- **GUI-based Interface**  
  Built with **Tkinter**, the app provides a user-friendly workflow without requiring technical knowledge.

---

## 📂 Project Structure

The most important folders and files are:

```
APP/
├── API/
│   ├── Internal_APIs/      # Internal handlers to manage LLM calls
│   ├── External_APIs/      # OpenAI API integration
│   └── set_API.py          # Setup and environment configuration
│
├── GUI/
│   ├── initial_window.py   # Entry window (New Project, Load Project, Instructions)
│   ├── title_and_resume_window.py
│   ├── schema_ref_board.py
│   ├── sugest_acts_window.py
│   ├── sugest_chapters_window.py
│   ├── sugests_beats_window.py
│   ├── finishing_writing_window.py
│   └── project_loader.py   # Load saved JSON projects
│
├── Assets/                 # Icons, logos, instructions (HTML/CSS/JS)
├── config/                 # .env file for API keys
├── Main.py                 # Entry point of the application
└── sample_json.json        # Example of a saved project
```

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **Tkinter** for GUI
- **dotenv** for environment variable handling
- **OpenAI API** for LLM-powered text generation

---

## 📖 Motivation

This project was created as part of my **Final Undergraduate Thesis (TCC)** in Computer Science at **UNIP**.  
The main goal was to explore **applied computer science in creative writing**, leveraging **LLMs** to build a tool that assists, rather than replaces, human authors.  

The program emphasizes **workflow coherence**, **project persistence**, and **practical usability**, showing how AI can empower writers to structure and generate large-scale narratives.

---

## 🤝 Contributions

Contributions are welcome!  
Feel free to **fork this repository**, submit issues, and create pull requests to improve features, UI, or documentation.

---

## 📜 License

This project is licensed under the **MIT License**.  
You are free to use, modify, and distribute it, provided proper credit is given.

---

## 🔗 Author

Developed by **Antonio Sérgio Costa Carpinteiro II**  
- [LinkedIn](https://www.linkedin.com/)  
- [GitHub](https://github.com/antonioii)
