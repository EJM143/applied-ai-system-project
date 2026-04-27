# PawPal+ Project 2 Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.

My initial UML design included four main classes: Owner, Pet, Task, and Scheduler.

- What classes did you include, and what responsibilities did you assign to each?

The Owner class is responsible for storing the user’s basic information and available time for pet care. The Pet class stores information about the pet, such as name and type. The Task class represents individual pet care activities, including name, duration, and priority. The Scheduler class is responsible for organizing tasks and generating a daily plan based on available time and task priority.

**b. Design changes**

- Did your design change during implementation?

Yes, the design changed during implementation.

- If yes, describe at least one change and why you made it.

Initially, tasks did not include time or date attributes. These were added later to support sorting, scheduling, and conflict detection. This change made it possible to organize tasks more realistically and detect when tasks happen at the same time.
Another change was updating the task completion logic to support recurring tasks. The mark_complete() method was modified to create the next occurrence for daily and weekly tasks. This improved the system by making it more automated and closer to real-life scheduling.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?

The scheduler considers task time, priority level, duration, and completion status. It also considers the owner’s available time when building a daily plan. Tasks with higher priority are considered first when creating the schedule. Time is used to sort and detect conflicts, while duration is used to fit tasks into the available schedule.

- How did you decide which constraints mattered most?

Priority and available time were chosen as the most important because they directly affect what gets done in a day.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.

One tradeoff is that conflict detection only checks for exact matching start times. It does not detect overlapping task durations. This keeps the system simple and easy to understand, but it may miss some real scheduling conflicts.

- Why is that tradeoff reasonable for this scenario?

This tradeoff is reasonable because it reduces complexity and keeps the scheduler beginner-friendly while still catching the most common conflicts.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?

I used AI tools to help design the UML structure, improve scheduling logic, and debug issues in the implementation. 

- What kinds of prompts or questions were most helpful?

The most useful prompts were those asking for simplification, and debugging help.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.

One moment where I did not accept the AI suggestion was when it recommended making the scheduling logic more complex with advanced overlap handling. I chose not to implement it because it would make the system harder to understand and was not required for the project.

- How did you evaluate or verify what the AI suggested?

I verified AI suggestions by comparing them with my actual code and running tests to confirm behavior. If the suggestion added unnecessary complexity or did not match my design goals, I simplified or ignored it.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?

I tested task sorting by priority and time, recurring task behavior, conflict detection, and scheduling with limited available time. 

- Why were these tests important?

These tests were important because they confirm that the core scheduling logic works correctly and handles real usage scenarios.

**b. Confidence**

- How confident are you that your scheduler works correctly?

I am highly confident that my scheduler works correctly because all major behaviors passed testing and match the expected logic.

- What edge cases would you test next if you had more time?

If I had more time, I would test more edge cases such as overlapping durations, large numbers of tasks, and unusual recurrence patterns.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I am most satisfied with the scheduling logic because it correctly balances priority and available time while still being simple and readable.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

If I had another iteration, I would improve conflict detection to handle overlapping time ranges instead of only exact matches. I would also improve the UI to make task input more interactive.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

I learned that designing a system is easier when you start simple and gradually add features. I also learned that AI is helpful for generating ideas and debugging, but the final decisions should focus on keeping the system simple and easy to understand.

---

# PawPal+ Project 4 Applied AI System Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial design for the AI system.

My initial design for Project 4 extended the Project 2 scheduler with three AI-inspired components: a Retrieval-Augmented Generation (RAG) module to surface pet care rules, a Scheduler Agent to detect and resolve conflicts, and an Evaluator to score schedule quality. The system was planned as a linear pipeline — user input flows through RAG retrieval, then the agent, then the evaluator, and finally returns a structured result to the UI.

- What components did you plan, and what role did each play?

The RAG module was planned as a knowledge provider that retrieves relevant care rules based on task context. The Scheduler Agent was responsible for conflict detection and resolution. The Evaluator acted as a built-in critic to validate the output and assign a confidence score. A Streamlit web app was planned as the user-facing interface to replace the CLI demo.

**b. Design changes**

- Did your design change during implementation?

Yes, several changes were made during implementation.

- If yes, describe at least one change and why you made it.

The most significant change was adding three UI-layer guardrails in the Streamlit app that were not in the original plan. These prevent tasks with invalid time formats, duplicate time slots, or durations that exceed the owner's available time from ever reaching the AI pipeline. This change was made because without input validation, the agent could receive malformed data and produce incorrect or misleading results. Catching these problems at the boundary was simpler and more reliable than handling them inside the agent.

Another change was making conflict resolution non-destructive by using a deep copy of the schedule before applying any fixes. This allowed the original schedule to be preserved so the user could compare it against the optimized version and choose whether to accept or reject the changes.

---

## 2. Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your AI system consider?

The system considers task time slots (for conflict detection), task duration and owner available time (for plan generation), task priority (for scheduling order), and pet care domain rules (retrieved via the RAG module). The evaluator also checks for the presence of at least one feeding task, since feeding is considered a non-negotiable daily requirement.

- How did you decide which constraints mattered most?

