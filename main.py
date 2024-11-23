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
