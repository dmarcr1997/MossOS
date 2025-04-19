import tkinter as tk
from tkinter import ttk
from llama_cpp import Llama
import os
from chat_tab import ChatTab
from project_tab import ProjectTab
from theme import apply_theme

def init_model():
    try:
        print("Trying to connect model to the GPU...")
        return Llama(
            model_path="models\\Dolphin3.0-Llama3.1-8B_Q5_K_M.gguf",
            n_ctx=2048,
            n_threads=os.cpu_count(),
            n_gpu_layers=-1,
            verbose=True
        )
    except Exception as e:
        print("Failed GPU connection. Using CPU")
        return Llama(
            model_path='models\\Dolphin3.0-Llama3.1-8B_Q5_K_M.gguf',
            n_ctx=2048,
            n_threads=os.cpu_count(),
            n_gpu_layers=0,  # CPU-only
            verbose=True
        )


def on_closing():
    root.destroy()

#initialize the model
llm = init_model()

# ======== Root GUI SETUP =========
root = tk.Tk()
apply_theme(root)

root.title("LLM - Local Assistant")
root.geometry("600x450")
icon_path = "assets\LeafIcon.ico"  # must be .ico on Windows
root.iconbitmap(icon_path)

# === Create Notebook for Tabs ===
notebook = ttk.Notebook(root)
notebook.pack(expand=1, fill='both', padx=20, pady=20)

chat_tab = ChatTab(notebook, llm, on_closing)

project_tab = ProjectTab(notebook, llm, on_closing)

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
print("Cleaning up....")
del llm
print("🌞 Assistant shut down.")