Conflict-free scheduling and available time were treated as hard constraints — violating them produces an unusable schedule. Priority and domain rules were treated as soft constraints that guide quality but do not block execution. This ordering matched what would matter most to a real pet owner.

**b. Tradeoffs**

- Describe one tradeoff your AI system makes.

The RAG retrieval uses keyword matching instead of semantic search or embeddings. This means a task named "administer insulin" would not retrieve medication rules, because the keyword trigger is "med" or "medicine." Precision is high for tasks using expected vocabulary, but recall suffers for synonyms or unusual phrasing.

- Why is that tradeoff reasonable for this scenario?

This tradeoff is reasonable because the task types in PawPal+ are limited and user-defined from a small set of common categories (feeding, walking, medication, scheduling). Keyword matching is fully deterministic, requires no external dependencies, and is easy to extend. For a larger or more open-ended domain, embedding-based retrieval would be worth the added complexity.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project?

I used AI tools throughout the project for planning the pipeline architecture, drafting the agent and evaluator logic, debugging edge cases in conflict resolution, and refining the Streamlit UI layout. AI was especially useful for thinking through the non-destructive scheduling approach and for suggesting how to structure the evaluator's scoring logic.

- What kinds of prompts or questions were most helpful?

The most useful prompts asked AI to explain the tradeoffs between two specific approaches (for example, keyword RAG vs. embedding RAG for this project scope), or to identify potential edge cases in a specific function. Asking AI to review a function and point out what could go wrong was more useful than asking it to write the function from scratch.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.

When designing the conflict resolution logic, AI suggested resolving conflicts by sorting all tasks into non-overlapping slots using a greedy interval-packing algorithm. I chose not to implement this because it would silently reorder all tasks, not just the conflicting ones, which could confuse the user and make the explanation step unreliable. Instead, I kept the simpler approach of shifting only the second conflicting task forward by one hour, which is predictable and easy to explain.

- How did you evaluate or verify what the AI suggested?

I verified AI suggestions by tracing through the logic manually with a concrete example before accepting them, and by running the test suite after each significant change. If a suggestion changed behavior in a way that was not reflected in the existing tests, I wrote a new test to confirm the behavior was correct before moving on.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?

I tested 33 behaviors across two test files. For the base system: task completion and recurrence, sort order by time and priority, conflict detection for two and three tasks at the same time, and plan generation with limited available time. For the AI pipeline: RAG keyword retrieval for feeding and walking rules, agent conflict detection and fixing, explanation generation, the full `run()` pipeline output structure, invalid time format handling, and evaluator detection of a missing feeding task.

- Why were these tests important?

The agent tests were especially important because the pipeline has multiple stages and an error in an early stage (like invalid time arithmetic) would silently corrupt every downstream result. Testing each stage independently made it easier to locate failures and confirm that edge cases like malformed time strings did not crash the system.

**b. Confidence**

- How confident are you that your system works correctly?

I am highly confident in the core pipeline behavior because all 33 tests pass and the system log shows consistent 95% confidence scores for clean schedules and 80% scores when a conflict was detected and fixed. The guardrails have also been exercised through manual UI testing across the three main scenarios: no conflict, conflict detected and fixed, and invalid input blocked.

- What edge cases would you test next if you had more time?

I would test tasks with durations long enough that shifting by one hour still causes an overlap with a third task, a schedule where all tasks are at the same time to verify the multi-conflict resolution loop terminates correctly, and RAG retrieval for task names that describe the same activity using different words (for example, "administer meds" vs. "give medication").

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I am most satisfied with the end-to-end pipeline design — the way RAG, the agent, and the evaluator each have a single responsibility and pass a clean result to the next stage. This separation made it straightforward to test each component independently and made the explanation output predictable because only one stage (the agent) ever modifies the schedule.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would improve the RAG retrieval to use semantic similarity so that task names with unusual phrasing still match the right rules. I would also improve conflict resolution to handle duration overlap rather than only exact time matches, which would make the system accurate for tasks like a 90-minute walk scheduled at 08:00 conflicting with a 30-minute feeding at 09:00. Finally, I would add an undo history so users could step back through multiple accepted changes rather than only being able to reject the most recent one.

**c. Key takeaway**

- What is one important thing you learned about designing AI systems on this project?

I learned that the most important design decision in an AI pipeline is where to place guardrails and validation. A well-structured system catches bad input at the boundary so that every component downstream can assume it is working with valid data. This made the agent and evaluator logic much simpler than they would have been if each stage had to handle every possible error condition on its own.

## 6. Ethics and Misuse Risk

**a. Misuse risk**
This system could be misused if a user enters incorrect or misleading pet care tasks and relies fully on the generated schedule without checking it. This could lead to missed care activities or incorrect task timing for pets.

Another risk is that users might assume the AI output is always correct because it includes a confidence score, even though it is still rule-based and limited.

**b. Prevention and mitigation**
To reduce these risks, the system uses guardrails to block invalid input formats and prevent clearly impossible schedules from entering the pipeline. The evaluator also flags missing critical tasks (like feeding), which helps catch unsafe schedules.

However, users are still expected to review the final schedule manually, since the system is a decision-support tool and not a fully autonomous scheduler.