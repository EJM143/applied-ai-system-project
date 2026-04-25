import os


class Evaluator:
    """
    Evaluator class for checking schedule quality and logging results.
    """

    def __init__(self):
        """Initialize the Evaluator."""
        pass

    def validate(self, schedule, conflicts):
        """
        Validate a schedule and return a list of issues found.

        Args:
            schedule (list): List of Task objects to validate
            conflicts (list): List of conflict tuples (task1, task2, time)

        Returns:
            list: List of issue strings. Possible issues:
                  - "conflicts_exist" if any conflicts are found
                  - "empty_schedule" if schedule is empty
        """
        issues = []

        # Check if schedule is empty
        if not schedule or len(schedule) == 0:
            issues.append("empty_schedule")

        # Check if conflicts exist
        if conflicts and len(conflicts) > 0:
            issues.append("conflicts_exist")
    
        # Rule: schedule must include at least one feeding task
        has_feeding = any("feed" in task.name.lower() for task in schedule)

        if not has_feeding:
            issues.append("missing_feeding")

        return issues

    def score(self, issues, conflicts_fixed_count):
        """
        Calculate a confidence score based on issues and conflict fixes.

        Args:
            issues (list): List of issue strings from validate()
            conflicts_fixed_count (int): Number of conflicts that were fixed

        Returns:
            int: Confidence score from 0 to 100
        """

        if not issues or len(issues) == 0:
            return 95

        if "empty_schedule" in issues:
            return 50

        if "conflicts_exist" in issues:
            if conflicts_fixed_count > 0:
                return 80
            else:
                return 60

        return 95

    def log(self, conflicts_fixed_count, score):
        """
        Write evaluation results to a log file.
        """
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        log_file_path = os.path.join(log_dir, "system_log.txt")

        log_entry = (
            f"Schedule checked\n"
            f"Conflicts fixed: {conflicts_fixed_count}\n"
            f"Confidence: {score}%\n"
        )

        with open(log_file_path, "a") as log_file:
            log_file.write(log_entry)

    def evaluate(self, schedule, conflicts, conflicts_fixed_count):
        """
        Validate schedule, compute score, log results, and return feedback.
        """

        issues = self.validate(schedule, conflicts)
        confidence = self.score(issues, conflicts_fixed_count)

        self.log(conflicts_fixed_count, confidence)

        feedback = []

        if "empty_schedule" in issues:
            feedback.append("Schedule is empty. Please add tasks.")

        if "conflicts_exist" in issues:
            feedback.append("There are overlapping tasks at the same time.")

        if "missing_feeding" in issues:
            feedback.append("At least one feeding task is required per day.")

        if not feedback:
            feedback.append("Schedule looks good. No issues found.")

        return {
            "issues": issues,
            "confidence": confidence,
            "feedback": feedback
        }