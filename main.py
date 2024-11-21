class User:
    def __init__(self, username, password, name, email):
        self.username = username
        self.password = password
        self.name = name
        self.email = email

class Hotel:
    def __init__(self, name, location, num_rooms, amenities):
        self.name = name
        self.location = location
        self.num_rooms = num_rooms
        self.amenities = amenities
        self.rooms = [{"room_no": i+1, "occupied": False, "guest_name": None, "check_in": None, "check_out": None} for i in range(num_rooms)]
        self.itineraries = []

    def add_itinerary(self, activity, time, price):
        itinerary = Itinerary(self, activity, time, price)
        self.itineraries.append(itinerary)

    def check_in(self, room_no, guest_name, check_in_date, check_out_date):
        for room in self.rooms:
            if room["room_no"] == room_no and not room["occupied"]:
                room["occupied"] = True
                room["guest_name"] = guest_name
                room["check_in"] = check_in_date
                room["check_out"] = check_out_date
                print(f"{guest_name} checked in to room {room_no} from {check_in_date} to {check_out_date}")
                return
        print(f"Room {room_no} is not available.")

    def check_out(self, room_no):
        for room in self.rooms:
            if room["room_no"] == room_no and room["occupied"]:
                guest_name = room["guest_name"]
                check_in_date = room["check_in"]
                check_out_date = room["check_out"]
                room["occupied"] = False
                room["guest_name"] = None
                room["check_in"] = None
                room["check_out"] = None
                print(f"{guest_name} checked out of room {room_no} (stayed from {check_in_date} to {check_out_date})")
                return
        print(f"Room {room_no} is not occupied.")

    def get_available_rooms(self):
        available_rooms = [room for room in self.rooms if not room["occupied"]]
        return available_rooms
