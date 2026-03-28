import json
import os
import pickle
import datetime
import random

USERS_FILE = 'users.pkl'
USER_DATA_FILE = 'user_data.pkl'
SCORE_HISTORY_FILE = 'score_history.pkl'

class Quiz:
    def __init__(self, username):
        self.username = username
        self.questions = self.load_questions()
        self.user_data = self.load_user_data()
        self.current_streak = self.user_data.get('streak', 0)
        self.max_streak = self.user_data.get('max_streak', 0)
        self.correct = 0
        self.total = 0
        self.category = None

    def load_questions(self):
        if not os.path.exists('questions.json'):
            print("Could not find questions")
            exit(1)
        try:
            with open('questions.json', 'r') as f:
                data = json.load(f)
        except json.JSONDecodeError:
            print("Questions are not valid")
            exit(1)
        questions = []
        for q in data.get('questions', []):
            if 'question' in q and 'type' in q and 'answer' in q and 'category' in q:
                if q['type'] == 'multiple_choice' and 'options' not in q:
                    print(f"Warning: Skipping invalid question: {q.get('question', 'Unknown')}")
                    continue
                questions.append(q)
            else:
                print(f"Warning: Skipping invalid question: {q.get('question', 'Unknown')}")
        if not questions:
            print("No questions available")
            exit(1)
        return questions

    def load_user_data(self):
        if os.path.exists(USER_DATA_FILE):
            with open(USER_DATA_FILE, 'rb') as f:
                all_data = pickle.load(f)
            return all_data.get(self.username, {})
        return {}

    def save_user_data(self):
        if os.path.exists(USER_DATA_FILE):
            with open(USER_DATA_FILE, 'rb') as f:
                all_data = pickle.load(f)
        else:
            all_data = {}
        all_data[self.username] = self.user_data
        with open(USER_DATA_FILE, 'wb') as f:
            pickle.dump(all_data, f)

    def append_score_history(self, score_entry):
        if os.path.exists(SCORE_HISTORY_FILE):
            with open(SCORE_HISTORY_FILE, 'rb') as f:
                history = pickle.load(f)
        else:
            history = {}
        history.setdefault(self.username, []).append(score_entry)
        with open(SCORE_HISTORY_FILE, 'wb') as f:
            pickle.dump(history, f)

    def select_category(self):
        categories = set(q['category'] for q in self.questions)
        if not categories:
            print("No questions available.")
            exit(1)
        print("Available topics:")
        cat_list = sorted(categories)
        for i, cat in enumerate(cat_list, 1):
            print(f"{i}. {cat}")
        while True:
            try:
                choice = int(input("Select a topic: "))
                if 1 <= choice <= len(cat_list):
                    self.category = cat_list[choice-1]
                    break
                else:
                    print("Invalid choice, try again")
            except ValueError:
                print("Invalid choice, try again")

    def get_questions_for_category(self):
        qs = [q for q in self.questions if q['category'] == self.category]
        # To influence future selections, sort by feedback and randomize each bucket for variety
        feedback = self.user_data.get('feedback', {})
        liked = [q for q in qs if feedback.get(q['question'], '') == 'like']
        disliked = [q for q in qs if feedback.get(q['question'], '') == 'dislike']
        neutral = [q for q in qs if q['question'] not in feedback]
        random.shuffle(liked)
        random.shuffle(neutral)
        random.shuffle(disliked)
        # Prefer liked, then neutral, then disliked
        qs = liked + neutral + disliked
        return qs

    def run_quiz(self):
        questions = self.get_questions_for_category()
        if not questions:
            print("No questions in this category.")
            return
        self.total = len(questions)
        try:
            for q in questions:
                self.ask_question(q)
        except KeyboardInterrupt:
            print(f"\nQuiz cancelled, you answered {self.correct}/{self.total} questions before quitting")
            self.save_results()
            exit(0)
        self.show_summary()
        self.save_results()

    def ask_question(self, q):
        print(f"\n{q['question']}")
        if q['type'] == 'multiple_choice':
            for i, opt in enumerate(q['options'], 1):
                print(f"{i}. {opt}")
            while True:
                try:
                    ans = int(input("Your answer: "))
                    if 1 <= ans <= len(q['options']):
                        user_ans = q['options'][ans-1]
                        break
                    else:
                        print("Invalid Answer")
                except ValueError:
                    print("Invalid Answer")
        elif q['type'] == 'true_false':
            print("1. True")
            print("2. False")
            while True:
                try:
                    ans = int(input("Your answer: "))
                    if ans == 1:
                        user_ans = 'true'
                    elif ans == 2:
                        user_ans = 'false'
                    else:
                        print("Invalid Answer")
                        continue
                    break
                except ValueError:
                    print("Invalid Answer")
        elif q['type'] == 'short_answer':
            while True:
                user_ans = input("Your answer: ").strip()
                if user_ans:
                    break
                print("Invalid Answer")
        else:
            print("Unknown question type")
            return
        correct = user_ans.lower() == q['answer'].lower()  # case insensitive for matching
        if correct:
            print("Correct!")
            self.correct += 1
            self.current_streak += 1
            if self.current_streak > self.max_streak:
                self.max_streak = self.current_streak
        else:
            print(f"Wrong! The correct answer is {q['answer']}")
            self.current_streak = 0
        print(f"Current streak: {self.current_streak}")
        # Feedback
        while True:
            fb = input("Did you like this question? (y/n): ").strip().lower()
            if fb in ['y', 'yes']:
                self.user_data.setdefault('feedback', {})[q['question']] = 'like'
                break
            elif fb in ['n', 'no']:
                self.user_data.setdefault('feedback', {})[q['question']] = 'dislike'
                break
            else:
                print("Please answer y or n")

    def show_summary(self):
        percentage = (self.correct / self.total) * 100 if self.total > 0 else 0
        print(f"\nYou got {self.correct}/{self.total} ({percentage:.1f}%)!")
        print(f"Current streak: {self.current_streak}")
        print(f"Max streak: {self.max_streak}")

    def save_results(self):
        self.user_data['streak'] = self.current_streak
        self.user_data['max_streak'] = self.max_streak
        self.save_user_data()

        score_entry = {
            'date': datetime.datetime.now().isoformat(),
            'category': self.category,
            'score': f"{self.correct}/{self.total}",
            'streak': self.current_streak
        }
        self.append_score_history(score_entry)
