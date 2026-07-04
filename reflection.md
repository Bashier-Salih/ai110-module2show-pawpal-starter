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
3. Owner: represents the user of the app. Holds their name and how many hours per day they are availble. 
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

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

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

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
