import json
import os
PROJECT_FILE="projects.json"

def load_projects():
    """Load Projects from projects.json file in root directory of app."""
    if not os.path.exists(PROJECT_FILE): # if project file doesn't exist return an empty json object
        return {}
    with open(PROJECT_FILE, 'r') as f: # open project file with read access
        return json.load(f) # return json data of projects

def save_projects(projects):
    """Save projects to projects.json in root directory of app."""
    with open(PROJECT_FILE, 'w') as f: # Open project file as write or create new file
        json.dump(projects, f, indent=2) # save projects data to projects.json file

def add_project(projects, name):
    
    if name in projects:
        return False

    projects[name] = {"status": "in-progress", "tasks": []}
    return True

def add_task(projects, project_name, task_name):
    if project_name not in projects:
        return False
    projects[project_name]["tasks"].append({"name": task_name, "done": False})
    return True

def toggle_task(projects, project_name, task_index):
    if project_name not in projects:
        return False
    tasks = projects[project_name]["tasks"]
    if task_index < 0 or task_index >= len(tasks):
        return False
    tasks[task_index]["done"] = not tasks[task_index]["done"]
    return True