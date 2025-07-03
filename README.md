# Task-Tracker

A simple, modern, and minimalistic Python GUI application to help you track your tasks and manage your to-do list efficiently. This app is built with only the Python standard library (Tkinter, JSON, etc.)—no external dependencies required!

## Features

- **Add, Update, and Delete tasks**  
  Quickly create, edit, or remove tasks as needed.
- **Change Task Status**  
  Mark tasks as `todo`, `in-progress`, or `done` with a convenient dropdown.
- **Filter Tasks**  
  Instantly filter to show all tasks, only tasks to do, in progress, or completed.
- **Modern & Responsive GUI**  
  Clean, modern design with responsive layout that adapts to window resizing.
- **Persistent Storage**  
  All tasks are stored in a `tasks.json` file in your working directory.

## Task Properties

Each task in the tracker has the following properties:

- `id`: Unique identifier (UUID)
- `description`: Brief description of the task
- `status`: Either `todo`, `in-progress`, or `done`
- `createdAt`: ISO 8601 timestamp of creation
- `updatedAt`: ISO 8601 timestamp of last update

## Getting Started

### Prerequisites

- Python 3.x (no external libraries required)

### Installation

1. **Clone or Download this repository.**
2. Place `TaskTracker.py` in your desired directory.

### Running the App

```sh
python TaskTracker.py
```

- The application window will open.
- A `tasks.json` file will be created in the current directory if it doesn't exist.

## Usage

- **Add Task:** Click "Add Task", enter the description, and save.
- **Update Task:** Select a task, click "Update Task", edit the description, and save.
- **Delete Task:** Select a task and click "Delete Task".
- **Set Status:** Select a task, click "Set Status", and choose a status from the dropdown.
- **Filter:** Use the filter buttons to view all, pending, in-progress, or completed tasks.

## Customization

- Colors and fonts can be adjusted in `TaskTracker.py` for a personalized look.

---

**Enjoy being organized with Task Tracker!**
