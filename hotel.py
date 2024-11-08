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

    def cancel_booking(self, booking_id):
        if booking_id in self.bookings:
            del self.bookings[booking_id]
            print(f"booking {booking_id} has been canceled.")
        else:
            print(f"booking id {booking_id} not found.")

    def list_amenities(self):
        if not self.amenities:
           print("no amenities available.")
        else:
           print("amenities:")
           for amenity in self.amenities:
               print(f" - {amenity}")
