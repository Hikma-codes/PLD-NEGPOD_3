# Importing necessary libraries for MySQL database connection and date manipulation
import mysql.connector
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
