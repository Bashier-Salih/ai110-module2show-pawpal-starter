from pawpal_system import Owner, Pet, Task, Scheduler
from datetime import date

# --- Setup ---
owner = Owner(name="Alex", available_hours=3)

biscuit = Pet(name="Biscuit", species="Dog", breed="Golden Retriever", age=4)
mochi = Pet(name="Mochi", species="Cat", breed="Scottish Fold", age=2)

today = date.today()

# --- Tasks for Biscuit (added out of order intentionally) ---
biscuit.add_task(Task(name="Evening walk",    type="walk",       duration=30, priority="medium", preferred_time="17:00", recurrence="daily",  due_date=today))
biscuit.add_task(Task(name="Flea medication", type="meds",       duration=5,  priority="medium", preferred_time="09:00", due_time="10:00"))
biscuit.add_task(Task(name="Breakfast",       type="feeding",    duration=10, priority="high",   preferred_time="08:30", recurrence="daily",  due_date=today))
biscuit.add_task(Task(name="Morning walk",    type="walk",       duration=30, priority="high",   preferred_time="08:00", recurrence="daily",  due_date=today))

# --- Tasks for Mochi (added out of order intentionally) ---
mochi.add_task(Task(name="Playtime",          type="enrichment", duration=20, priority="medium", preferred_time="11:00", recurrence="weekly", due_date=today))
mochi.add_task(Task(name="Breakfast",         type="feeding",    duration=5,  priority="high",   preferred_time="08:00", recurrence="daily",  due_date=today))
mochi.add_task(Task(name="Grooming",          type="grooming",   duration=15, priority="low",    preferred_time="10:00"))

# --- Register pets with owner ---
owner.add_pet(biscuit)
owner.add_pet(mochi)

# --- Generate schedules ---
print("=" * 45)
print(f"       TODAY'S SCHEDULE FOR {owner.name.upper()}")
print("=" * 45)

schedulers = {}
for pet in owner.get_pets():
    scheduler = Scheduler(owner=owner, pet=pet)
    scheduler.generate_plan()
    schedulers[pet.name] = scheduler
    print()
    print(scheduler.display_plan())
    print()
    print(scheduler.get_reasoning())
    print("-" * 45)

# --- Demo: sort_by_time() ---
print()
print("=" * 45)
print("      SORT BY TIME DEMO")
print("=" * 45)

for pet_name, scheduler in schedulers.items():
    sorted_tasks = scheduler.sort_by_time()
    print(f"\n{pet_name}'s tasks sorted chronologically:")
    for task in sorted_tasks:
        print(f"  {task.scheduled_time} — {task.name} ({task.priority})")

# --- Demo: filter_tasks() ---
print()
print("=" * 45)
print("      FILTER TASKS DEMO")
print("=" * 45)

print("\nAll incomplete tasks (all pets):")
for pet, task in owner.filter_tasks(completed=False):
    print(f"  [{pet.name}] {task.name} — {task.priority}")

print("\nAll completed tasks (all pets):")
for pet, task in owner.filter_tasks(completed=True):
    print(f"  [{pet.name}] {task.name} — {task.priority}")

print("\nAll tasks for Biscuit only:")
for pet, task in owner.filter_tasks(pet_name="Biscuit"):
    status = "done" if task.completed else "pending"
    print(f"  {task.name} [{status}]")

print("\nBiscuit's incomplete tasks only:")
for pet, task in owner.filter_tasks(completed=False, pet_name="Biscuit"):
    print(f"  {task.name}")

# --- Demo: recurrence ---
print()
print("=" * 45)
print("      RECURRENCE DEMO")
print("=" * 45)

morning_walk = biscuit.tasks[3]   # Morning walk (daily)
breakfast     = mochi.tasks[1]    # Mochi Breakfast (daily)
playtime      = mochi.tasks[0]    # Playtime (weekly)

print(f"\nBefore: Biscuit has {len(biscuit.tasks)} task(s)")
next_task = biscuit.complete_task(morning_walk)
print(f"Completed '{morning_walk.name}' — was due {morning_walk.due_date} (recurrence={morning_walk.recurrence})")
print(f"After:  Biscuit has {len(biscuit.tasks)} task(s)")
if next_task:
    print(f"  -> Next occurrence: '{next_task.name}' due {next_task.due_date} (today + 1 day via timedelta)")

print(f"\nBefore: Mochi has {len(mochi.tasks)} task(s)")
next_breakfast = mochi.complete_task(breakfast)
next_playtime  = mochi.complete_task(playtime)
print(f"Completed '{breakfast.name}' — was due {breakfast.due_date} (recurrence={breakfast.recurrence})")
if next_breakfast:
    print(f"  -> Next occurrence: '{next_breakfast.name}' due {next_breakfast.due_date} (today + 1 day via timedelta)")
print(f"Completed '{playtime.name}' — was due {playtime.due_date} (recurrence={playtime.recurrence})")
if next_playtime:
    print(f"  -> Next occurrence: '{next_playtime.name}' due {next_playtime.due_date} (today + 7 days via timedelta)")
print(f"After:  Mochi has {len(mochi.tasks)} task(s)")

print("\nMochi's pending tasks after completions:")
for t in mochi.get_pending_tasks():
    recur_label = f" [{t.recurrence}]" if t.recurrence else ""
    due_label   = f" due {t.due_date}" if t.due_date else ""
    print(f"  {t.name}{recur_label}{due_label}")

# --- Demo: detect_conflicts() ---
print()
print("=" * 45)
print("      CONFLICT DETECTION DEMO")
print("=" * 45)

# Build a fresh pet with two tasks manually forced to overlap
rex = Pet(name="Rex", species="Dog", breed="Labrador", age=3)
rex.add_task(Task(name="Bath time",   type="grooming", duration=30, priority="high",   scheduled_time="09:00"))
rex.add_task(Task(name="Vet checkup", type="medical",  duration=45, priority="high",   scheduled_time="09:15"))
rex.add_task(Task(name="Lunch",       type="feeding",  duration=10, priority="medium", scheduled_time="12:00"))

owner.add_pet(rex)
rex_scheduler = Scheduler(owner=owner, pet=rex)
# Bypass assign_time_slots — tasks already have scheduled_time set manually above
rex_scheduler.generated_plan = rex.tasks[:]

print(f"\nRex's manually scheduled tasks:")
for t in rex_scheduler.generated_plan:
    print(f"  {t.scheduled_time} — {t.name} ({t.duration} min)")

print()
conflicts = rex_scheduler.detect_conflicts()
if conflicts:
    for warning in conflicts:
        print(warning)
else:
    print("No conflicts detected.")

print()
print("No-conflict check (Biscuit's auto-generated plan):")
biscuit_scheduler = Scheduler(owner=owner, pet=biscuit)
biscuit_scheduler.generate_plan()
conflicts = biscuit_scheduler.detect_conflicts()
if conflicts:
    for warning in conflicts:
        print(warning)
else:
    print("  No conflicts detected — Biscuit's plan is clean.")
