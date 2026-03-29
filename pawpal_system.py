from dataclasses import dataclass

class Owner:
    def __init__(self, name, available_time):
        self.name = name
        self.available_time = available_time

    def update_info(self):
        pass

    def set_available_time(self, time):
        self.available_time = time

@dataclass
class Pet:
    name: str
    pet_type: str

    def update_pet_info(self):
        pass

@dataclass
class Task:
    name: str
    duration: int
    priority: int

    def update_task(self):
        pass

    def display_task(self):
        pass

class Scheduler:
    def __init__(self, list_of_tasks=None, available_time=0):
        if list_of_tasks is None:
            list_of_tasks = []
        self.list_of_tasks = list_of_tasks
        self.available_time = available_time

    def add_task(self, task):
        pass

    def remove_task(self, task):
        pass

    def generate_plan(self):
        pass

    def sort_tasks_by_priority(self):
        pass
