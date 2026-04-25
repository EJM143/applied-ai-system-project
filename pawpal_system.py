from dataclasses import dataclass, field
from datetime import datetime, timedelta

class Owner:
    def __init__(self, name, available_time):
        self.name = name
        self.available_time = available_time  # in minutes
        self.pets = []

    def update_info(self, name=None, available_time=None):
        """Update owner name and/or available time."""
        if name is not None:
            self.name = name
        if available_time is not None:
            self.available_time = available_time

    def set_available_time(self, time):
        """Set the owner's available time in minutes."""
        self.available_time = time

    def add_pet(self, pet):
        """Add a Pet object to the owner's pet list."""
        self.pets.append(pet)

    def remove_pet(self, pet_name):
        """Remove a pet from the owner's list by name."""
        self.pets = [p for p in self.pets if p.name != pet_name]

    def get_all_tasks(self):
        """Return a flat list of all tasks across all owned pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks

@dataclass
class Pet:
    name: str
    pet_type: str
    breed: str = ""
    age: int = 0
    tasks: list = field(default_factory=list)

    def update_pet_info(self, name=None, pet_type=None, breed=None, age=None):
        """Update one or more pet detail fields."""
        if name is not None:
            self.name = name
        if pet_type is not None:
            self.pet_type = pet_type
        if breed is not None:
            self.breed = breed
        if age is not None:
            self.age = age

    def add_task(self, task):
        """Add a Task object to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, task_name):
        """Remove a task from this pet's list by name."""
        self.tasks = [t for t in self.tasks if t.name != task_name]

    def get_tasks(self):
        """Return the list of tasks assigned to this pet."""
        return self.tasks

@dataclass
class Task:
    name: str
    duration: int  # in minutes
    priority: int  # 1 (low) to 3 (high)
    description: str = ""
    frequency: str = "daily"  # e.g. "daily", "weekly", "as needed"
    completed: bool = False
    time: str = ""  # scheduled start time in "HH:MM" format
    date: str = ""  # scheduled date in "YYYY-MM-DD" format

    def mark_complete(self):
        """Mark this task as completed and return the next occurrence if recurring."""
        self.completed = True
        if self.frequency in ("daily", "weekly"):
            return self.reschedule()
        return None

    def mark_incomplete(self):
        """Mark this task as not completed."""
        self.completed = False

    def update_task(self, name=None, duration=None, priority=None, description=None, frequency=None):
        """Update one or more task fields."""
        if name is not None:
            self.name = name
        if duration is not None:
            self.duration = duration
        if priority is not None:
            self.priority = priority
        if description is not None:
            self.description = description
        if frequency is not None:
            self.frequency = frequency

    def reschedule(self):
        """Create a new Task for the next scheduled occurrence."""
        if not self.date or self.frequency not in ("daily", "weekly"):
            return None
        current = datetime.strptime(self.date, "%Y-%m-%d")
        delta = timedelta(days=1) if self.frequency == "daily" else timedelta(weeks=1)
        next_date = (current + delta).strftime("%Y-%m-%d")
        return Task(self.name, self.duration, self.priority,
                    self.description, self.frequency, date=next_date, time=self.time)

    def display_task(self):
        """Print a formatted one-line summary of the task."""
        status = "Done" if self.completed else "Pending"
        print(f"[{status}] {self.name} | {self.duration} min | Priority: {self.priority} | Frequency: {self.frequency}")
        if self.description:
            print(f"       {self.description}")

class Scheduler:
    def __init__(self, owner, list_of_tasks=None):
        self.owner = owner
        self.list_of_tasks = list_of_tasks if list_of_tasks is not None else []
        self.plan = []

    def load_tasks_from_owner(self):
        """Pull all tasks from the owner's pets into the scheduler."""
        self.list_of_tasks = self.owner.get_all_tasks()

    def add_task(self, task):
        """Add a task directly to the scheduler's task list."""
        self.list_of_tasks.append(task)

    def complete_task(self, task_name):
        """Mark a task complete by name and auto-add the next occurrence if recurring."""
        for task in self.list_of_tasks:
            if task.name == task_name:
                next_task = task.mark_complete()
                if next_task:
                    self.add_task(next_task)
                return
        print(f"Task '{task_name}' not found.")

    def remove_task(self, task_name):
        """Remove a task from the scheduler's list by name."""
        self.list_of_tasks = [t for t in self.list_of_tasks if t.name != task_name]

    def sort_tasks_by_priority(self):
        """Return tasks sorted by priority descending (3 = high first)."""
        return sorted(self.list_of_tasks, key=lambda t: t.priority, reverse=True)

    def sort_by_time(self):
        """Return tasks sorted by scheduled start time (HH:MM), tasks with no/invalid time go last."""
        return sorted(
            self.list_of_tasks,
            key=lambda t: t.time if t.time and ":" in t.time else "23:59"
        )

    def filter_by_pet(self, pet_name):
        """Return all tasks belonging to the pet with the given name."""
        for pet in self.owner.pets:
            if pet.name == pet_name:
                return pet.get_tasks()
        return []

    def schedule_next_occurrences(self):
        """Return a list of new Tasks rescheduled for their next occurrence."""
        next_tasks = []
        for task in self.list_of_tasks:
            next_task = task.reschedule()
            if next_task:
                next_tasks.append(next_task)
        return next_tasks

    def generate_plan(self):
        """
            Build a daily plan using high-priority tasks within available time.
        Skips completed tasks.
        """
        self.plan = []
        time_remaining = self.owner.available_time
        sorted_tasks = self.sort_tasks_by_priority()

        for task in sorted_tasks:
            if task.completed:
                continue
            if task.duration <= time_remaining:
                self.plan.append(task)
                time_remaining -= task.duration

        return self.plan

    def display_plan(self):
        """Print the full daily plan with totals and skipped tasks."""
        if not self.plan:
            print("No plan generated yet. Call generate_plan() first.")
            return

        print(f"\nDaily Plan for {self.owner.name} ({self.owner.available_time} min available)")
        print("-" * 50)
        total = 0
        for i, task in enumerate(self.plan, 1):
            print(f"{i}. ", end="")
            task.display_task()
            total += task.duration
        print("-" * 50)
        print(f"Total time: {total} min | Time remaining: {self.owner.available_time - total} min")

        skipped = [t for t in self.list_of_tasks if t not in self.plan and not t.completed]
        if skipped:
            print(f"\nSkipped ({len(skipped)} tasks didn't fit):")
            for task in skipped:
                print(f"  - {task.name} ({task.duration} min)")
