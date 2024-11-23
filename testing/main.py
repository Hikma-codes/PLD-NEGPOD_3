from modules.user import login, signup
from modules.models import Hotel
from modules.payment import initiate_payment

class HotelManagementSystem:
    def __init__(self):
        self.hotels = Hotel.get_all_hotels()

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

    def profile(self, user):
        print(f"\nProfile Information:")
        print(f"Name: {user.name}")
        print(f"Email: {user.email}")
        input("Press Enter to continue...")

    def select_hotel(self, user):
        print("\nSelect a hotel:")
        for i, hotel in enumerate(self.hotels):
            print(f"{i+1}. {hotel.name} - {hotel.location}")
        choice = int(input("Enter your choice: "))
        if 1 <= choice <= len(self.hotels):
            self.view_hotel(self.hotels[choice-1])
        else:
            print("Invalid choice. Please try again.")

    def view_hotel(self, hotel):
        print(f"\nHotel: {hotel.name}")
        print(f"Location: {hotel.location}")
        print(f"Rooms: {hotel.num_rooms}")
        print(f"Amenities: {', '.join(hotel.amenities)}")
        available_rooms = [room for room in hotel.rooms if not room['occupied']]
        print("\nAvailable Rooms:")
        for room in available_rooms:
            print(f"Room {room['room_no']}")
        self.book_room(hotel)

    def book_room(self, hotel):
        room_no = int(input("Enter the room number to book: "))
        guest_name = input("Enter the guest name: ")
        if hotel.check_in_guest(room_no, guest_name):
            print(f"Room {room_no} successfully booked for {guest_name}.")
            self.view_itineraries(None, hotel)
        else:
            print("Booking failed. Please try another room or check availability.")

    def view_itineraries(self, user, hotel=None):
        if hotel is None:
            print("Select a hotel to view itineraries:")
            for i, h in enumerate(self.hotels):
                print(f"{i+1}. {h.name} - {h.location}")
            choice = int(input("Enter your choice: "))
            if 1 <= choice <= len(self.hotels):
                hotel = self.hotels[choice-1]
            else:
                print("Invalid choice.")
                return

        print(f"\nItineraries for {hotel.name}:")
        for itinerary in hotel.itineraries:
            print(f"{itinerary.activity} - {itinerary.time} - ${itinerary.price}")
        self.book_itinerary(user, hotel, itinerary)

    def book_itinerary(self, user, hotel, itenerary):
        selected_activities = []
        total_cost = 0  # Initialize total cost as 0
        while True:
            # Prompt user for activity input
            activity = input("Enter an activity to book (or 'done' to finish): ")

            if activity.lower() == "done":
                break

            # Search for the activity in the hotel's itineraries
            activity_found = False  # Flag to check if the activity was found
            for itinerary in itenerary:
                # Make comparison case insensitive by converting both to lowercase
                if itinerary.activity.lower() == activity.lower():
                    selected_activities.append(itinerary)
                    print(f"DEBUG: Adding {itinerary.activity} - Price: {itinerary.price}")
                    total_cost += itinerary.price  # Add the activity's price to total cost
                    print(f"Added {itinerary.activity} - {itinerary.time} - ${itinerary.price}")
                    activity_found = True
                    break
            
            # If activity is not found, inform the user
            if not activity_found:
                print(f"Activity '{activity}' not found. Please try again.")

        # Debugging: Print total cost for selected activities
        print(f"\nTotal cost for selected activities: RWF 30000")

        # Now initiate payment
        print(f"\nTotal Cost: RWF 30000")
        phone_number = input("Enter your mobile number: ")
        payment_response = initiate_payment(phone_number, "30000")
        if payment_response.get('status') == 'success':
            print("Payment successful. Your itinerary is booked!")
        else:
            print("Payment failed. Please try again.")

if __name__ == "__main__":
    print("Welcome to Hotel Management System")
    print("1. Login")
    print("2. Signup")
    choice = input("Enter your choice (1-2): ")

    if choice == "1":
        user = login()
        if user:
            system = HotelManagementSystem()
            system.home_page(user)
    elif choice == "2":
        user = signup()
        if user:
            system = HotelManagementSystem()
            system.home_page(user)
