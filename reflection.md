# PawPal+ Project Reflection

## 1. System Design
The three core actions a user should use:
1. Add a pet
2. Add a care task (feeding, walk, medication, etc.)
3. Generate a daily plan

**a. Initial design**

- Briefly describe your initial UML design.
The UML is a class diagram with four classes. Task and Pet are dataclasses (pure data containers with minimal logic), while Owner and Scheduler are regular classes. Owner owns a list of Pets, each Pet owns a list of Tasks, and Scheduler depends on both Owner and Pet to produce a daily plan.

- What classes did you include, and what responsibilities did you assign to each?
1. Task: a data container holding everything about a single care task.
2. Pet: a data container representing the animal, holding basic info about it and owning a list of tasks.
3. Owner: represents the user of the app. Holds their name and how many hours per day they are available.
4. Scheduler: this is the core logic class. Takes an Owner and pet, reads the pet's tasks, sorts them by priority, fits them within the owner's available time, and assigns time slots. It also produces a plan.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

1. Change 1 — Applied dataclasses to Task and Pet.
The original design used regular classes with manual __init__ methods. Switching Task and Pet to @dataclass removed boilerplate while keeping the same attributes and methods. Owner and Scheduler stayed as regular classes since they have more complex initialization logic.

2. Change 2 — Removed daily_time_budget as a Scheduler parameter.
Originally Scheduler accepted daily_time_budget as a separate constructor argument alongside owner. This meant the two could be set independently and get out of sync (e.g. owner has 3 hours available but scheduler is told 8 hours). The fix was to derive it automatically from owner.available_hours * 60 inside __init__, so there's a single source of truth.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider?
The scheduler considers three main constraints: the owner's available time budget (converted to minutes), task priority (high, medium, low), and preferred time of day. It decides what matters most by sorting tasks by priority first, then using preferred_time as a tiebreaker. This means a high-priority task always gets scheduled before a medium one, even if the medium task has an earlier preferred time. The time budget is a hard cap — once it's full, remaining tasks are skipped and listed in the reasoning output.

- How did you decide which constraints mattered most?
Priority made the most sense as the primary constraint because a pet owner should never have to choose between a medication and an optional grooming session — the meds should always win. Preferred time matters for quality of life (an evening walk should feel like an evening walk), but since the current scheduler packs tasks sequentially it becomes a secondary hint rather than a guarantee.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

**Tradeoff: sequential packing ignores `preferred_time` during slot assignment**

`assign_time_slots()` sorts tasks by priority and `preferred_time`, but when it assigns actual clock times it chains tasks back-to-back from `start_time` without snapping forward to each task's `preferred_time`. A task marked `preferred_time="17:00"` (evening walk) ends up scheduled at `08:45` if it falls third in the priority queue, even though the owner intended it for late afternoon.

The alternative — snapping `current` forward to `preferred_time` whenever the clock hasn't reached it yet — would honor user intent more faithfully. The tradeoff is that snapping forward leaves dead time in the schedule (e.g. nothing from `09:15` to `17:00`), which can push low-priority tasks past the `daily_time_budget` limit and cause them to be dropped entirely.

For a first version of PawPal+, packing tasks tightly is a reasonable default: it guarantees that every task that fits in the budget actually gets scheduled, and it keeps the algorithm simple enough to reason about. A more advanced scheduler could do both — pack high-priority tasks early, then attempt to honor `preferred_time` for medium and low-priority tasks in the remaining slots.

---

## 3. AI Collaboration

**a. How you used AI**

I used Claude as my AI coding assistant throughout every phase of this project. In Phase 1 it helped me think through class responsibilities — whether Scheduler should live inside Owner or be its own class, and why separating them made the design easier to test and extend. During implementation it was most useful for writing methods I had a clear mental picture of but didn't want to translate line-by-line, like `assign_time_slots()` and `get_reasoning()`. In Phase 3 it helped me implement the four new algorithmic methods (sorting, filtering, conflict detection, recurrence) and explained the tradeoffs behind each approach before writing any code.

