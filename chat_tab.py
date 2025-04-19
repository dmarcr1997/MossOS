import tkinter as tk
import tkinter.ttk as ttk
from tkinter import scrolledtext
import threading
import time
from theme import colors

class ChatTab():
    """ChatTab class for llm chat window for tkinter Notebook frame"""
    def __init__(self, notebook, llm, on_closing):
        """Chat Tab constructor. Save Notebook, llm, and chat_frame to class attributes"""
        self.notebook = notebook
        self.llm = llm
        self.chat_frame = tk.Frame(notebook,  bg=colors["panel"])
        self.init_chat_frame()
        self.notebook.add(self.chat_frame, text="🌞 Assistant")
        self.on_closing = on_closing

    def init_chat_frame(self):
        """Initialize chat_frame, display, entry input, and send button."""
        self.chat_frame.grid_columnconfigure(0, weight=1) #INPUT Location
        self.chat_frame.grid_columnconfigure(1, weight=0) #SEND Location
        self.chat_frame.grid_columnconfigure(2, weight=0) #EXIT Location
        self.chat_frame.grid_rowconfigure(0, weight=1) #Chat display row
        self.chat_frame.grid_rowconfigure(1, weight=0) #Input and buttons row

        self.chat_display = scrolledtext.ScrolledText(
            self.chat_frame, 
            bg=colors["light"],
            fg=colors["text"],
            insertbackground=colors["text"],
            font=("Segoe UI", 9),
            highlightthickness=0,
            relief="flat",
            wrap=tk.WORD, 
            height=20
        ) # Create scrolled text text area for chat with LLM
        self.chat_display.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="nsew") # add to display grid at row 0 col 0 spanning across columns

        self.entry = ttk.Entry(
            self.chat_frame, 
            font=("Segoe UI", 9)
        ) # Create entry input box 
        self.entry.grid(row=1, column=0, padx=(10, 5), pady=10, sticky="ew") # add entry to display grid at row 1 col 0
        self.send_button = ttk.Button(self.chat_frame, text="Send", command=self.send_message) # Create send input to llm button and bind it to send_message method
        self.send_button.grid(row=1, column=1, padx=5, pady=10, sticky="ew") # add to display grid row 1 column 1
        self.entry.bind('<Return>', lambda e: self.send_message())
        self.exit_button = ttk.Button(self.chat_frame, text="Exit", command=self.close)
        self.exit_button.grid(row=1, column=2, padx=(5, 10), pady=5, sticky="ew")

            
    def close(self):
        """Closing wrapper"""
        self.on_closing()

    def send_message(self):
        """Send message to LLM, start loading, and append message to chat window. Uses 2+Threads of execution"""
        user_message = self.entry.get() # Get user input to entry box
        if not user_message.strip(): # Check for empty input
            return # Return if input is empty
        self.entry.delete(0, tk.END) # Clear entry box
        self.chat_display.insert(tk.END, f"You: {user_message}\n\n") #Echo user command/prompt to chat window
        self.chat_display.see(tk.END) #Move cursor to end of text added to display scroll box

        def run_llm(): 
            """Thread based method to run llm based on user prompt"""
            response_text = "" # response variable
            stop_loader = threading.Event() #Setup threading event for loading 
            loader_tag = "loader" #tag for loader element
            self.chat_display.insert(tk.END, "LLM: ") #insert beginning of llm response while waiting
            loader_pos = self.chat_display.index(tk.END) # set loader position 
            dots = [".", " ", ".", " "] # loader dots
            def animate_loader():
                """Animation of loader while waiting for llm response"""
                dot_indx = 0 # loader index
                while not stop_loader.is_set(): # while stop_loader event is undefined
                    load_indx = dot_indx % 4 # clamp load_indx between 0-3
                    self.chat_display.insert(loader_pos, dots[load_indx]) # Insert loading dot to chat scrollwindow
                    time.sleep(0.5) # Delay
                    dot_indx += 1 # increment dot index
            loader_thread = threading.Thread(target=animate_loader, daemon=True) # Spawn thread to run animate_loader as daemon so that it can be killed if app crashes or is shutdown
            loader_thread.start() # Start animation_loader thread

            try:
                response = self.llm(
                    f"User: {user_message}\nAssistant: ",
                    max_tokens=1024,
                    stop=["User:"],
                    echo=False    
                ) # Send user_message to llm

                response_text = response["choices"][0]["text"] # extract llm resposne from response object
            except Exception as e:
                response_text = f"[Error] {e}" # Log any errors while querying llm

            stop_loader.set() # set stop_loader to stop loader thread
            time.sleep(0.1) # small sleep time for buffer

            self.chat_display.insert(tk.END, '\n') # Add new line after loading ....
            if response_text: # If response text is not empty
                for char in response_text: # typewriter effect
                    self.chat_display.insert(tk.END, char) # add one char to the display
                    self.chat_display.see(tk.END) # move to next position
                    time.sleep(0.02) # delay. change for different typewriter timing
                self.chat_display.insert(tk.END, "\n\n") # add new lines after full response is typed ouf
            else: # no response from llm
                self.chat_display.insert(tk.END, "LLM: [No response received]\n\n") # add no response method to display
            self.chat_display.see(tk.END) # move cursor to end of scrollbox
        threading.Thread(target=run_llm, daemon=True).start() # create and start run_llm thread
