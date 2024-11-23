# Importing necessary libraries for MySQL database connection and date manipulation
import mysql.connector
from datetime import datetime

# Establishing a connection to the MySQL database 'smart_stay' with user credentials
conn = mysql.connector.connect(
    host="localhost",  # Host where MySQL is running
    user="root",  # MySQL user
    password="",  # Password for MySQL user (empty for now)
    database="smart_stay"  # The database being accessed
)
cursor = conn.cursor()  # Creating a cursor object to interact with the database

# Function to fetch user data for login by validating the provided username and password
def get_user(username, password):
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    return cursor.fetchone()  # Returns the user data if found
# Function to check if a username already exists in the database for registration
def get_user_by_username(username):
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    return cursor.fetchone()  # Returns the user data if the username is taken

# Function to register a new user with the provided username and password
def register_user(username, password):
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
    conn.commit()  # Commit the transaction to the database
    print(f"User {username} registered successfully!")  # Confirmation message

# Function to fetch all hotels available in the database
def get_hotels():
    cursor.execute("SELECT * FROM hotels")
    return cursor.fetchall()  # Returns a list of all hotels

# Function to fetch rooms of a specific hotel by its ID
def get_rooms(hotel_id):
    cursor.execute("SELECT * FROM rooms WHERE hotel_id = %s", (hotel_id,))
    return cursor.fetchall()  # Returns a list of rooms for the given hotel

# Function to fetch amenities available for a specific room by its ID
def get_amenities(room_id):
    cursor.execute("SELECT * FROM amenities WHERE room_id = %s", (room_id,))
    return cursor.fetchall()  # Returns a list of amenities for the given room

# Function to book a room for a user and store booking information in the database
def book_room(user_id, room_id, check_in, check_out, total_price):
    cursor.execute("""
        INSERT INTO bookings (user_id, room_id, check_in, check_out, total_price, status) 
        VALUES (%s, %s, %s, %s, %s, 'Confirmed')
    """, (user_id, room_id, check_in, check_out, total_price))
    conn.commit()  # Commit the transaction to the database
    return cursor.lastrowid  # Returns the booking ID for the new booking

# Function to add an itinerary for a given booking, specifying the day, meal, activity, and cost
def add_itinerary(booking_id, day, meal, activity, cost):
    cursor.execute("""
        INSERT INTO itinerary (booking_id, day, meal, activity, cost) 
        VALUES (%s, %s, %s, %s, %s)
    """, (booking_id, day, meal, activity, cost))
    conn.commit()  # Commit the transaction to the database
    
# Function to generate and display an invoice with booking and itinerary details
def generate_invoice(user, selected_hotel, selected_room, check_in, check_out, total_price, payment_method, booking_id):
    print("\n--- Invoice ---")
    print(f"Customer: {user[1]}")
    print(f"Hotel: {selected_hotel[1]} - {selected_hotel[2]}")
    print(f"Room: {selected_room[2]}")
    print(f"Check-in: {check_in}")
    print(f"Check-out: {check_out}")
    print(f"Total Price: ${total_price}")
    print(f"Payment Method: {payment_method}")
    
    # Fetch itinerary details for the booking and display them
    cursor.execute("SELECT * FROM itinerary WHERE booking_id = %s", (booking_id,))
    itineraries = cursor.fetchall()
    print("\n--- Itinerary ---")
    for itinerary in itineraries:
        print(f"Day {itinerary[2]}: Meal: {itinerary[3]}, Activity: {itinerary[4]}, Cost: ${itinerary[5]}")
    
    print("------------------")

# Function to return the price for selected amenities
def get_amenity_price(amenity_name):
    # For simplicity, assuming fixed prices for the amenities
    prices = {"Gym": 100, "Private Pool": 200, "Gaming Area": 50}
    return prices.get(amenity_name, 0)

# Function to process the payment based on the selected option
def process_payment(option):
    if option == 1:
        card_number = input("Enter your card number: ")
        card_pin = input("Enter your card PIN: ")
        if len(card_number) == 16 and len(card_pin) == 4:
            print("Processing payment...")
            print("Payment Successful!")
        else:
            print("Invalid card details. Please try again.")
    elif option == 2:
        paypal_email = input("Enter your PayPal email: ")
        print("Processing payment via PayPal...")
        print("Payment Successful!")

# Main function to simulate the booking process and interact with the user
def main():
    print("Welcome to Smart Stay Hotels System!")
    
    # Main loop for the system's menu
    while True:
        print("\nMenu:")
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        
        choice = input("Select an option: ")
        
        if choice == "1":
            # Login process: Validate user credentials
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            
            user = get_user(username, password)
            if user:
                print(f"Welcome, {username}! Let's book your perfect stay.")
                
                hotels = get_hotels()
                print("Available Locations:")
                for idx, hotel in enumerate(hotels, 1):
                    print(f"{idx}. {hotel[1]}, {hotel[2]}")
                hotel_choice = int(input("Select a hotel location: "))
                selected_hotel = hotels[hotel_choice - 1]
                
                rooms = get_rooms(selected_hotel[0])
                print("Room Categories:")
                for idx, room in enumerate(rooms, 1):
                    print(f"{idx}. {room[2]} (Price: ${room[4]})")
                room_choice = int(input("Choose a room category (1/2): "))
                selected_room = rooms[room_choice - 1]
                
                amenities = get_amenities(selected_room[0])
                print("Available Amenities:")
                for amenity in amenities:
                    print(f"- {amenity[1]}: ${amenity[2]}")
                amenities_choice = input("Select amenities (comma-separated): ").split(",")
                
                check_in = input("Enter check-in date (YYYY-MM-DD): ")
                check_out = input("Enter check-out date (YYYY-MM-DD): ")
                
                # Calculate total price
                total_price = selected_room[4] * (datetime.strptime(check_out, "%Y-%m-%d") - datetime.strptime(check_in, "%Y-%m-%d")).days
                total_price += sum([get_amenity_price(amenity.strip()) for amenity in amenities_choice])
                
                print(f"Confirm booking for Room {selected_room[0]} at ${total_price} for {total_price / selected_room[4]} nights? (yes/no): ", end="")
                confirm = input().lower()
                
                if confirm == 'yes':
                    # Book the room and get the booking ID
                    booking_id = book_room(user[0], selected_room[0], check_in, check_out, total_price)
                    print(f"Room {selected_room[0]} booked successfully!")
                    
                    # Generate itinerary for the booking
                    for day in range(1, (datetime.strptime(check_out, "%Y-%m-%d") - datetime.strptime(check_in, "%Y-%m-%d")).days + 1):
                        add_itinerary(booking_id, day, "Breakfast", 10, 50)
                    print("Itinerary booked successfully!")
                    
                    # Payment options and processing
                    print("Payment Options:\n1. Visa/Mastercard\n2. PayPal")
                    payment_option = int(input("Select payment option (1/2): "))
                    payment_method = "Visa/Mastercard" if payment_option == 1 else "PayPal"
                    process_payment(payment_option)
                    
                    # Generate and print the invoice with itinerary details
                    generate_invoice(user, selected_hotel, selected_room, check_in, check_out, total_price, payment_method, booking_id)
            else:
                print("Invalid username or password")
        
        elif choice == "2":
            # Registration process
            username = input("Enter your desired username: ")
            if get_user_by_username(username):
                print("Username already exists! Please choose another.")
                continue
            password = input("Enter your password: ")
            register_user(username, password)
        
        elif choice == "3":
            print("Goodbye!")
            break

# Run the main function if this script is executed
if __name__ == "__main__":
    main()