class Hotel:
    def __init__(self, name, location, amenities, room_types):
        self.name = name
        self.location = location
        self.amenities = amenities
        self.room_types = room_types

    def book_room(self, room_types, room_number):
        self.room_number = room_number
        