from pawpal_system import Owner, Pet, Task, Scheduler
from agent.scheduler_agent import SchedulerAgent

def header(title):
    """Print unified header with icon and separator."""
    print()
    print("═" * 70)
    print(f"📌 {title}")
    print("═" * 70)
    print()

def print_task(task, index=None):
    """Format and print a task with aligned columns, optionally numbered."""
    status = "Done" if task.completed else "Pending"
    prefix = f"{index}. " if index is not None else ""
    print(f"{prefix}[{status:<8}] {task.name:<20} | {task.time:<5} | {task.duration:>3} min | Priority: {task.priority} | {task.frequency:<10}")

# --- Setup ---
edale = Owner("Edale", available_time=90)

mochi = Pet("Mochi", "dog")
luna = Pet("Luna", "cat")

# Tasks out of order by time
mochi.add_task(Task("Evening walk",   20, 2, time="18:00", date="2026-03-29", frequency="daily"))
mochi.add_task(Task("Morning walk",   30, 3, time="07:30", date="2026-03-29", frequency="daily"))
mochi.add_task(Task("Training",       20, 2, time="10:00", date="2026-03-29", frequency="weekly"))

luna.add_task(Task("Playtime",        15, 3, time="09:00", date="2026-03-29", frequency="daily"))
luna.add_task(Task("Vet check notes", 10, 2, time="07:30", date="2026-03-29", frequency="as needed"))  # conflict with Morning walk

edale.add_pet(mochi)
edale.add_pet(luna)

scheduler = Scheduler(edale)
scheduler.load_tasks_from_owner()

# Mark one task complete to test filtering
scheduler.list_of_tasks[2].mark_complete()  # Training is done

# --- Sort by Time ---
header("TASKS SORTED BY TIME")
for task in scheduler.sort_by_time():
    print_task(task)

# --- Filter by Pet ---
header("TASKS FOR MOCHI")
for task in scheduler.filter_by_pet("Mochi"):
    print_task(task)

header("TASKS FOR LUNA")
for task in scheduler.filter_by_pet("Luna"):
    print_task(task)

# --- Filter by Completion Status ---
header("PENDING TASKS ONLY")
pending = [t for t in scheduler.list_of_tasks if not t.completed]
for task in pending:
    print_task(task)

# --- Conflict Detection ---
header("CONFLICT DETECTION")
agent = SchedulerAgent()
conflicts = agent.detect_conflicts(scheduler.list_of_tasks)
if not conflicts:
    print("No conflicts found.")
else:
    for t1, t2, time_slot in conflicts:
        print(f"[WARNING] Conflict at {time_slot}: '{t1.name}' and '{t2.name}'")

# --- Generate Plan ---
header("TODAY'S SCHEDULE")
plan = scheduler.generate_plan()
for i, task in enumerate(plan, 1):
    print_task(task, index=i)

total = sum(t.duration for t in plan)
remaining = scheduler.owner.available_time - total
print(f"\nTotal time: {total} min | Time remaining: {remaining} min")

# --- Recurring Tasks ---
header("NEXT OCCURRENCES")
for task in scheduler.schedule_next_occurrences():
    print(f"• {task.name} → {task.date}")

print()