# 🌞 MossOS Notes

**MossOS** is a local note-taking assistant powered by local llama based LLMs via `llama.cpp`. It features a retro aesthetic and offline functionality to helps you write, brainstorm, track projects, and reflect using AI with no costs besides your computer's runtime.

---

## ✨ Features

- 🤖 Local LLM Assitant
- 🧩 Project tracking and AI project management
- 🌿 Local LLM-powered note continuation
- 🧠 LLM thread runs in background with loader feedback
- 🔐 Fully offline

---

## 🏗 Directory Structure

```
mossos/
├── notes/                   # .txt files and metadata stored here
│   └── saved_notes.json
├── models/                  # Local GGUF LLM models
├── note_tab.py
├── chat_tab.py
├── project_tab.py 
├── theme.py
├── main.py                   # App entry
├── assets/                   # Icon
├── README.md
├── requirements.txt
```

---

## 🖥️ Requirements

Install with pip:

```
pip install -r requirements.txt
```

### requirements.txt
```
llama-cpp-python>=0.2.20
```

---

## 🚀 How to Run

```bash
python main.py
```

Place your `.gguf` model inside the `models/` directory and make sure `llama-cpp-python` is pointing to it correctly in `main.py`.

---

## ⌨️ Shortcuts

| Shortcut | Action                                       |
|----------|----------------------------------------------|
| `Alt + G`| Ask the LLM to continue the note on note tab |
| `Enter`  | Send Chat to AI on Assistant or Project tabs |


## License
[MIT License](./LICENSE)

## Author
Built by Damon Rocha — inspired by robotics, nature, and AI to solve real-world problems.
