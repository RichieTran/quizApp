# quizzr

## Overview
Quizzr is a CLI Python Quiz App, meaning it quizzes users on how to use Python (could be basic stuff like if & elif or more advanced stuff like data structures), which should be chosen in a "topics" section before quizzing the user. It needs to have a local login system and it will read questions from a JSON file. Quizzr should also track scores and performance statistics securely (in a non-human-readable format), and it should allow users to provide feedback on questions to influence future quiz selections, and saves results. Finally it should also have a streak tracker (ie how many questions they have correct in a row).

## Data Format
Your question bank should be a JSON file using the format below:
{
  "questions": [
    {
      "question": "What keyword is used to define a function in Python?",
      "type": "multiple_choice",
      "options": ["func", "define", "def", "function"],
      "answer": "def",
      "category": "Python Basics"
    },
    {
      "question": "A list in Python is immutable.",
      "type": "true_false",
      "answer": "false",
      "category": "Data Structures"
    },
    {
      "question": "What built-in function returns the number of items in a list?",
      "type": "short_answer",
      "answer": "len",
      "category": "Python Basics"
    },
    {
      "question": "What is the difference between '=' and '=='?",
      "type": "multiple_choice",
      "options": ["'=' sets value and '==' compares values", "no difference", "'==' sets value and '=' compares values", "i don't know"],
      "answer": "'=' sets value and '==' compares values",
      "category": "Python Basics"
    },
    {
      "question": "Return the last element from a list, A, of unknown size:",
      "type": "short_answer",
      "answer": "A[-1]",
      "category": "Python Basics"
    }
  ]
}

## Suggested File Structure:
quizApp/
├── main.py          # Entry point — runs the quizzes
├── questions.JSON   # Question bank
├── quiz.py          # Quiz logic — asking, scoring, feedback
└── README.md        # How to run it, what it does

## Error Handling:
- If no 'questions.JSON' exists then the app should print a message like "Could not find questions" then exit.
- If user types invalid input like "e" on a multiple choice answer, then it should say "Invalid Answer" and ask user the same question.
- If the user interrupts the quiz ie "Ctrl+C", then close the app but print how many questions they answer ie "Quiz cancelled, you answered 3/10 questions before quitting"

## Required Features:
- A local login system that prompts users for a username and password (or allows them to enter a new username and password). The passwords should not be easily discoverable.
- A score history file that tracks performance and other useful statistics over time for each user. This file should not be human-readable and should be relatively secure. (This means someone could look at the file and perhaps find out usernames but not passwords or scores.)
- Users should somehow be able to provide feedback on whether they like a question or not, and this should inform what questions they get next.
- The questions should exist in their own human-readable .json file so that they can be easily modified. (This lets you use the project for studying other subjects if you wish; all you have to do is generate the question bank.)
- Note: None of this requires a backend, HTML, CSS, a graphical user interface, or the use of any APIs. Everything is local. If your project uses any of these things, you migth be over-engineering it.
- Score streak of how many correct questions in a row.

## Acceptance Criteria
1. Happy path works end to end — Running python main.py loads questions from JSON, presents them one at a time with numbered options, accepts valid input, tracks score, and prints a final summary like "You got 7/10 (70%)!"
2. Empty question bank exits gracefully — If questions.json contains an empty list [], the app prints specified message and exits.
3. Missing file exits gracefully, If questions.json doesn't exist, the app prints "Could not find questions.json" and exits.
4. Malformed JSON exits gracefully — If questions.json contains broken syntax, the app prints "Questions are not valid" and exits.
5. Invalid input re-prompts, If the user types something other than a valid option, the app says "Invalid choice, try again" and re-prompts for the same question. The question is not skipped or counted as wrong.
6. Ctrl+C exits cleanly, pressing Ctrl+C at any point during the quiz prints a short "Quiz cancelled" message with the current score, and exits.
7. Questions with missing fields are skipped. If a question in the JSON is missing prompt, options, or answer, it's skipped (with a warning) and doesn't crash the app. The total count adjusts accordingly.
8. Score is accurate. The final score correctly reflects the number of right answers. Running through a 3-question bank and answering all correctly shows 3/3. Answering all wrong shows 0/3.