from pawpal_system import Owner, Pet, Task, Scheduler

# Owner
jordan = Owner("Jordan", available_time=90)

# Pets
mochi = Pet("Mochi", "dog", breed="Shiba Inu", age=3)
luna = Pet("Luna", "cat", breed="Tabby", age=5)

# Tasks for Mochi
mochi.add_task(Task("Morning walk", 30, 3, description="Around the block twice"))
mochi.add_task(Task("Training session", 20, 2, description="Sit, stay, shake"))
mochi.add_task(Task("Grooming", 45, 1, description="Brush coat and trim nails"))

# Tasks for Luna
luna.add_task(Task("Playtime", 15, 3, description="Feather wand and laser"))
luna.add_task(Task("Vet check notes", 10, 2, description="Log weight and behavior"))

# Assign pets to owner
jordan.add_pet(mochi)
jordan.add_pet(luna)

# Schedule
scheduler = Scheduler(jordan)
scheduler.load_tasks_from_owner()
scheduler.generate_plan()

print("=" * 50)
print("       TODAY'S SCHEDULE — PawPal+")
print("=" * 50)
scheduler.display_plan()
