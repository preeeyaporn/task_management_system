# oop_tasks.py
from abc import ABC, abstractmethod

class TaskStorage(ABC):
   @abstractmethod
   def load_tasks(self):
       pass
   @abstractmethod
   def save_tasks(self, tasks):
       pass

class FileTaskStorage(TaskStorage):
   def __init__(self, filename="tasks.txt"):
       self.filename = filename

   def load_tasks(self):
       loaded_tasks = []
       try:
           with open(self.filename, "r") as f:
               for line in f:
                   parts = line.strip().split(',')
                   if len(parts) == 4:
                       task_id = int(parts[0])
                       description = parts[1]
                       due_date = parts[2] if parts[2] != 'None' else None
                       completed = parts[3] == 'True'
                       loaded_tasks.append(Task(task_id, description, due_date, completed))
       except FileNotFoundError:
           print(f"No existing task file '{self.filename}' found. Starting fresh.")
       return loaded_tasks

   def save_tasks(self, tasks):
       with open(self.filename, "w") as f:
           for task in tasks:
               f.write(f"{task.id},{task.description},{task.due_date},{task.completed}\n")
       print(f"Tasks saved to {self.filename}")


class Task:
    def __init__(self, task_id, description, due_date=None, completed=False, priority="medium"):
        self.id = task_id
        self.description = description
        self.due_date = due_date
        self.completed = completed
        self.priority = priority  # เพิ่ม attribute priority

    def mark_completed(self):
        self.completed = True
        print(f"Task {self.id} '{self.description}' marked as completed.")

    def __str__(self):
        status = "✓" if self.completed else " "
        due = f" (Due: {self.due_date})" if self.due_date else ""
        return f"[{status}] {self.id}. {self.description}{due} [Priority: {self.priority}]"


# oop_tasks.py (ต่อจาก Class Task)

class TaskManager:
    def __init__(self, storage: TaskStorage): # รับ storage object เข้ามา
       self.storage = storage
       self.tasks = self.storage.load_tasks()
       self.next_id = max([t.id for t in self.tasks] + [0]) + 1 if self.tasks else 1
       print(f"Loaded {len(self.tasks)} tasks. Next ID: {self.next_id}")

    def add_task(self, description, due_date=None, priority="medium"):
        task = Task(self.next_id, description, due_date, priority=priority)  # ส่งค่า priority เข้า Task
        self.tasks.append(task)
        self.next_id += 1
        self.storage.save_tasks(self.tasks)  # Save หลังเพิ่ม
        print(f"Task '{description}' added with priority '{priority}'.")
        return task


    def list_tasks(self):
       print("\n--- Current Tasks ---")
       if not self.tasks:
           print("No tasks available.")
           return
       for task in self.tasks:
           print(task)
       print("---------------------")

    def get_task_by_id(self, task_id):
       for task in self.tasks:
           if task.id == task_id:
               return task
       return None

    def mark_task_completed(self, task_id):
       task = self.get_task_by_id(task_id)
       if task:
           task.mark_completed()
           self.storage.save_tasks(self.tasks) # Save after marking
           return True
       print(f"Task {task_id} not found.")
       return False


# oop_tasks.py (ต่อจาก Class TaskManager)

print("Finished")

if __name__ == "__main__":
    storage = FileTaskStorage("my_tasks.txt")  # สร้าง storage object
    manager = TaskManager(storage)             # ส่งเข้า TaskManager
    manager.add_task("Learn Git", "2024-08-01")
    manager.add_task("Practice OOP", "2024-08-05")
    manager.list_tasks()
    manager.mark_task_completed(1)
    manager.list_tasks()

   # Note: Logic สำหรับ Save/Load ยังไม่ครบถ้วน จะเพิ่มในภายหลังโดยใช้หลักการ Single Responsibility Principle (SRP)