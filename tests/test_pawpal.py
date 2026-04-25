from pawpal_system import Task, Pet, Owner, Scheduler
from agent.scheduler_agent import SchedulerAgent


# ── Basic behavior ────────────────────────────────────────────────────────────

def test_task_completion():
    task = Task("Walk", 30, 2)
    task.mark_complete()
    assert task.completed == True


def test_task_addition():
    pet = Pet("Mochi", "dog")
    initial_count = len(pet.tasks)
    pet.add_task(Task("Feed", 10, 3))
    assert len(pet.tasks) == initial_count + 1


def test_mark_incomplete_resets_flag():
    task = Task("Bath", 20, 1)
    task.mark_complete()
    task.mark_incomplete()
    assert task.completed == False


def test_pet_with_no_tasks_returns_empty_list():
    pet = Pet("Luna", "cat")
    assert pet.get_tasks() == []


# ── Sorting ───────────────────────────────────────────────────────────────────

def test_sort_by_time_earliest_first():
    owner = Owner("Alex", 120)
    scheduler = Scheduler(owner)
    scheduler.add_task(Task("Dinner", 15, 1, time="18:00"))
    scheduler.add_task(Task("Morning walk", 30, 2, time="07:30"))
    scheduler.add_task(Task("Midday play", 20, 2, time="12:00"))

    sorted_tasks = scheduler.sort_by_time()
    times = [t.time for t in sorted_tasks if t.time]

    assert times == ["07:30", "12:00", "18:00"]


def test_sort_by_time_tasks_without_time_go_last():
    owner = Owner("Alex", 120)
    scheduler = Scheduler(owner)
    scheduler.add_task(Task("No-time task", 10, 2))
    scheduler.add_task(Task("Morning walk", 30, 2, time="08:00"))

    sorted_tasks = scheduler.sort_by_time()

    # safer check (handles both "" and None cases)
    assert sorted_tasks[-1].time == "" or not sorted_tasks[-1].time
    assert sorted_tasks[0].time == "08:00"


def test_sort_tasks_by_priority_descending():
    owner = Owner("Alex", 120)
    scheduler = Scheduler(owner)
    scheduler.add_task(Task("Low",  10, 1))
    scheduler.add_task(Task("High", 10, 3))
    scheduler.add_task(Task("Mid",  10, 2))

    sorted_tasks = scheduler.sort_tasks_by_priority()
    priorities = [t.priority for t in sorted_tasks]
    assert priorities == [3, 2, 1]


# ── Recurring task logic ──────────────────────────────────────────────────────

def test_daily_task_complete_creates_next_day():
    task = Task("Feed", 10, 3, frequency="daily", date="2025-06-01")
    next_task = task.mark_complete()

    assert next_task is not None
    assert next_task.date == "2025-06-02"
    assert next_task.completed == False


def test_weekly_task_complete_creates_next_week():
    task = Task("Grooming", 45, 2, frequency="weekly", date="2025-06-01")
    next_task = task.mark_complete()

    assert next_task is not None
    assert next_task.date == "2025-06-08"


def test_as_needed_task_complete_returns_no_next():
    task = Task("Vet visit", 60, 3, frequency="as needed", date="2025-06-01")
    next_task = task.mark_complete()
    assert next_task is None


def test_recurring_task_without_date_returns_no_next():
    task = Task("Walk", 30, 2, frequency="daily")
    next_task = task.mark_complete()
    assert next_task is None


def test_complete_task_in_scheduler_adds_next_occurrence():
    owner = Owner("Alex", 120)
    scheduler = Scheduler(owner)
    scheduler.add_task(Task("Feed", 10, 3, frequency="daily", date="2025-06-01"))

    scheduler.complete_task("Feed")

    assert len(scheduler.list_of_tasks) == 2
    next_task = [t for t in scheduler.list_of_tasks if t.name == "Feed" and not t.completed][0]
    assert next_task.date == "2025-06-02"
    assert next_task.completed == False


