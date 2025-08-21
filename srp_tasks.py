from abc import ABC, abstractmethod

class Task:
    def __init__(self, id, description, due_date=None, completed=False, priority="medium"):
        self.id = id
        self.description = description
        self.due_date = due_date
        self.completed = completed
        self.priority = priority  # เพิ่ม attribute priority

    def mark_completed(self):
        self.completed = True

    def __str__(self):
        status = "✓" if self.completed else " "
        due = f"(Due: {self.due_date})" if self.due_date else ""
        priority = f"[Priority: {self.priority}]" if self.priority else ""
        return f"[{status}] {self.id}. {self.description} {due} {priority}".strip()

# ...existing code...

class FileTaskStorage(TaskStorage):
    def __init__(self, filename="tasks.txt"):
        self.filename = filename

    def load_tasks(self):
        loaded_tasks = []
        try:
            with open(self.filename, "r") as f:
                for line in f:
                    parts = line.strip().split(',')
                    if len(parts) == 5:
                        task_id = int(parts[0])
                        description = parts[1]
                        due_date = parts[2] if parts[2] != 'None' else None
                        completed = parts[3] == 'True'
                        priority = parts[4] if parts[4] else "medium"
                        loaded_tasks.append(Task(task_id, description, due_date, completed, priority))
                    elif len(parts) == 4:
                        # กรณีไฟล์เก่าไม่มี priority
                        task_id = int(parts[0])
                        description = parts[1]
                        due_date = parts[2] if parts[2] != 'None' else None
                        completed = parts[3] == 'True'
                        loaded_tasks.append(Task(task_id, description, due_date, completed, "medium"))
        except FileNotFoundError:
            print(f"No existing task file '{self.filename}' found. Starting fresh.")
        return loaded_tasks

    def save_tasks(self, tasks):
        with open(self.filename, "w") as f:
            for task in tasks:
                f.write(f"{task.id},{task.description},{task.due_date},{task.completed},{task.priority}\n")
        print(f"Tasks saved to {self.filename}")

# ...existing code...

class TaskManager:
    def __init__(self, storage: TaskStorage):
        self.storage = storage
        self.tasks = self.storage.load_tasks()
        self.next_id = max([t.id for t in self.tasks] + [0]) + 1 if self.tasks else 1
        print(f"Loaded {len(self.tasks)} tasks. Next ID: {self.next_id}")

    def add_task(self, description, due_date=None, priority="medium"):
        task = Task(self.next_id, description, due_date, priority=priority)
        self.tasks.append(task)
        self.next_id += 1
        self.storage.save_tasks(self.tasks)
        print(f"Task '{description}' added.")
        return task

    # ...existing code...

if __name__ == "__main__":
    file_storage = FileTaskStorage("my_tasks.txt")
    manager = TaskManager(file_storage)

    manager.list_tasks()
    manager.add_task("Review SOLID Principles", "2024-08-10", priority="high")
    manager.add_task("Prepare for Final Exam", "2024-08-15", priority="medium")
    manager.list_tasks()
    manager.mark_task_completed(1)
    manager.list_tasks()