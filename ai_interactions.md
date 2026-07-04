# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF7)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

Add a third algorithmic capability — "find next available slot" — that scans a generated plan for the earliest gap large enough to fit a task of a given duration.

**What did the agent do?**

1. **`pawpal_system.py`** — Added `Scheduler.find_next_slot(duration: int) -> Optional[str]`. The algorithm:
   - Converts all scheduled tasks to integer-minute intervals using a local `to_minutes()` helper (same pattern as `detect_conflicts()`)
   - Sorts tasks by start time to guarantee left-to-right gap scanning
   - Checks three positions in order: before the first task, between every consecutive pair, then after the last task up to 23:59
   - Returns the earliest fitting start time as `"HH:MM"`, or `None` if no gap exists
   - Includes a full docstring explaining all three gap positions and the return contract

2. **`formatting.py`** — Added `format_next_slot(duration, slot, pet_name)`, which returns a cyan `🕐` success line or a red `✗` no-availability line depending on whether a slot was found.

3. **`main.py`** — Added a `FIND NEXT AVAILABLE SLOT` demo section that tests three durations (5 min, 20 min, 900 min) against each pet's plan, showing both the found-slot and no-slot-available output paths.

4. **`app.py`** — Added a `🕐 Find Next Available Slot` UI widget below the schedule table: a number input for duration that calls `scheduler.find_next_slot()` live and displays the result as `st.success` or `st.warning`.

**What did you have to verify or fix manually?**

Two things needed human correction:

1. **Test durations in the initial demo were not illustrative.** The agent first used `[5, 20, 90]` as test durations. Since the plan ends around 09:15 and there are nearly 15 hours left in the day, all three found the same slot (09:15) — the demo never triggered the "no slot found" path. The 90-minute case wasn't meaningfully different from 5 minutes. Corrected to `[5, 20, 900]` so the 900-minute case exceeds what's left in the day and demonstrates the `None` return path.

2. **Mochi's 900-min result needed a sanity check.** The output showed Mochi *could* fit 900 minutes starting at 08:40. This looked wrong at first glance, but it's mathematically correct: Mochi's plan ends at 08:40, and 08:40 to 23:59 is 919 minutes ≥ 900. Biscuit's plan runs longer (ends at 09:15), leaving only 884 minutes — correctly returning `None`. No code change was needed, but the human review confirmed the algorithm was right before accepting it.

---

## Prompt Comparison (SF11)

> Compare two different prompts (or two different models) on the same task.

| | Option A | Option B |
|-|----------|----------|
| **Model / tool used** | | |
| **Prompt** | | |
| **Response summary** | | |
| **What was useful** | | |
| **Problems noticed** | | |
| **Decision** | | |

**Which approach did you use in your final implementation and why?**

<!-- Your conclusion -->
