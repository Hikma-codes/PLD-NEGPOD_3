#!/usr/bin/python3
import re

class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.password = None
        
    def validate_email(self):
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(pattern, self.email):
            print(f"Invalid email format: {self.email}")
            return False
        return True
    
    def validate_password(self, password):
        if len(password) < 6:
            print("Password must be at least 6 characters long.")
            return False
        if not re.search(r'[A-Za-z]', password) or not re.search(r'[0-9]', password):
            print("Password must contain both letters and numbers.")
            return False
        return True

    def signup(self, password):
        if not self.validate_email():
            return
        if not self.validate_password(password):
            return
        
        if self.email in User.user_db:
            print(f"User with email {self.email} is already registered.")
        else:
            self.password = password
            User.user_db[self.email] = {'name': self.name, 'password': self.password}
            print(f"User {self.name} with email {self.email} has been successfully signed up.")

    def login(self, password):
        if not self.validate_email():
            return
        
        if self.email in User.user_db:
            if User.user_db[self.email]['password'] == password:
                print(f"Welcome back, {self.name}!")
            else:
                print("Invalid password. Please try again.")
        else:
            print("No user found with this email. Please sign up first.")


