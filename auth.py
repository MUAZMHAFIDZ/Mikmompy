from db import create_connection

def fetchlogin(username, password):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        cursor.close()
        connection.close()
        return user
    return None

def update_myuser(id, username, password):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "UPDATE users SET username = %s, password = %s WHERE id = %s"
            cursor.execute(query, (username, password, id))
            connection.commit()
            if cursor.rowcount > 0:
                print("User updated successfully.")
            else:
                print("No user found with the given ID.")
            cursor.close()
        except Exception as e:
            print(f"Error occurred: {e}")
        finally:
            connection.close()
    else:
        print("Failed to connect to the database.")

def save_mikrotik(ip, username, pw, hot, dns):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        query = "INSERT INTO mikrotik (ip, username, password, hotspot_name, dns_name) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (ip, username, pw, hot, dns))
        connection.commit()
        cursor.close()
        connection.close()

def delete_mikrotik(id):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        query = "DELETE FROM mikrotik WHERE id = %s"
        cursor.execute(query, (id))
        connection.commit()
        cursor.close()
        connection.close()