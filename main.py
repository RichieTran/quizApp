import getpass
import hashlib
import os
import pickle
from quiz import Quiz

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login():
    while True:
        username = input("Username: ").strip()
        if not username:
            print("Username cannot be empty")
            continue

        if os.path.exists('users.pkl'):
            with open('users.pkl', 'rb') as f:
                users = pickle.load(f)
        else:
            users = {}

        if username in users:
            password = getpass.getpass("Password: ")
            if hash_password(password) == users[username].get('password_hash'):
                return username
            else:
                print("Incorrect password, try again")
                continue

        password = getpass.getpass("New password: ")
        confirm = getpass.getpass("Confirm password: ")
        if password != confirm:
            print("Passwords do not match, try again")
            continue

        users[username] = {'password_hash': hash_password(password)}
        with open('users.pkl', 'wb') as f:
            pickle.dump(users, f)
        return username

def main():
    print("Welcome to Quizzr!")
    try:
        username = login()
        quiz = Quiz(username)
        quiz.select_category()
        quiz.run_quiz()
    except KeyboardInterrupt:
        print("\nQuiz cancelled, you answered 0/0 questions before quitting")
        # Data may not have been generated yet; exit cleanly
        exit(0)

if __name__ == "__main__":
    main()