def test_complete_non_recurring_task_does_not_add_next():
    owner = Owner("Alex", 120)
    scheduler = Scheduler(owner)
    scheduler.add_task(Task("Vet visit", 60, 3, frequency="as needed", date="2025-06-01"))

    scheduler.complete_task("Vet visit")
    assert len(scheduler.list_of_tasks) == 1


# ── Conflict detection (SchedulerAgent) ──────────────────────────────────────

def test_two_tasks_same_time_returns_one_conflict_tuple():
    owner = Owner("Alex", 120)
    scheduler = Scheduler(owner)
    t1 = Task("Feed",  10, 3, time="09:00")
    t2 = Task("Walk",  30, 2, time="09:00")
    scheduler.add_task(t1)
    scheduler.add_task(t2)

    agent = SchedulerAgent()
    conflicts = agent.detect_conflicts(scheduler.list_of_tasks)

    assert len(conflicts) == 1
    task_a, task_b, time_slot = conflicts[0]
    assert {task_a.name, task_b.name} == {"Feed", "Walk"}
    assert time_slot == "09:00"


def test_no_conflicts_when_all_times_differ():
    owner = Owner("Alex", 120)
    scheduler = Scheduler(owner)
    scheduler.add_task(Task("Feed",  10, 3, time="09:00"))
    scheduler.add_task(Task("Walk",  30, 2, time="10:00"))
    scheduler.add_task(Task("Bath",  20, 1, time="11:00"))

    agent = SchedulerAgent()
    assert agent.detect_conflicts(scheduler.list_of_tasks) == []


def test_tasks_without_time_not_flagged_as_conflicts():
    owner = Owner("Alex", 120)
    scheduler = Scheduler(owner)
    scheduler.add_task(Task("Task A", 10, 2))
    scheduler.add_task(Task("Task B", 10, 2))

    agent = SchedulerAgent()
    assert agent.detect_conflicts(scheduler.list_of_tasks) == []


def test_three_tasks_same_time_returns_three_conflict_tuples():
    owner = Owner("Alex", 120)
    scheduler = Scheduler(owner)
    scheduler.add_task(Task("Feed",  10, 3, time="09:00"))
    scheduler.add_task(Task("Walk",  30, 2, time="09:00"))
    scheduler.add_task(Task("Bath",  20, 1, time="09:00"))

    agent = SchedulerAgent()
    conflicts = agent.detect_conflicts(scheduler.list_of_tasks)

    assert len(conflicts) == 3
    for _, _, time_slot in conflicts:
        assert time_slot == "09:00"


# ── Scheduling edge cases ─────────────────────────────────────────────────────

def test_generate_plan_respects_available_time():
    owner = Owner("Alex", 40)
    scheduler = Scheduler(owner)
    scheduler.add_task(Task("Walk",  30, 3))
    scheduler.add_task(Task("Bath",  20, 2))

    plan = scheduler.generate_plan()
    assert len(plan) == 1
    assert plan[0].name == "Walk"


def test_generate_plan_excludes_completed_tasks():
    owner = Owner("Alex", 120)
    scheduler = Scheduler(owner)
    done = Task("Old walk", 30, 3)
    done.mark_complete()
    scheduler.add_task(done)
    scheduler.add_task(Task("Feed", 10, 2))

    plan = scheduler.generate_plan()
    names = [t.name for t in plan]
    assert "Old walk" not in names
    assert "Feed" in names


def test_generate_plan_empty_when_no_tasks():
    owner = Owner("Alex", 120)
    scheduler = Scheduler(owner)
    assert scheduler.generate_plan() == []


def test_generate_plan_empty_when_available_time_is_zero():
    owner = Owner("Alex", 0)
    scheduler = Scheduler(owner)
    scheduler.add_task(Task("Feed", 10, 3))
    assert scheduler.generate_plan() == []


def test_duplicate_tasks_allowed():
    owner = Owner("Alex", 120)
    scheduler = Scheduler(owner)

    t1 = Task("Feed", 10, 3, time="09:00")
    t2 = Task("Feed", 10, 3, time="09:00")

    scheduler.add_task(t1)
    scheduler.add_task(t2)

    assert len(scheduler.list_of_tasks) == 2