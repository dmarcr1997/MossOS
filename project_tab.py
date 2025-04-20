import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk, simpledialog
from project_tracker import load_projects, save_projects
import threading
import json
from theme import colors, icon_path
from difflib import get_close_matches # used for fuzzy matching for llm commands


class ProjectTab():
    """Project Tab class for project frame of app. Used to track and add projects and tasks."""
    def __init__(self, notebook, llm, on_closing):
        """Constructor for project tab. Caches notebook and llm. Instantiates project frame and projects."""
        self.notebook = notebook
        self.llm = llm
        self.project_frame = tk.Frame(notebook, bg=colors["panel"])
        self.projects = load_projects()
        self.init_project_frame()
        self.notebook.add(self.project_frame, text="🧩 Projects")
        self.on_closing = on_closing
    
    def init_project_frame(self):
        #LEFT SIDE OF SCREEN GRID
        self.project_frame.columnconfigure(0, weight=0)
        self.project_frame.columnconfigure(1, weight=1)
        self.project_frame.rowconfigure(0, weight=1)
        
        self.project_listbox = tk.Listbox(
            self.project_frame, 
            bg=colors["light"],
            fg=colors["text"],
            font=("Segoe UI", 9),
            highlightthickness=0,
            relief="flat"
        ) # Create list box and set styling
        self.project_listbox.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10) #Position listbox to fill left side of screen with 10x10x10x10 padding
        self.project_listbox.bind("<<ListboxSelect>>", self.open_project) # Bind selection on list box to open project
        #RIGHT SIDE OF SCREEN
        self.right_frame = tk.Frame(self.project_frame, bg=colors["panel"]) # Create right frame
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=10) # Set right frame as column 1 of project frame
        self.right_frame.columnconfigure(0, weight=1) # Command display, Input, Send Column
        self.right_frame.columnconfigure(1, weight=1) # Command display, Input, Exit Column
        self.right_frame.rowconfigure(0, weight=3) # Command display
        self.right_frame.rowconfigure(1, weight=0) # Input
        self.right_frame.rowconfigure(2, weight=0) # Buttons

        self.command_display = scrolledtext.ScrolledText(
            self.right_frame, 
            bg=colors["light"],
            fg=colors["text"],
            insertbackground=colors["text"],
            font=("Segoe UI", 9),
            highlightthickness=0,
            relief="flat",
            wrap=tk.WORD, 
            height=20
        ) # Create scrolled text command display
        self.command_display.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=(0,10)) # Add command display
        self.command_entry = ttk.Entry(
            self.right_frame,
            font=("Segoe UI", 9)
        ) # Create entry with styling
        self.command_entry.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0,10)) # add entry under command display
        self.command_entry.bind("<Return>", lambda e: self.process_llm_command()) # Bind Enter key to process_llm_command function
        self.send_button = ttk.Button(self.right_frame, text="Send", command=self.process_llm_command) # Add send button for manually sending llm command
        self.send_button.grid(row=2, column=0, sticky="ew", padx=(0, 5)) # Add to row 2 column 0 
        self.exit_button = ttk.Button(self.right_frame, text="Exit", command=self.close) # Exit button to close app
        self.exit_button.grid(row=2, column=1, sticky="ew", padx=(5, 0)) # Add exit button to row 2 col 1
        self.refresh_project_list() # Refresh proejct list

    def close(self):
        """Close Function wrapper to allow sending close command to exit button"""
        self.on_closing() # Run close sent from main
    
    def refresh_project_list(self):
        """Load Projects in from json"""
        self.project_listbox.delete(0, tk.END) # Clear project list box
        for name, data in self.projects.items(): # For name and data in project list
            status = data.get("status",'in-progress') # Get status or return in progress if status doesn't exist 
            self.project_listbox.insert(tk.END, f"{name} ({status})") # insert projects into listbox 
    
    def process_llm_command(self):
        """Sends input command to llm for execution."""
        user_cmd = self.command_entry.get().strip() # Get user input and strip whitespace
        if not user_cmd: # If no user input return
            return
        self.command_entry.delete(0, tk.END) # Clear command entry
        self.command_display.insert(tk.END, f"You: {user_cmd}\n\n") #Echo user command/prompt to chat window
        self.command_display.see(tk.END) #Move cursor to end of text added to display scroll box
        prompt = f"""
        Interpret the following command and return the JSON response shown below. DO NOT RETURN ANYTHING ELSE JUST THE RESPONSE OBJECT IN JSON FORMAT
        COMMAND: "{user_cmd}"
        RESPONSE FORMAT:""" + """{ 
            action: <add_project | add_task | toggle_task>,
            project: <project name>,
            task: <task description>
        }
        """ + """NO EXTRA TEXT JUST THE JSON!!""" # Prompt to send to llm to try and parse command from user input

        def query_llm():
            """Thread function to query llm on separate thread from program"""
            try:
                response = self.llm(
                    f"{prompt}",
                    max_tokens=200,
                    stop=["User:"],
                    echo=False
                ) # Query LLM with prompt
                response_text = response["choices"][0]["text"].strip() # Extract llm response
                
                self.execute_llm_instruction(response_text) # Execute command 
            except Exception as e: # Catch errors
                messagebox.showerror("LLM Error", str(e)) # Show errors in messagebox
        threading.Thread(target=query_llm, daemon=True).start() # Spawn thread to run query_llm as daemon so that it can be killed if app crashes or is shutdown
    
    def execute_llm_instruction(self, text):
        """Try to execute llm command to create new project, new task, and mark task as done"""
        if not text: 
            self.command_display(f"LLM: Cannot parse-{text}")
            self.command_display.see(tk.END)
        data = json.loads(text) # Turn llm text into json
        print("TEST2")
        action = data.get("action") # GET action from json
        project = data.get("project") # GET project from json
        task = data.get("task") # GET task from json

        if action == "add_project" and project: # new project command
            print(f"ADD PROJECT {project}")
            self.add_project(project) 
        elif action == "add_task" and project and task: # New task command
            print(f"ADD TASK {task} | {project}")
            self.add_task(project, task)
        elif action == "toggle_task" and project and task: # Toggle task command
            self.toggle_task(project, task)
        self.refresh_project_list() # Refresh project list
        
    def add_project(self, project):
        """Add project to projects given a project name"""
        if project not in self.projects: #If project doesn't already exist. DOES NOT CHECK CAP
            self.command_display.insert(tk.END, f"LLM: Added Project- {project}\n\n") #Echo user command/prompt to chat window
            self.projects[project] = {"status": "in-progress", "tasks": []} # Add new project to project list
            save_projects(self.projects) # Save project's list to json file
            self.refresh_project_list() # Refresh project list
        else:
            self.command_display.insert(tk.END, f"LLM: Project Already Exists.\n\n") # If project already exists 
        self.command_display.see(tk.END) #Move cursor to end of text added to display scroll box

    def open_project(self, event):
        """Open project. Shows tasks in new tk window"""
        selection = self.project_listbox.curselection() # Get selected project in list
        if not selection: # If no selection return
            return
        project_name = self.project_listbox.get(selection[0]).split(" (")[0] #GET only the projects name from list item
        self.open_task_window(project_name) # Open task window with project

    def add_task(self, project, task):
        """Create new task for project. Takes in project and task name."""
        if project in self.projects: # If project exists
            self.command_display.insert(tk.END, f"LLM: Added Task- {task} to Project- {project}\n\n") #Echo user command/prompt to chat window
            self.command_display.see(tk.END) #Move cursor to end of text added to display scroll box
            self.projects[project]["tasks"].append({"name": task, "done": False}) # Add task to project list
            save_projects(self.projects) # Save projects to json file

    def toggle_task(self, project, task): 
        """Toggle task completed/in progress"""
        if project not in self.projects: # If project doesnt exist return
            return
        tasks = self.projects[project]["tasks"] # get tasks
        task_names =[t["name"] for t in tasks] # Get names of tasks
        matches = get_close_matches(task, task_names, n=1, cutoff=0.6) # Look for similar task names
        if matches: # if there is a name
            matched_task = matches[0] # get first match
            index = task_names.index(matched_task) # Get index of match
            tasks[index]["done"] = not tasks[index]["done"] # Set to opposite boolean value
            self.command_display.insert(
                tk.END,
                f"LLM: Toggled Task '{matched_task}' in '{project}'.\n\n"
            ) # Echo command result to command display
            save_projects(self.projects) # Save projects with task changes
        else:
            self.command_display.insert("LLM: Task Not Found\nLLM: No close match found for task: {task}\n\n") # Echo task not found to user
        self.command_display.see(tk.END) # Move command_display to end

    def open_task_window(self, project_name): #TODO: Move to TaskWindow Class
        """Opens window for project's tasks, given a project name string"""
        #======== WINDOW ========
        win = tk.Toplevel(self.project_frame) # Create new tk window with project_frame as parent
        win.title(f"📋 {project_name}") # Set window title
        win.geometry("400x400") # Set windwo size
        win.configure(bg=colors["background"]) # Set background color
        win.iconbitmap(icon_path)
        selected_task_name = tk.StringVar() # global var for new window

        task_listbox = tk.Listbox(
            win, 
            bg=colors["light"],
            fg=colors["text"],
            font=("Segoe UI", 9, "italic"),
            relief="flat",
            highlightthickness=0,
            selectbackground=colors["primary"],
            selectforeground=colors["text"]
        ) # listbox for tasks to allow for selection
        task_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10) # Add tasks box to fill window

        def select_task(event):
            """Task selection event to get task name from selection"""
            selection = task_listbox.curselection() # Get current selection
            if not selection: # if no selection return
                return
            task_line = task_listbox.get(selection[0]) # get line in task_list based on selection result
            
            name = task_line.strip()[4:].strip() # strip other characters besides task name(e.g done/not done [])
            selected_task_name.set(name) # Set selected_task_name
            
        task_listbox.bind("<<ListboxSelect>>", select_task) #bind listbox select to select_task method

        def refresh_tasks():
            """Refresh tasks in window"""
            task_listbox.delete(0, tk.END) # Clear window
            for task in self.projects[project_name]["tasks"]: # iterate through tasks
                check = "✅" if task["done"] else " " # set status of task
                task_listbox.insert(tk.END, f"[{check}] {task['name']}") # insert into end of task_listbox

        def manual_toggle_task():
            """toggle task wrapper to handle passing values into toggle_task method"""
            self.toggle_task(project_name, selected_task_name.get())
            refresh_tasks()

        def manual_add_task():
            """add task wrapper to handle getting new task name and using add_task method"""
            task_name = simpledialog.askstring("New Task", "Enter Name:")
            if task_name:
                self.add_task(project_name, task_name)
                refresh_tasks()

        # === TASK BUTTONS ===
        btns = tk.Frame(win, bg=colors["background"]) # Button frame
        btns.pack(pady=10) # add padding on y

        style = {"font": ("Segoe UI", 9), "padx": 10, "pady": 6} # Button styling

        tk.Button(
            btns,
            text="➕ Add Task",
            command=manual_add_task,
            bg=colors["primary"],
            fg=colors["text"],
            activebackground=colors["accent"],
            bd=0,
            **style
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btns,
            text="✅ Toggle Done",
            command=manual_toggle_task,
            bg=colors["primary"],
            fg=colors["text"],
            activebackground=colors["accent"],
            bd=0,
            **style
        ).pack(side=tk.LEFT, padx=5)

        refresh_tasks()