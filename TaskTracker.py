import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import json
import os
import uuid
from datetime import datetime

TASKS_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "w") as f:
            json.dump([], f)
    with open(TASKS_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

def new_task(description):
    now = datetime.now().isoformat()
    return {
        "id": str(uuid.uuid4()),
        "description": description,
        "status": "todo",
        "createdAt": now,
        "updatedAt": now
    }

class TaskTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Tracker")
        self.tasks = load_tasks()
        self.filter_status = None

        # Set window minimum size and make responsive
        self.root.minsize(540, 360)
        self.root.geometry("700x500")
        self.root.configure(bg="#24292e")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Main Frame
        self.frame = tk.Frame(root, bg="#f8f9fa")
        self.frame.grid(sticky="nsew")
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        # Title label
        title = tk.Label(self.frame, text="Task Tracker", font=("Segoe UI", 24, "bold"), bg="#24292e", fg="#f6f8fa", pady=16)
        title.grid(row=0, column=0, sticky="ew", columnspan=3)
        self.frame.grid_columnconfigure(0, weight=1)

        # Task List with scrollbar
        tree_frame = tk.Frame(self.frame, bg="#f8f9fa")
        tree_frame.grid(row=1, column=0, sticky="nsew", pady=(8,8), padx=(12,12), columnspan=3)
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
            background="#f6f8fa",
            foreground="#22272e",
            rowheight=28,
            fieldbackground="#f6f8fa",
            font=("Segoe UI", 12)
        )
        style.configure("Treeview.Heading", font=("Segoe UI", 13, "bold"), background="#e1e4e8", foreground="#24292e")
        style.map('Treeview', background=[('selected', '#0366d6')], foreground=[('selected', '#f6f8fa')])

        self.tree = ttk.Treeview(tree_frame, columns=("desc", "status"), show="headings", selectmode="browse")
        self.tree.heading("desc", text="Description")
        self.tree.heading("status", text="Status")
        self.tree.column("desc", anchor="w")
        self.tree.column("status", width=120, anchor="center")

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        # Buttons frame
        btn_frame = tk.Frame(self.frame, bg="#f8f9fa")
        btn_frame.grid(row=2, column=0, columnspan=3, pady=(4,0), sticky="ew")
        btn_frame.grid_columnconfigure((0,1,2,3), weight=1)

        self.add_btn = tk.Button(btn_frame, text="Add Task", width=12, bg="#2ea44f", fg="#fff", font=("Segoe UI", 11, "bold"),
                                 activebackground="#22863a", activeforeground="#fff", bd=0, command=self.add_task)
        self.add_btn.grid(row=0, column=0, padx=3, pady=6, sticky="ew")

        self.update_btn = tk.Button(btn_frame, text="Update Task", width=12, bg="#0366d6", fg="#fff", font=("Segoe UI", 11, "bold"),
                                   activebackground="#005cc5", activeforeground="#fff", bd=0, command=self.update_task)
        self.update_btn.grid(row=0, column=1, padx=3, pady=6, sticky="ew")

        self.del_btn = tk.Button(btn_frame, text="Delete Task", width=12, bg="#d73a49", fg="#fff", font=("Segoe UI", 11, "bold"),
                                activebackground="#b31d28", activeforeground="#fff", bd=0, command=self.delete_task)
        self.del_btn.grid(row=0, column=2, padx=3, pady=6, sticky="ew")

        self.mark_btn = tk.Button(btn_frame, text="Set Status", width=12, bg="#6f42c1", fg="#fff", font=("Segoe UI", 11, "bold"),
                                 activebackground="#5a32a3", activeforeground="#fff", bd=0, command=self.set_status)
        self.mark_btn.grid(row=0, column=3, padx=3, pady=6, sticky="ew")

        # Filter buttons frame
        filter_frame = tk.Frame(self.frame, bg="#f8f9fa")
        filter_frame.grid(row=3, column=0, columnspan=3, pady=(4,12), sticky="ew")
        filter_frame.grid_columnconfigure((0,1,2,3), weight=1)

        self.filter_buttons = []
        filter_specs = [
            ("All", None, "#24292e"),
            ("To Do", "todo", "#e36209"),
            ("In Progress", "in-progress", "#dbab09"),
            ("Done", "done", "#22863a"),
        ]
        for i, (label, val, color) in enumerate(filter_specs):
            b = tk.Button(filter_frame, text=label, bg="#f6f8fa", fg=color, font=("Segoe UI", 11, "bold"),
                          activebackground="#e1e4e8", activeforeground="#0366d6", bd=0,
                          command=lambda v=val: self.filter_tasks(v))
            b.grid(row=0, column=i, padx=6, pady=3, sticky="ew")
            self.filter_buttons.append(b)

        self.refresh_tasks()

        # Responsive resizing
        for i in range(4):
            btn_frame.grid_columnconfigure(i, weight=1)
            filter_frame.grid_columnconfigure(i, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        # Bind resizing events for even column widths
        self.root.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        # Responsive column sizing in treeview
        w = self.tree.winfo_width()
        if w > 200:
            self.tree.column("desc", width=int(w*0.72))
            self.tree.column("status", width=int(w*0.25))

    def refresh_tasks(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for task in self.get_filtered_tasks():
            color = "#22863a" if task["status"]=="done" else "#dbab09" if task["status"]=="in-progress" else "#e36209"
            self.tree.insert(
                "", "end", iid=task["id"],
                values=(task["description"], task["status"].capitalize()),
                tags=(task["status"],)
            )
            self.tree.tag_configure(task["status"], foreground=color)

    def get_filtered_tasks(self):
        if self.filter_status is None:
            return self.tasks
        return [t for t in self.tasks if t["status"] == self.filter_status]

    def add_task(self):
        desc = simpledialog.askstring("Add Task", "Enter task description:", parent=self.root)
        if desc is None or not desc.strip():
            return
        task = new_task(desc.strip())
        self.tasks.append(task)
        save_tasks(self.tasks)
        self.refresh_tasks()

    def update_task(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Select Task", "Select a task to update.")
            return
        task_id = sel[0]
        task = next((t for t in self.tasks if t["id"] == task_id), None)
        if not task:
            messagebox.showerror("Error", "Task not found.")
            return
        new_desc = simpledialog.askstring("Update Task", "Edit task description:", initialvalue=task["description"], parent=self.root)
        if new_desc is None or not new_desc.strip():
            return
        task["description"] = new_desc.strip()
        task["updatedAt"] = datetime.now().isoformat()
        save_tasks(self.tasks)
        self.refresh_tasks()

    def delete_task(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Select Task", "Select a task to delete.")
            return
        task_id = sel[0]
        if messagebox.askyesno("Delete Task", "Are you sure you want to delete this task?"):
            self.tasks = [t for t in self.tasks if t["id"] != task_id]
            save_tasks(self.tasks)
            self.refresh_tasks()

    def set_status(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Select Task", "Select a task to change status.")
            return
        task_id = sel[0]
        task = next((t for t in self.tasks if t["id"] == task_id), None)
        if not task:
            messagebox.showerror("Error", "Task not found.")
            return

        # Modal dialog for status selection
        status_win = tk.Toplevel(self.root)
        status_win.title("Set Status")
        status_win.geometry("280x140")
        status_win.resizable(False, False)
        status_win.transient(self.root)
        status_win.grab_set()

        tk.Label(status_win, text="Select status:", font=("Segoe UI", 12), pady=8).pack(pady=(18, 0))

        status_options = ["todo", "in-progress", "done"]
        status_var = tk.StringVar(value=task["status"])
        status_cb = ttk.Combobox(status_win, textvariable=status_var, values=status_options, state="readonly", font=("Segoe UI", 12))
        status_cb.pack(pady=8)
        status_cb.set(task["status"])

        def on_set():
            status = status_var.get()
            task["status"] = status
            task["updatedAt"] = datetime.now().isoformat()
            save_tasks(self.tasks)
            self.refresh_tasks()
            status_win.destroy()

        tk.Button(status_win, text="Set", width=9, bg="#0366d6", fg="#fff", font=("Segoe UI", 11, "bold"),
                  activebackground="#005cc5", activeforeground="#fff", bd=0, command=on_set).pack(pady=12)

    def filter_tasks(self, status):
        self.filter_status = status
        self.refresh_tasks()

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskTrackerApp(root)
    root.mainloop()