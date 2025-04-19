import tkinter as tk
from tkinter import ttk
from llama_cpp import Llama
import os
from chat_tab import ChatTab
from project_tab import ProjectTab
from note_tab import NoteTab
from theme import apply_theme, icon_path

def init_model():
    """Intialize Dolphin Llama LLM. Try to get GPU, otherwise fallback to CPU based model"""
    try:
        print("Trying to connect model to the GPU...")
        return Llama(
            model_path="models\\Dolphin3.0-Llama3.1-8B_Q5_K_M.gguf",
            n_ctx=2048,
            n_threads=os.cpu_count(), # Use number of available cpus
            n_gpu_layers=-1, # Use any GPUs available on the system
            verbose=True
        ) # Create LLama llm using model and GPU
    except Exception as e:
        print("Failed GPU connection. Using CPU")
        return Llama(
            model_path='models\\Dolphin3.0-Llama3.1-8B_Q5_K_M.gguf',
            n_ctx=2048,
            n_threads=os.cpu_count(), # Use number of available cpus
            n_gpu_layers=0,  # CPU-only
            verbose=True
        ) # Create Llama llm using model and CPU


def on_closing():
    """Destroy tkinter root to close app"""
    root.destroy()

#initialize the model
llm = init_model()

# ======== Root GUI SETUP =========
root = tk.Tk() # TK App root
apply_theme(root) # Apply theme to app

root.title("MossyOS") # Title name 
root.geometry("600x450") # Window sizing
icon_path = "assets\LeafIcon.ico"  # .ico for window
root.iconbitmap(icon_path) # change window icon to app icon

# === Create Notebook for Tabs ===
notebook = ttk.Notebook(root) # Create new Notebook to allow for tabs
notebook.pack(expand=1, fill='both', padx=20, pady=20) # Position notebook on root 

# === Tab Classes ================
chat_tab = ChatTab(notebook, llm, on_closing) # Chat tab

project_tab = ProjectTab(notebook, llm, on_closing) # Projects tab

note_tab = NoteTab(notebook, llm, on_closing)

# bind closing to window delete event
root.protocol("WM_DELETE_WINDOW", on_closing)

# run loop for tkinter root
root.mainloop()

# === CLEAN UP =============
print("Cleaning up....")
del llm
print("🌞 Assistant shut down.")