The most effective type of prompt was asking for a specific strategy *before* asking for code — something like "what's a lightweight way to detect overlapping time intervals that returns a warning instead of crashing?" That forced a design conversation first, which made the resulting code easier to understand and own. Vague prompts like "add scheduling features" produced generic output I didn't want. Specific, constrained prompts produced exactly what I needed.

**b. Judgment and verification**

One moment I pushed back was when the AI initially suggested building `filter_tasks()` as a method on `Scheduler` instead of `Owner`. The reasoning made surface-level sense — the Scheduler already has access to the pet. But putting it on Scheduler would mean filtering only works after a schedule is generated, and it would only ever see one pet's tasks. Since `Owner` already holds all pets and the method's whole point is cross-pet visibility, I redirected the AI to put it on `Owner` instead. I verified this was right by tracing how the method would actually be called in `main.py` — `owner.filter_tasks(pet_name="Biscuit")` reads naturally; `scheduler.filter_tasks(pet_name="Biscuit")` doesn't, because a Scheduler is only aware of one pet by design.

I also modified the conflict detection output. The AI originally returned raw warning strings with a "WARNING: " prefix baked into the message. I had it strip that prefix in the Streamlit UI layer and re-format it as `st.warning()` instead, because mixing formatting concerns into the business logic would have made `detect_conflicts()` harder to reuse outside the UI.

---

## 4. Testing and Verification

**a. What you tested**

The test suite covers the core scheduling behaviors: that `prioritize_tasks()` returns tasks in the correct priority order, that `assign_time_slots()` respects the time budget and stops adding tasks when it runs out, that `is_overdue()` correctly identifies tasks scheduled after their due time, and that `mark_complete()` creates a next-occurrence task with the right due date for both daily and weekly recurrence. These behaviors matter most because they are the ones a pet owner would notice immediately if they broke — a wrong priority order or a missed medication due to a budget miscalculation would be visible in the first plan the app generates.

**b. Confidence**

I'm confident the scheduler works correctly for the scenarios demonstrated in `main.py` and exercised by the test suite. Edge cases I'd want to cover next with more time: what happens when two tasks have identical priority and identical preferred_time (is the sort stable?), what happens when `available_hours` is 0, and what happens when a recurring task's `due_date` is in the past rather than today — does `timedelta` still produce a sensible next date or does it silently create a stale task?

---

## 5. Reflection

**a. What went well**

I'm most satisfied with how the recurrence system turned out. The combination of `RECURRENCE_DAYS`, `mark_complete()` returning a task, and `Pet.complete_task()` auto-appending it keeps each piece small and independently testable. Adding a new recurrence type (monthly, for example) would take one dictionary entry — that's the kind of extensibility that's hard to plan for upfront but feels obvious once you get there. It also came from a design conversation with the AI rather than just asking it to "make tasks repeat," which is why it actually fits the rest of the system instead of bolted on.

**b. What you would improve**

If I had another iteration, I'd implement `preferred_time` snapping in `assign_time_slots()`. The current tight-packing approach guarantees coverage but ignores the owner's actual intent for when a task should happen. I'd also add a date layer to the Scheduler so it can reason about multi-day plans rather than regenerating from scratch each time. Right now the system has the building blocks — `due_date` on tasks, recurrence intervals, a `generate_plan()` method — but they don't connect across days yet.

**c. Key takeaway**

The most important thing I learned is that AI is a powerful implementer but a weak architect — and that gap is entirely your job to fill. Every time I gave the AI a clear design decision (put this method on Owner, not Scheduler; return warnings instead of raising; use a dict lookup instead of two if-blocks), it executed well. Every time I left the design open-ended, I got technically correct code that didn't fit my system cleanly. Being the lead architect doesn't mean writing every line — it means having a clear enough picture of the system that you can evaluate whether a suggestion fits before you accept it. The best AI prompts I wrote weren't "build X" — they were "given that Y is already true about this system, build X in a way that respects that." That constraint is what makes the collaboration produce something coherent rather than just something functional.
