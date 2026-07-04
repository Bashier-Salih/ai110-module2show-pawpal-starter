# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
=============================================
       TODAY'S SCHEDULE FOR ALEX
=============================================

Daily plan for Biscuit (Golden Retriever):
  08:00 — Morning walk (30 min) [priority: high]
  08:30 — Breakfast (10 min) [priority: high]
  08:40 — Flea medication (5 min) [priority: medium]
  08:45 — Evening walk (30 min) [priority: medium]

Reasoning for Biscuit's plan:
  1. 'Morning walk' scheduled at 08:00 because it has high priority and preferred time 08:00.
  2. 'Breakfast' scheduled at 08:30 because it has high priority and preferred time 08:30.
  3. 'Flea medication' scheduled at 08:40 because it has medium priority and preferred time 09:00.
  4. 'Evening walk' scheduled at 08:45 because it has medium priority and preferred time 17:00.
---------------------------------------------

Daily plan for Mochi (Scottish Fold):
  08:00 — Breakfast (5 min) [priority: high]
  08:05 — Playtime (20 min) [priority: medium]
  08:25 — Grooming (15 min) [priority: low]

Reasoning for Mochi's plan:
  1. 'Breakfast' scheduled at 08:00 because it has high priority and preferred time 08:00.
  2. 'Playtime' scheduled at 08:05 because it has medium priority and preferred time 11:00.
  3. 'Grooming' scheduled at 08:25 because it has low priority and preferred time 10:00.
---------------------------------------------
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Sorts by `scheduled_time` using a lambda key; zero-padded `"HH:MM"` strings compare correctly without parsing |
| Priority sorting | `Scheduler.prioritize_tasks()` | Sorts pending tasks by priority level (`high → medium → low`), then by `preferred_time` as a tiebreaker |
| Filtering | `Owner.filter_tasks(completed, pet_name)` | Returns `(Pet, Task)` pairs; both params are optional — omit either to skip that filter. Pet name match is case-insensitive |
| Conflict detection | `Scheduler.detect_conflicts()` | Checks every scheduled pair for interval overlap (`a_start < b_end and b_start < a_end`); returns warning strings, never raises |
| Recurring tasks | `Task.mark_complete()`, `Pet.complete_task()` | `mark_complete()` returns the next `Task` with `due_date` advanced by `timedelta`; `complete_task()` auto-appends it to the pet's task list |

### Sorting

`Scheduler.sort_by_time()` returns a new list of the generated plan's tasks ordered from earliest to latest `scheduled_time`. It uses Python's `sorted()` with a lambda key:

```python
sorted(tasks, key=lambda t: t.scheduled_time)
```

Because `scheduled_time` is always zero-padded `"HH:MM"`, string comparison is equivalent to chronological comparison — no `datetime` parsing needed. The original `generated_plan` is not modified.

### Filtering

`Owner.filter_tasks(completed, pet_name)` scans every task across all pets and returns only the `(Pet, Task)` pairs that match the supplied filters:

```python
owner.filter_tasks(completed=False)              # all pending tasks, all pets
owner.filter_tasks(pet_name="Biscuit")           # all tasks for one pet
owner.filter_tasks(completed=True, pet_name="Mochi")  # Mochi's completed tasks
```

Both parameters default to `None`, which means "no filter". The method searches `pet.tasks` directly (not `get_pending_tasks()`) so `completed=True` correctly surfaces finished tasks.

### Conflict Detection

`Scheduler.detect_conflicts()` compares every pair of scheduled tasks using integer interval arithmetic. Each `"HH:MM"` time is converted to total minutes; two tasks conflict when:

```
a_start < b_end  and  b_start < a_end
```

The method returns a list of human-readable warning strings — one per conflicting pair — and returns an empty list when the plan is clean. It never raises, so callers can safely print results without extra guards.

### Recurring Tasks

Tasks carry a `recurrence` field (`"daily"` or `"weekly"`) and a `due_date`. When `Pet.complete_task(task)` is called:

1. `task.mark_complete()` sets `completed = True` and, for recurring tasks, uses `timedelta` to compute the next due date:
   - `"daily"` → `due_date + timedelta(days=1)`
   - `"weekly"` → `due_date + timedelta(days=7)`
2. A fresh `Task` (identical fields, `completed=False`, `scheduled_time=None`, updated `due_date`) is returned.
3. `complete_task()` appends that new task to the pet's list automatically.

Adding a new recurrence interval requires only one line in the `RECURRENCE_DAYS` dict at the top of `pawpal_system.py`.

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
