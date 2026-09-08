# Imports
import mysql.connector
from config import db_config

# Fucntion to connect to 
def get_db_connection():
    try:
        print("Attempting to connect to MySQL...")

        # Connect to db
        db = mysql.connector.connect(**db_config)
        print("Connection object created.")

        if db.is_connected():
            print("Connection successful!")
        else:
            print("Connection failed")
            
        # Create cursor
        cursor = db.cursor()
        
    # Return nothing and display error 
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None, None
    
    # Return connection + cursor
    return db, cursor
