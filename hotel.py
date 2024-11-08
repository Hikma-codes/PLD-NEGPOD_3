class Hotel:
    def __init__(self, name, location, amenities, room_types):
        self.name = name
        self.location = location
        self.amenities = amenities
        self.room_types = room_types

    def book_room(self, room_types, room_number):
        self.room_number = room_number

    def show_details(self):
        print(f"This is the hotel name {self.name}")
        print(f"This is the hotel location {self.location}")
        print(f"This is the hotel amenities {self.amenities}")
        print(f"This is the hotel room_types {self.room_types}")
    