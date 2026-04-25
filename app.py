import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler
from agent.scheduler_agent import SchedulerAgent
from evaluator.evaluator import Evaluator

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="wide")

# ─────────────────────────────────────────────
# SIDEBAR NAVIGATION 
# ─────────────────────────────────────────────
st.sidebar.title("🐾 PawPal+")

page = st.sidebar.radio(
    "Navigation",
    ["🏠 Dashboard", "👤 Owner","🐶 Pets", "📋 Tasks", "🧠 AI Scheduler", ]
)

# ─────────────────────────────────────────────
# STATE
# ─────────────────────────────────────────────
if "owner" not in st.session_state:
    st.session_state.owner = Owner("Edale", available_time=60)

if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler(st.session_state.owner)

if "tasks" not in st.session_state:
    st.session_state.tasks = []

# ─────────────────────────────────────────────
# DASHBOARD
# ─────────────────────────────────────────────
if page == "🏠 Dashboard":

    st.markdown(
        "<h1 style='text-align:center;'>🐾 PawPal+</h1>",
        unsafe_allow_html=True
    )

    st.info("AI Pipeline: RAG → Scheduler Agent → Evaluator → Output")

    st.write("")

    with st.container(border=True):
        st.subheader("Owner Information")

        col1, col2, col3 = st.columns(3)
        col1.metric("Owner", st.session_state.owner.name)
        col2.metric("Available Time", f"{st.session_state.owner.available_time} min")
        col3.metric("Pets", len(st.session_state.owner.pets))

# ─────────────────────────────────────────────
# OWNER PAGE
# ─────────────────────────────────────────────
elif page == "👤 Owner":

    st.title("👤 Owner Settings")

    with st.container(border=True):

        new_name = st.text_input(
            "Owner Name",
            placeholder="Update owner name"
        )

        new_time = st.number_input(
            "Available Time (min)",
            min_value=60
        )

        if st.button("Update Owner"):
            if new_name:
                st.session_state.owner.name = new_name

            if new_time:
                st.session_state.owner.available_time = new_time

            st.success("Owner updated")

# ─────────────────────────────────────────────
# PETS PAGE
# ─────────────────────────────────────────────
elif page == "🐶 Pets":

    st.title("🐶 Pets")

    with st.container(border=True):

        pet_name = st.text_input(
            "Pet Name",
            placeholder="Add pet's name",
            key="pet_name"
        )

        species = st.selectbox(
            "Species",
            ["dog", "cat", "other"],
            index=None,
            key="species"
        )

        if st.button("Add Pet"):
            if pet_name and species:
                st.session_state.owner.add_pet(Pet(pet_name, species))
                st.success("Pet added")
                st.rerun()

    st.write("---")

    for i, pet in enumerate(st.session_state.owner.pets):
        col1, col2, col3 = st.columns([3, 2, 1])

        with col1:
            st.write(pet.name)

        with col2:
            st.write(pet.pet_type)

        with col3:
            if st.button("🗑️", key=f"del_pet_{i}"):
                st.session_state.owner.pets.pop(i)
                st.rerun()

# ─────────────────────────────────────────────
# TASKS PAGE
# ─────────────────────────────────────────────
elif page == "📋 Tasks":

    st.title("📋 Tasks")

    with st.container(border=True):

        task_type = st.selectbox(
            "Task Type",
            ["Feed", "Walk", "Groom", "Play", "Vet Visit", "Other"],
            index=None,
            placeholder="Select task type",
            key="task_type"
        )

        if task_type == "Other":
            custom_task = st.text_input("Custom Task Name", key="custom_task")
        else:
            custom_task = task_type

        priority = st.selectbox("Priority", ["low", "medium", "high"], index=None, key="priority")
        time = st.text_input("Time", placeholder="HH:MM", key="time")
        duration = st.number_input("Duration", 1, 240, 30, key="duration")

        if st.button("Add Task"):
            if custom_task and priority:

                pmap = {"low": 1, "medium": 2, "high": 3}

                # Normalize time input once so all comparisons and storage are consistent
                clean_time = time.strip()

                # Issue 0 (FIX): Validate time format
                if not clean_time or ":" not in clean_time:
                    st.error("Invalid time format. Use HH:MM")
                    st.stop()

                # Issue 1: Duplicate time — compare against normalized stored times
                existing_times = [t.time for t in st.session_state.tasks]
                if clean_time and clean_time in existing_times:
                    st.error("A task already exists at this time.")

                # Issue 2: Available time — cast to int to avoid float precision issues
                elif int(sum(t.duration for t in st.session_state.tasks)) + int(duration) > int(st.session_state.owner.available_time):
                    st.error(f"Cannot add task: total duration would exceed owner's available time ({st.session_state.owner.available_time} min).")

                else:
                    task = Task(custom_task, int(duration), pmap[priority], time=clean_time)
                    st.session_state.tasks.append(task)
                    st.session_state.scheduler.add_task(task)
                    st.success("Task added")
                    st.rerun()

    st.write("---")

    for i, t in enumerate(st.session_state.tasks):
        col1, col2, col3 = st.columns([3, 2, 1])

        with col1:
            st.write(t.name)

        with col2:
            st.write(t.time)

        with col3:
            if st.button("🗑️", key=f"del_task_{i}"):
                st.session_state.tasks.pop(i)
                st.rerun()

# ─────────────────────────────────────────────
# AI SCHEDULER PAGE (UPDATED)
# ─────────────────────────────────────────────
elif page == "🧠 AI Scheduler":

    st.title("🧠 AI Scheduler")

    st.info("Pipeline: UI → RAG → Scheduler Agent → Evaluator → Output")

    scheduler = st.session_state.scheduler
    agent = SchedulerAgent()

    plan = st.session_state.tasks

    if not plan:
        st.warning("No tasks available")
        st.stop()

    # ─────────────────────────────────────
    # ORIGINAL SCHEDULE
    # ─────────────────────────────────────
    st.markdown("### 📌 Original Schedule")

    st.table([
        {"Task": t.name, "Time": t.time if t.time else "No time set"}
        for t in plan
    ])

    # ─────────────────────────────────────
    # GENERATE OPTIMIZED
    # ─────────────────────────────────────
    if st.button("Generate Optimized Schedule"):

        user_input = " ".join([t.name for t in plan])
        result = agent.run(user_input, plan)

        st.session_state.optimized_result = result

    # ─────────────────────────────────────
    # SHOW OPTIMIZED
    # ─────────────────────────────────────
    if "optimized_result" in st.session_state:

        result = st.session_state.optimized_result

        st.markdown("### 🧠 Optimized Schedule")

        st.table([
            {"Task": t.name, "Time": t.time if t.time else "No time set"}
            for t in result["fixed_schedule"]
        ])

        st.markdown("### ⚠️ Evaluation")

        st.success(f"Confidence Score: {result['evaluation']['confidence']}%")

        if result["evaluation"]["issues"]:
            for issue in result["evaluation"]["issues"]:
                st.write("• " + issue)

        st.markdown("### 💡 Explanations")

        for exp in result["explanations"]:
            st.write("• " + exp)

        st.markdown("### 📚 RAG Rules Used")

        for rule in result["rules_used"]:
            st.write("• " + rule)

        st.write("---")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("✅ Accept Optimized Schedule"):

                st.session_state.tasks = result["fixed_schedule"]
                del st.session_state.optimized_result
                st.success("Optimized schedule accepted")
                st.rerun()

        with col2:
            if st.button("↩️ Keep Original Schedule"):

                del st.session_state.optimized_result
                st.info("Kept original schedule")
                st.rerun()