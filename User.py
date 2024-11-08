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

class Hotel:
    def __init__(self, name, location, amenities, room_types):
        self.name = name
        self.location = location
        self.amenities = amenities
        self.room_types = room_types
