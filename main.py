from pawpal_system import Owner, Pet, Task, Scheduler

# --- Setup ---
jordan = Owner("Jordan", available_time=90)

mochi = Pet("Mochi", "dog")
luna = Pet("Luna", "cat")

# Tasks out of order by time
mochi.add_task(Task("Evening walk",   20, 2, time="18:00", date="2026-03-29", frequency="daily"))
mochi.add_task(Task("Morning walk",   30, 3, time="07:30", date="2026-03-29", frequency="daily"))
mochi.add_task(Task("Training",       20, 2, time="10:00", date="2026-03-29", frequency="weekly"))

luna.add_task(Task("Playtime",        15, 3, time="09:00", date="2026-03-29", frequency="daily"))
luna.add_task(Task("Vet check notes", 10, 2, time="07:30", date="2026-03-29", frequency="as needed"))  # conflict with Morning walk

jordan.add_pet(mochi)
jordan.add_pet(luna)

scheduler = Scheduler(jordan)
scheduler.load_tasks_from_owner()

# Mark one task complete to test filtering
scheduler.list_of_tasks[2].mark_complete()  # Training is done

# --- Sort by Time ---
print("=" * 50)
print("TASKS SORTED BY TIME")
print("=" * 50)
for task in scheduler.sort_by_time():
    task.display_task()

# --- Filter by Pet ---
print("\n" + "=" * 50)
print("TASKS FOR MOCHI")
print("=" * 50)
for task in scheduler.filter_by_pet("Mochi"):
    task.display_task()

print("\n" + "=" * 50)
print("TASKS FOR LUNA")
print("=" * 50)
for task in scheduler.filter_by_pet("Luna"):
    task.display_task()

# --- Filter by Completion Status ---
print("\n" + "=" * 50)
print("PENDING TASKS ONLY")
print("=" * 50)
pending = [t for t in scheduler.list_of_tasks if not t.completed]
for task in pending:
    task.display_task()

# --- Conflict Detection ---
print("\n" + "=" * 50)
print("CONFLICT DETECTION")
print("=" * 50)
conflicts = scheduler.detect_conflicts()
if not conflicts:
    print("No conflicts found.")

# --- Generate Plan ---
print("\n" + "=" * 50)
print("TODAY'S SCHEDULE")
print("=" * 50)
scheduler.generate_plan()
scheduler.display_plan()

# --- Recurring Tasks ---
print("\n" + "=" * 50)
print("NEXT OCCURRENCES")
print("=" * 50)
for task in scheduler.schedule_next_occurrences():
    print(f"  {task.name} → {task.date}")
