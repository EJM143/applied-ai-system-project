# PawPal+ Project Reflection

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
