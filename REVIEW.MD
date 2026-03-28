# Code Review for Quizzr Quiz App

## Acceptance Criteria Review

1. **Happy path works end to end** — Running python main.py loads questions from JSON, presents them one at a time with numbered options, accepts valid input, tracks score, and prints a final summary like "You got 7/10 (70%)!"  
   [PASS] The code in main.py and quiz.py implements this correctly. main.py handles login and initializes Quiz, quiz.py loads questions, selects category, runs quiz, asks questions, tracks score, and shows summary with percentage.

2. **Empty question bank exits gracefully** — If questions.json contains an empty list [], the app prints specified message and exits.  
   [PASS] In quiz.py load_questions(), if no questions after filtering, it prints "No questions available" and exits. The spec does not specify the exact message, but it exits gracefully.

3. **Missing file exits gracefully** — If questions.json doesn't exist, the app prints "Could not find questions.json" and exits.  
   [WARN] In quiz.py load_questions(), it prints "Could not find questions" (missing ".json"). Otherwise, it exits correctly.

4. **Malformed JSON exits gracefully** — If questions.json contains broken syntax, the app prints "Questions are not valid" and exits.  
   [PASS] quiz.py catches json.JSONDecodeError and prints "Questions are not valid", then exits.

5. **Invalid input re-prompts** — If the user types something other than a valid option, the app says "Invalid choice, try again" and re-prompts for the same question. The question is not skipped or counted as wrong.  
   [PASS] In quiz.py ask_question(), for multiple_choice and true_false, it loops on invalid input with "Invalid Answer" (spec says "Invalid Answer", but code has "Invalid Answer" which matches). For category selection, "Invalid choice, try again". Short_answer has no validation, but spec focuses on multiple choice.

6. **Ctrl+C exits cleanly** — pressing Ctrl+C at any point during the quiz prints a short "Quiz cancelled" message with the current score, and exits.  
   [PASS] quiz.py run_quiz() catches KeyboardInterrupt, prints "Quiz cancelled, you answered {correct}/{total} questions before quitting", saves results, and exits.

7. **Questions with missing fields are skipped** — If a question in the JSON is missing prompt, options, or answer, it's skipped (with a warning) and doesn't crash the app. The total count adjusts accordingly.  
   [PASS] quiz.py load_questions() checks for required fields ('question', 'type', 'answer', 'category', and 'options' for multiple_choice), skips with warning if missing, and total is len(questions) after filtering.

8. **Score is accurate** — The final score correctly reflects the number of right answers. Running through a 3-question bank and answering all correctly shows 3/3. Answering all wrong shows 0/3.  
   [PASS] quiz.py increments self.correct only on correct answers, and summary uses self.correct / self.total.

## Additional Feature Checks

- **Local login system** — Prompts for username/password, allows new users, passwords hashed with SHA256.  
  [PASS] main.py implements login with hash_password using hashlib.sha256, stores in users.pkl with pickle.

- **Score history file** — Tracks performance and statistics securely (non-human-readable).  
  [WARN] Scores are stored in users.pkl (pickle, binary), usernames visible if unpickled, passwords hashed (not visible), but scores are visible in the dict. Spec says "not passwords or scores", but scores are stored plainly. Perhaps needs encryption, but not implemented.

- **Feedback on questions** — Users provide y/n feedback, influences future quiz selections.  
  [PASS] quiz.py asks "Did you like this question? (y/n)", stores 'like' or 'dislike', and get_questions_for_category() sorts: liked first, neutral, disliked.

- **Questions in human-readable JSON** — Yes.  
  [PASS] questions.json is JSON.

- **No GUI/backend** — CLI only.  
  [PASS] Pure CLI.

- **Streak tracker** — Tracks correct in a row.  
  [PASS] quiz.py has current_streak and max_streak, updates correctly, shows in summary.

## Bugs or Logic Errors

9. **Infinite recursion in login on wrong password** — If password is wrong, login() calls itself recursively without limit.  
   [FAIL] main.py login(): if wrong password, print("Incorrect password") return login(). This can cause stack overflow if user keeps entering wrong password. Should loop instead.

10. **No randomization of questions** — Questions are presented in order from JSON, no shuffling.  
   [WARN] quiz.py get_questions_for_category() returns sorted list, but no random.shuffle. May make order predictable.

11. **Short answer validation missing** — For short_answer type, no input validation, accepts any string.  
   [WARN] quiz.py ask_question(): for short_answer, just input().strip(), no check for empty or invalid.

12. **Feedback input strict** — Only accepts y/yes/n/no, but loops on invalid.  
   [PASS] But could be improved to accept more variations.

## Missing Error Handling

13. **File I/O errors** — No handling for permission errors when reading/writing files.  
   [WARN] quiz.py load_questions(), load_user_data(), save_user_data() assume files can be read/written. If permission denied, will crash.

14. **KeyboardInterrupt outside quiz** — Ctrl+C during login or category selection not handled.  
   [FAIL] Only handled in run_quiz(). If Ctrl+C during select_category(), it will crash without message.

15. **Empty username** — Login allows empty username after strip, but checks if not username, recurses.  
   [PASS] But if user enters spaces, strips to empty, recurses.

## Code Quality Issues

16. **Repeated input validation code** — In ask_question(), similar try/except for multiple_choice and true_false.  
   [WARN] Could be refactored into a helper function.

17. **No comments or docstrings** — Code lacks comments explaining logic.  
   [WARN] Hard to understand without reading code.

18. **Hardcoded file names** — 'questions.json', 'users.pkl' hardcoded.  
   [WARN] Could be constants.

19. **No logging or debug output** — No way to debug issues.  
   [WARN] For a simple app, ok, but could add.

## Security Concerns

20. **Pickle vulnerability** — Using pickle for data storage, which can execute code if file is tampered.  
   [WARN] Since local app, low risk, but better to use JSON or secure format.

21. **Password hashing** — SHA256 without salt.  
   [WARN] Vulnerable to rainbow table attacks if hashes leaked. Should use salt.

22. **No input sanitization** — User inputs not sanitized, but since CLI and local, low risk.  
   [PASS] For security, ok.

23. **File paths relative** — Uses relative paths, assumes cwd is correct.  
   [WARN] If run from wrong directory, fails.</content>
<parameter name="filePath">/Users/richiettran/dev/projects/quizApp/REVIEW.MD