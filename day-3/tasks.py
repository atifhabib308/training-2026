import json
import sys
import os
from datetime import datetime

TASKS_FILE = "tasks.json"

class Task:
    def __init__(self, id, title, status="todo", created_at=None):
        self.id = id
        self.title = title
        self.status = status
        self.created_at = created_at or datetime.utcnow().isoformat()

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "status": self.status,
            "created_at": self.created_at,
        }

    @staticmethod
    def from_dict(data):
        return Task(
            id=data["id"],
            title=data["title"],
            status=data.get("status", "todo"),
            created_at=data.get("created_at"),
        )


class TaskManager:
    def __init__(self, filepath=TASKS_FILE):
        self.filepath = filepath
        self.tasks = []
        self._load_tasks()

    def _load_tasks(self):
        if not os.path.exists(self.filepath):
            self.tasks = []
            return

        try:
            with open(self.filepath, "r") as f:
                data = json.load(f)
                self.tasks = [Task.from_dict(t) for t in data]
        except json.JSONDecodeError:
            print("Error: tasks.json is corrupted. Starting with empty task list.")
            self.tasks = []
        except Exception as e:
            print(f"Unexpected error while loading tasks: {e}")
            self.tasks = []

    def _save_tasks(self):
        try:
            with open(self.filepath, "w") as f:
                json.dump([t.to_dict() for t in self.tasks], f, indent=2)
        except Exception as e:
            print(f"Error saving tasks: {e}")

    def _get_next_id(self):
        if not self.tasks:
            return 1
        return max(t.id for t in self.tasks) + 1

    def add_task(self, title):
        task = Task(id=self._get_next_id(), title=title)
        self.tasks.append(task)
        self._save_tasks()
        print(f"Task added with id {task.id}")

    def complete_task(self, id):
        task = self._find_task(id)
        if not task:
            print(f"Error: Task with id {id} does not exist")
            return
        task.status = "done"
        self._save_tasks()
        print(f"Task {id} marked as done")

    def delete_task(self, id):
        task = self._find_task(id)
        if not task:
            print(f"Error: Task with id {id} does not exist")
            return
        self.tasks.remove(task)
        self._save_tasks()
        print(f"Task {id} deleted")

    def list_tasks(self, filter=None):
        tasks = self.tasks
        if filter:
            if filter not in ["todo", "done"]:
                print("Invalid filter. Use 'todo' or 'done'")
                return
            tasks = [t for t in tasks if t.status == filter]

        if not tasks:
            print("No tasks found")
            return

        for t in tasks:
            print(f"[{t.id}] {t.title} | {t.status} | {t.created_at}")

    def _find_task(self, id):
        for t in self.tasks:
            if t.id == id:
                return t
        return None


# CLI handling

def main():
    manager = TaskManager()

    if len(sys.argv) < 2:
        print("Usage: python tasks.py [add|done|delete|list] ...")
        return

    command = sys.argv[1]

    if command == "add":
        if len(sys.argv) < 3:
            print("Error: Title is required")
            return
        title = " ".join(sys.argv[2:])
        manager.add_task(title)

    elif command == "done":
        if len(sys.argv) < 3:
            print("Error: Task id is required")
            return
        try:
            task_id = int(sys.argv[2])
        except ValueError:
            print("Error: Task id must be an integer")
            return
        manager.complete_task(task_id)

    elif command == "delete":
        if len(sys.argv) < 3:
            print("Error: Task id is required")
            return
        try:
            task_id = int(sys.argv[2])
        except ValueError:
            print("Error: Task id must be an integer")
            return
        manager.delete_task(task_id)

    elif command == "list":
        filter_value = None
        if "--filter" in sys.argv:
            try:
                idx = sys.argv.index("--filter")
                filter_value = sys.argv[idx + 1]
            except IndexError:
                print("Error: --filter requires a value")
                return
        manager.list_tasks(filter_value)

    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
