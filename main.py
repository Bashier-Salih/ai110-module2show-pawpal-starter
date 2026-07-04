from pawpal_system import Owner, Pet, Task, Scheduler

# --- Setup ---
owner = Owner(name="Alex", available_hours=3)

biscuit = Pet(name="Biscuit", species="Dog", breed="Golden Retriever", age=4)
mochi = Pet(name="Mochi", species="Cat", breed="Scottish Fold", age=2)

# --- Tasks for Biscuit ---
biscuit.add_task(Task(name="Morning walk",    type="walk",       duration=30, priority="high",   preferred_time="08:00"))
biscuit.add_task(Task(name="Breakfast",       type="feeding",    duration=10, priority="high",   preferred_time="08:30"))
biscuit.add_task(Task(name="Flea medication", type="meds",       duration=5,  priority="medium", preferred_time="09:00", due_time="10:00"))
biscuit.add_task(Task(name="Evening walk",    type="walk",       duration=30, priority="medium", preferred_time="17:00"))

# --- Tasks for Mochi ---
mochi.add_task(Task(name="Breakfast",         type="feeding",    duration=5,  priority="high",   preferred_time="08:00"))
mochi.add_task(Task(name="Grooming",          type="grooming",   duration=15, priority="low",    preferred_time="10:00"))
mochi.add_task(Task(name="Playtime",          type="enrichment", duration=20, priority="medium", preferred_time="11:00"))

# --- Register pets with owner ---
owner.add_pet(biscuit)
owner.add_pet(mochi)

# --- Generate and display schedules ---
print("=" * 45)
print(f"       TODAY'S SCHEDULE FOR {owner.name.upper()}")
print("=" * 45)

for pet in owner.get_pets():
    scheduler = Scheduler(owner=owner, pet=pet)
    scheduler.generate_plan()
    print()
    print(scheduler.display_plan())
    print()
    print(scheduler.get_reasoning())
    print("-" * 45)
