from pawpal_system import Task, Pet

def test_task_completion():
    task = Task("Walk", 30, 2)
    task.mark_complete()
    assert task.completed == True


def test_task_addition():
    pet = Pet("Mochi", "dog")
    initial_count = len(pet.tasks)

    pet.add_task(Task("Feed", 10, 3))
    assert len(pet.tasks) == initial_count + 1