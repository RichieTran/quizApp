import getpass
import hashlib
import os
import pickle
from quiz import Quiz

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login():
    username = input("Username: ").strip()
    if not username:
        print("Username cannot be empty")
        return login()
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
            print("Incorrect password")
            return login()
    else:
        password = getpass.getpass("New password: ")
        confirm = getpass.getpass("Confirm password: ")
        if password != confirm:
            print("Passwords do not match")
            return login()
        users[username] = {'password_hash': hash_password(password)}
        with open('users.pkl', 'wb') as f:
            pickle.dump(users, f)
        return username

def main():
    print("Welcome to Quizzr!")
    username = login()
    quiz = Quiz(username)
    quiz.select_category()
    quiz.run_quiz()

if __name__ == "__main__":
    main()