from pawpal_system import Task
from agent.scheduler_agent import SchedulerAgent
from agent.rag.rag_retriever import retrieve_rules


# ── RAG Tests ─────────────────────────────────────────────────────

def test_rag_feeding():
    rules = retrieve_rules("I need to feed my dog")
    assert any("feed" in r.lower() for r in rules)


def test_rag_walking():
    rules = retrieve_rules("walk my dog")
    assert any("walk" in r.lower() for r in rules)


# ── Scheduler Agent Tests ─────────────────────────────────────────────────────

def test_agent_detects_conflicts():
    t1 = Task("Walk", 30, 2, time="09:00")
    t2 = Task("Feed", 10, 3, time="09:00")

    agent = SchedulerAgent()
    conflicts = agent.detect_conflicts([t1, t2])

    assert len(conflicts) == 1


def test_agent_fixes_conflicts():
    t1 = Task("Walk", 30, 2, time="09:00")
    t2 = Task("Feed", 10, 3, time="09:00")

    agent = SchedulerAgent()
    fixed = agent.fix_conflicts([t1, t2])

    times = sorted([t.time for t in fixed])
    assert times == ["09:00", "10:00"]


def test_agent_explanations():
    t1 = Task("Walk", 30, 2, time="09:00")
    t2 = Task("Feed", 10, 3, time="09:00")

    agent = SchedulerAgent()

    fixed = agent.fix_conflicts([t1, t2])
    explanations = agent.explain_conflicts([t1, t2], fixed)

    assert len(explanations) > 0
    assert any("conflict" in exp.lower() or "fix" in exp.lower() for exp in explanations)


def test_agent_fixes_clean_schedule():
    t1 = Task("Walk", 30, 2, time="09:00")
    t2 = Task("Feed", 10, 3, time="10:00")

    agent = SchedulerAgent()
    fixed = agent.fix_conflicts([t1, t2])

    original_times = sorted([t.time for t in [t1, t2]])
    fixed_times = sorted([t.time for t in fixed])

    assert fixed_times == original_times


def test_agent_fixes_multiple_conflicts():
    t1 = Task("Walk Dog", 30, 2, time="09:00")
    t2 = Task("Feed Cat", 10, 3, time="09:00")
    t3 = Task("Bath Other", 20, 1, time="09:00")

    agent = SchedulerAgent()

    original_conflicts = agent.detect_conflicts([t1, t2, t3])
    fixed = agent.fix_conflicts([t1, t2, t3])
    fixed_conflicts = agent.detect_conflicts(fixed)

    assert len(fixed_conflicts) < len(original_conflicts)
    assert len(fixed) == 3


def test_agent_fixes_multiple_pets_tasks():
    t1 = Task("Walk Mochi", 30, 2, time="09:00")
    t2 = Task("Feed Luna", 10, 3, time="09:00")
    t3 = Task("Play Max", 20, 1, time="10:00")
    t4 = Task("Groom Mochi", 15, 2, time="10:00")

    agent = SchedulerAgent()

    original_conflicts = agent.detect_conflicts([t1, t2, t3, t4])
    fixed = agent.fix_conflicts([t1, t2, t3, t4])
    fixed_conflicts = agent.detect_conflicts(fixed)

    assert len(fixed_conflicts) < len(original_conflicts)
    assert len(fixed) == 4


# ── Full Pipeline Test ─────────────────────────────────────────────

def test_agent_run_pipeline():
    t1 = Task("Walk", 30, 2, time="09:00")
    t2 = Task("Feed", 10, 3, time="09:00")

    agent = SchedulerAgent()

    result = agent.run(
        "I need to walk and feed my dog",
        [t1, t2]
    )

    assert "input" in result
    assert "rules_used" in result
    assert "fixed_schedule" in result
    assert "explanations" in result


# ── Edge Case Tests ─────────────────────────────────────────────────────

def test_invalid_time_format_handling():
    t1 = Task("Walk", 30, 2, time="99:99")
    t2 = Task("Feed", 10, 3, time="abc")

    agent = SchedulerAgent()
    fixed = agent.fix_conflicts([t1, t2])

    assert len(fixed) == 2


def test_missing_feeding_detected():
    from evaluator.evaluator import Evaluator

    schedule = [
        Task("Walk", 30, 2, time="09:00"),
        Task("Play", 20, 1, time="10:00")
    ]

    evaluator = Evaluator()
    result = evaluator.evaluate(schedule, [], 0)

    assert "missing_feeding" in result["issues"]