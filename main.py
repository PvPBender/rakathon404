from db.database import connect


if __name__ == "__main__":
    # Connect to the database
    connection = connect()
    
    # Check if the connection was successful
    if connection:
        # Perform database operations here
        pass  # Replace with your code

        # Close the connection when done
        connection.close()