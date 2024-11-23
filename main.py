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