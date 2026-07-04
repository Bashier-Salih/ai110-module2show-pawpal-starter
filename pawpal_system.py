from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime, timedelta


PRIORITY_ORDER = {"high": 1, "medium": 2, "low": 3}


@dataclass
class Task:
    name: str
    type: str
    duration: int        # minutes
    priority: str        # "high", "medium", "low"
    preferred_time: Optional[str] = None   # "HH:MM" or None
    due_time: Optional[str] = None         # "HH:MM" or None
    scheduled_time: Optional[str] = None   # assigned by Scheduler
    completed: bool = False

    def mark_complete(self):
        """Mark this task as completed."""
        self.completed = True

    def is_overdue(self) -> bool:
        """Return True if the task was scheduled after its due time."""
        if not self.due_time or not self.scheduled_time:
            return False
        fmt = "%H:%M"
        return datetime.strptime(self.scheduled_time, fmt) > datetime.strptime(self.due_time, fmt)

    def update(self, **kwargs):
        """Update any task attribute by keyword argument."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


@dataclass
class Pet:
    name: str
    species: str
    breed: str
    age: int
    tasks: list = field(default_factory=list)

    def add_task(self, task: Task):
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, task: Task):
        """Remove a task from this pet's task list."""
        self.tasks.remove(task)

    def get_tasks(self) -> list:
        """Return all tasks for this pet."""
        return self.tasks

    def get_pending_tasks(self) -> list:
        """Return only tasks that have not been completed."""
        return [t for t in self.tasks if not t.completed]


class Owner:
    def __init__(self, name: str, available_hours: int):
        self.name = name
        self.available_hours = available_hours
        self.pets = []

    def add_pet(self, pet: Pet):
        """Register a pet with this owner."""
        self.pets.append(pet)

    def get_pets(self) -> list:
        """Return all pets belonging to this owner."""
        return self.pets

    def get_all_tasks(self) -> list:
        """Retrieve all pending tasks across every pet the owner has."""
        all_tasks = []
        for pet in self.pets:
            for task in pet.get_pending_tasks():
                all_tasks.append((pet, task))
        return all_tasks


class Scheduler:
    def __init__(self, owner: Owner, pet: Pet, start_time: str = "08:00"):
        self.owner = owner
        self.pet = pet
        self.daily_time_budget = owner.available_hours * 60  # convert to minutes
        self.start_time = start_time
        self.generated_plan = []

    def prioritize_tasks(self) -> list:
        """Sort pending tasks by priority then by preferred_time."""
        tasks = self.pet.get_pending_tasks()
        return sorted(tasks, key=lambda t: (
            PRIORITY_ORDER.get(t.priority, 99),
            t.preferred_time or "99:99"
        ))

    def assign_time_slots(self):
        """Walk through prioritized tasks and assign a start time to each that fits the budget."""
        current = datetime.strptime(self.start_time, "%H:%M")
        time_used = 0
        self.generated_plan = []

        for task in self.prioritize_tasks():
            if time_used + task.duration > self.daily_time_budget:
                break
            task.scheduled_time = current.strftime("%H:%M")
            self.generated_plan.append(task)
            current += timedelta(minutes=task.duration)
            time_used += task.duration

    def generate_plan(self) -> list:
        """Build and return the full daily plan for the pet."""
        self.assign_time_slots()
        return self.generated_plan

    def display_plan(self) -> str:
        """Return a formatted string of the scheduled plan."""
        if not self.generated_plan:
            return "No plan generated yet. Call generate_plan() first."
        lines = [f"Daily plan for {self.pet.name} ({self.pet.breed}):"]
        for task in self.generated_plan:
            overdue_flag = " [OVERDUE]" if task.is_overdue() else ""
            lines.append(
                f"  {task.scheduled_time} — {task.name} ({task.duration} min)"
                f" [priority: {task.priority}]{overdue_flag}"
            )
        return "\n".join(lines)

    def get_reasoning(self) -> str:
        """Explain why each task was scheduled in its position."""
        if not self.generated_plan:
            return "No plan generated yet. Call generate_plan() first."
        lines = [f"Reasoning for {self.pet.name}'s plan:"]
        for i, task in enumerate(self.generated_plan, 1):
            lines.append(
                f"  {i}. '{task.name}' scheduled at {task.scheduled_time} "
                f"because it has {task.priority} priority"
                + (f" and preferred time {task.preferred_time}." if task.preferred_time else ".")
            )
        skipped = [t for t in self.pet.get_pending_tasks() if t not in self.generated_plan]
        if skipped:
            skipped_names = ", ".join(t.name for t in skipped)
            lines.append(f"  Skipped (exceeded time budget): {skipped_names}")
        return "\n".join(lines)
