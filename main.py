import datetime

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

class Itinerary:
    def __init__(self, hotel, activity, time, price):
        self.hotel = hotel
        self.activity = activity
        self.time = time
        self.price = price

class HotelManagementSystem:
    def __init__(self):
        self.users = [User("root", "123", "Admin", "admin@example.com")]
        self.hotels = [
            Hotel("Grand Hotel", "New York", 50, ["Swimming pool", "Gym", "Restaurant"]),
            Hotel("Seaside Resort", "Miami", 30, ["Beach", "Spa", "Bar"]),
            Hotel("Mountain Retreat", "Colorado", 20, ["Hiking trails", "Sauna", "Fireplace"])
        ]

        # Add itineraries for each hotel
        self.hotels[0].add_itinerary("Gym", "9:00 AM", 10.00)
        self.hotels[0].add_itinerary("Swimming", "10:00 AM", 15.00)
        self.hotels[1].add_itinerary("Beach", "11:00 AM", 20.00)
        self.hotels[1].add_itinerary("Spa", "2:00 PM", 50.00)
        self.hotels[2].add_itinerary("Hiking", "9:00 AM", 25.00)
        self.hotels[2].add_itinerary("Sauna", "4:00 PM", 15.00)

    def login(self):
        username = input("Enter username: ")
        password = input("Enter password: ")
        for user in self.users:
            if user.username == username and user.password == password:
                print(f"Welcome, {user.name}!")
                self.home_page(user)
                return
        print("Invalid username or password. Please try again or create an account.")
        self.login()

    def signup(self):
        username = input("Enter a new username: ")
        password = input("Enter a new password: ")
        name = input("Enter your name: ")
        email = input("Enter your email: ")
        new_user = User(username, password, name, email)
        self.users.append(new_user)
        print("Account created successfully. Please log in.")
        self.login()

    def home_page(self, user):
        while True:
            print("\nHome Page:")
            print("1. Profile")
            print("2. Select Hotel")
            print("3. Itineraries")
            print("4. Logout")
            choice = input("Enter your choice (1-4): ")

            if choice == "1":
                self.profile(user)
            elif choice == "2":
                self.select_hotel(user)
            elif choice == "3":
                self.view_itineraries(user)
            elif choice == "4":
                print("Logging out...")
                return
            else:
                print("Invalid choice. Please try again.")

    def profile(self, user):
        print(f"\nProfile Information:")
        print(f"Name: {user.name}")
        print(f"Email: {user.email}")
        input("Press Enter to continue...")

    def select_hotel(self, user):
        print("\nSelect a hotel:")
        for i, hotel in enumerate(self.hotels):
            print(f"{i+1}. {hotel.name} - {hotel.location}")
        choice = int(input("Enter your choice (1-3): "))
        if 1 <= choice <= len(self.hotels):
            self.view_hotel(self.hotels[choice-1])
        else:
            print("Invalid choice. Please try again.")

    def view_hotel(self, hotel):
        print(f"\nHotel: {hotel.name}")
        print(f"Location: {hotel.location}")
        print(f"Rooms: {hotel.num_rooms}")
        print(f"Amenities: {', '.join(hotel.amenities)}")
        print("\nAvailable Rooms:")
        for room in hotel.get_available_rooms():
            print(f"Room {room['room_no']}")
        self.book_room(hotel)

    def book_room(self, hotel):
        room_no = int(input("Enter the room number to book: "))
        guest_name = input("Enter the guest name: ")
        check_in_date = datetime.datetime.strptime(input("Enter the check-in date (YYYY-MM-DD): "), "%Y-%m-%d")
        check_out_date = datetime.datetime.strptime(input("Enter the check-out date (YYYY-MM-DD): "), "%Y-%m-%d")
        hotel.check_in(room_no, guest_name, check_in_date, check_out_date)
        self.view_itineraries(None, hotel)

    def view_itineraries(self, user, hotel=None):
        if not hotel:
            hotel = self.hotels[0]  # Default to the first hotel
        print(f"\nItineraries for {hotel.name}:")
        for itinerary in hotel.itineraries:
            print(f"{itinerary.activity} - {itinerary.time} - ${itinerary.price}")
        self.book_itinerary(user, hotel)

    def book_itinerary(self, user, hotel):
        selected_activities = []
        total_cost = 0
        while True:
            activity = input("Enter an activity to book (or 'done' to finish): ")
            if activity.lower() == "done":
                break
            for itinerary in hotel.itineraries:
                if itinerary.activity.lower() == activity.lower():
                    selected_activities.append(itinerary)
                    total_cost += itinerary.price
                    print(f"Added {itinerary.activity} - {itinerary.time} - ${itinerary.price}")
                    break
            else:
                print("Invalid activity. Please try again.")

        print(f"\nTotal Cost: ${total_cost:.2f}")
        print("Payment Options:")
        print("1. Mobile Money")
        print("2. PayPal")
        print("3. Bank Account")
        payment_method = input("Enter your payment method (1-3): ")
        print("Booking confirmed. Thank you for using our Hotel Management System!")

if __name__ == "__main__":
    hms = HotelManagementSystem()

    while True:
        print("\nWelcome to the Hotel Management System!")
        print("1. Login")
        print("2. Signup")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            hms.login()
        elif choice == "2":
            hms.signup()
        elif choice == "3":
            print("Exiting the Hotel Management System...")
            break
        else:
            print("Invalid choice. Please try again.")
