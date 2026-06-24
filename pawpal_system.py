from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Task:
    name: str
    type: str
    duration: int
    priority: str
    preferred_time: Optional[str] = None
    due_time: Optional[str] = None
    scheduled_time: Optional[str] = None
    completed: bool = False

    def mark_complete(self):
        pass

    def is_overdue(self):
        pass

    def update(self, **kwargs):
        pass


@dataclass
class Pet:
    name: str
    species: str
    breed: str
    age: int
    tasks: list = field(default_factory=list)

    def add_task(self, task: Task):
        pass

    def remove_task(self, task: Task):
        pass

    def get_tasks(self):
        pass

    def get_pending_tasks(self):
        pass


class Owner:
    def __init__(self, name: str, available_hours: int):
        self.name = name
        self.available_hours = available_hours
        self.pets = []

    def add_pet(self, pet: Pet):
        pass

    def get_pets(self):
        pass


class Scheduler:
    def __init__(self, owner: Owner, pet: Pet, daily_time_budget: int, start_time: str = "08:00"):
        self.owner = owner
        self.pet = pet
        self.daily_time_budget = daily_time_budget
        self.start_time = start_time
        self.generated_plan = []

    def generate_plan(self):
        pass

    def prioritize_tasks(self):
        pass

    def assign_time_slots(self):
        pass

    def display_plan(self):
        pass

    def get_reasoning(self):
        pass
