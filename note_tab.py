import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import threading
import os
from theme import colors

class NoteTab():
    """Note Tab class for note frame of app. Used to write collaborative notes with LLM"""
    def __init__(self, notebook, llm, on_closing):
        """Constructor for note tab. Caches notebook and llm. Instantiates note frame and textbox."""
        self.notebook = notebook
        self.llm = llm
        self.note_frame = tk.Frame(notebook, bg=colors["panel"])
        self.notes_dir = "notes"
        self.notes_meta_path = os.path.join(self.notes_dir, "saved_notes.json")
        self.current_note_filename = "Untitled"
        os.makedirs(self.notes_dir, exist_ok=True)

        self.init_note_frame()
        self.notebook.add(self.note_frame, text="🤖 Notes")
        self.on_closing = on_closing
    
    def init_note_frame(self):
        """Initializes note frame and frame contents"""
        # Frame layout
        main_area = tk.Frame(self.note_frame, bg=colors["panel"])
        main_area.pack(fill=tk.BOTH, expand=True)

        sidebar = tk.Frame(main_area, bg=colors["panel"])
        sidebar.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        content_frame = tk.Frame(main_area, bg=colors["panel"])
        content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(0, 10), pady=10)

        # Sidebar buttons
        ttk.Button(sidebar, text="Save Note", command=self.save_note).pack(fill=tk.X, padx=2) # create save note button and position it on the sidebar
        ttk.Button(sidebar, text="Load Note", command=self.load_note).pack(fill=tk.X, padx=2) # Create load note button and position it on the sidebar
        ttk.Button(sidebar, text="Rename Note", command=self.rename_note).pack(fill=tk.X, padx=2) # Create rename note button and position on sidebar
        ttk.Button(sidebar, text="Exit", command=self.close).pack(fill=tk.X, padx=2) # Exit button
        self.loader_label = tk.Label(
            sidebar,
            text="Alt + G for LLM Note Processing...",
            font=("Segoe UI", 9, "italic"),
            fg=colors["text"],
            bg=colors["panel"]
        ) # LLM Loader
        self.loader_label.pack(pady=(10, 0)) #LLM Loader
        self.note_text = scrolledtext.ScrolledText(
            content_frame,
            bg=colors["light"],
            fg=colors["text"],
            font=("Segoe UI", 9),
            insertbackground=colors["text"],
            wrap=tk.WORD,
            relief="flat",
            height=20
        ) # Text area for note input
        self.note_text.pack(fill=tk.BOTH, expand=True) # Add to screen
        self.note_frame.bind_all("<Alt-g>", lambda e: self.process_llm_command()) # ALT + G generate binding to run llm and append llm response to end of current note

        self.new_note() # Creates temp note, no saving yet

    def close(self):
        """Close Function wrapper to allow sending close command to exit button"""
        self.on_closing() # Run close sent from main
    
    def new_note(self):
        """Load Projects in from json"""
        self.note_text.delete("1.0", tk.END) # Clear textarea
        self.current_note_name = "Untitled" # Set current note name to Untitled
    
    def process_llm_command(self):
        """Sends current note text content to llm and llm appends response to end of notes"""
        note_content = self.note_text.get("1.0", tk.END).strip()# Get text content from textarea starting at beginning to the end of the text remove unecessary whitespace
        prompt = (
            "You are a helpful assistant embedded in a retro futuristic notes app with the CONSTRAINTS BELOW.\n"
            "Take the NOTES and provide thoughtful continuation and reflection.\n\n"
            "NOTES:\n"
            f"{note_content}\n"
        )
        def query_llm():
            """Thread function to query llm on separate thread from program"""
            self.loader_label.config(text="Thinking... 🌿")
            try:
                response = self.llm(
                    f"{prompt}",
                    max_tokens=100,
                    stop=["User:"],
                    echo=False
                ) # Query LLM with prompt
                response_text = response["choices"][0]["text"].strip() # Extract llm response
                self.note_text.insert(tk.END, f"\n\n{response_text}") # Insert llm response at the end of the text area
                self.note_text.see(tk.END) # Move cursor to end of text area
            except Exception as e: # Catch errors
                messagebox.showerror("LLM Error", str(e)) # Show errors in messagebox
            self.loader_label.config(text="Alt + G for LLM Note Processing...")
        threading.Thread(target=query_llm, daemon=True).start() # Spawn thread to run query_llm as daemon so that it can be killed if app crashes or is shutdown
    
    def save_note(self):
        messagebox.showinfo("Coming Soon...")
        pass # TODO
    def load_note(self):
        messagebox.showinfo("Coming Soon...")
        pass # TODO
    def rename_note(self):
        messagebox.showinfo("Coming Soon...")
        pass # TODO
    def _save_metadata(self, note_name):
        pass # TODO
    def _load_metadata(self):
        pass # TODO