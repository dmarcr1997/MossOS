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
    """Add new project to projects list"""
    if name in projects: # If proejct already exists return. TODO: Add partial match
        return False

    projects[name] = {"status": "in-progress", "tasks": []} # New project
    return True

def add_task(projects, project_name, task_name):
    """Add task to project if project exists"""
    if project_name not in projects: # If project doesn't exist return
        return False
    projects[project_name]["tasks"].append({"name": task_name, "done": False}) # Add new task to project
    return True

def toggle_task(projects, project_name, task_index):
    """Toggle task as finished/in progress based on project and task_index"""
    if project_name not in projects: # If project doesn't exist return
        return False
    tasks = projects[project_name]["tasks"] # Find tasks
    if task_index < 0 or task_index >= len(tasks): # Look for tasks at index. return if it doesn't exist
        return False
    tasks[task_index]["done"] = not tasks[task_index]["done"] # toggle task status
    return True