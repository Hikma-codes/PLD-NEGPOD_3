#!/usr/bin/python3

class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

class Hotel:
    def __init__(self, name, location, amenities, room_types):
        self.name = name
        self.location = location
        self.amenities = amenities
        self.room_types = room_types