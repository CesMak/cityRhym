import sqlite3
DEBUG_MESSAGE = ""

def create_connection(database_name):
    """Connects to the specified database."""
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    # Check if the table exists based on the database name
    if "address" in database_name:
        table_name = 'addresses'
    elif "poem"  in database_name:
        table_name = 'poem'
    else:
        raise ValueError("Invalid database name")

    # Check if the table exists
    cursor.execute(f'''
        SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';
    ''')
    if not cursor.fetchone():  

        # Create the table if it doesn't exist
        if table_name == 'addresses':
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS addresses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT,
                last_name TEXT,
                street TEXT,
                house_number INTEGER,
                zipcode INTEGER,
                city TEXT
                )
            ''')
        elif table_name == 'poem':
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS poem (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    zipcode INTEGER,
                    city TEXT,
                    poem TEXT
                )
            ''')
    conn.commit()
    return conn

def insert_address(conn, first_name, last_name, street, house_number, zipcode, city):
    """Inserts a new address into the database, checking for duplicates."""
    cursor = conn.cursor()

    # Check if the address already exists
    cursor.execute('''
        SELECT * FROM addresses
        WHERE first_name = ? AND last_name = ? AND street = ? AND house_number = ? AND zipcode = ? AND city = ?
    ''', (first_name, last_name, street, house_number, zipcode, city))

    existing_address = cursor.fetchone()

    if existing_address:
        print("Address already exists.")
    else:
        cursor.execute('''
            INSERT INTO addresses (first_name, last_name, street, house_number, zipcode, city)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (first_name, last_name, street, house_number, zipcode, city))
        conn.commit()
        print("Address inserted successfully.")

def update_location(conn, first_name, last_name, new_street, new_house_number, new_zipcode, new_city):
    global DEBUG_MESSAGE
    """Updates the location information for a given address."""
    cursor = conn.cursor()

    # Find the address to update
    cursor.execute('''
        UPDATE addresses
        SET street = ?, house_number = ?, zipcode = ?, city = ?
        WHERE first_name = ? AND last_name = ?
    ''', (new_street, new_house_number, new_zipcode, new_city, first_name, last_name))

    conn.commit()

    if cursor.rowcount > 0:
        DEBUG_MESSAGE = "Location updated successfully."+"\n"
        print("Location updated successfully.")
    else:
        print("No address found for the given name.")
        DEBUG_MESSAGE = "No address found for the given name."+"\n"
    return DEBUG_MESSAGE

def delete_address(conn, first_name, last_name):
    global DEBUG_MESSAGE
    """Deletes an address from the database based on first and last name."""
    cursor = conn.cursor()

    print(first_name, last_name)

    cursor.execute('''
        DELETE FROM addresses
        WHERE first_name = ?
    ''', (first_name, ))
    conn.commit()

    rows_affected = cursor.rowcount
    if rows_affected > 0:
        DEBUG_MESSAGE = first_name+","+ last_name+" deleted successfully."
    else:
        DEBUG_MESSAGE = first_name+","+ last_name+" not found. Not deleted!"
    return DEBUG_MESSAGE

def delete_poem(conn, city_or_zipcode):
    global DEBUG_MESSAGE
    print("DB:", city_or_zipcode)
    cursor = conn.cursor()

    # Try to delete by ZIP code first (assuming ZIP code is an integer)
    try:
        zipcode = int(city_or_zipcode)
        print("is a zipcode")
        cursor.execute("DELETE FROM poem WHERE zipcode = ?", (zipcode,))
        conn.commit()
        DEBUG_MESSAGE = "Poem with ZIP code "+str(zipcode)+" deleted successfully."+"\n"
        return DEBUG_MESSAGE

    except ValueError:
        # If the query_term is not an integer, try deleting by city name
        print("is a city")
        #cursor.execute("DELETE FROM poem WHERE city = ?", (city_or_zipcode,))

        cursor.execute('''
            DELETE FROM poem
            WHERE city = ?
        ''', (str(city_or_zipcode), ))

        conn.commit()
        rows_affected = cursor.rowcount
        if rows_affected > 0:
            DEBUG_MESSAGE = "Poem with city "+city_or_zipcode+"deleted successfully."+"\n"
        else:
            DEBUG_MESSAGE = "No poem found for city "+city_or_zipcode+"\n"
    return DEBUG_MESSAGE

def check_if_poem_exists(conn, zipcode):
    """Checks if a poem exists for the given zipcode."""
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM poem WHERE zipcode = ?", (zipcode,))
    existing_poem = cursor.fetchone()

    if existing_poem:
        return True
    else:
        return False

def get_poem_by_zipcode(conn, zipcode):
    """Retrieves the poem for the given zipcode."""
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT poem FROM poem WHERE zipcode = ?", (zipcode,))
        result = cursor.fetchone()
        if result:
            return result[0]  # Return the poem text
        else:
            return None  # Indicate no poem found
    except Exception as e:
        print(e)
        return None

def insert_poem(conn, zipcode, city, poem):
    """Inserts a new poem into the database"""
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO poem (zipcode, city, poem)
        VALUES (?, ?, ?)
    ''', (zipcode, city, poem))
    conn.commit()

def print_table_entries(conn, db_name):
    """Prints all entries from a database"""
    res = ""
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM {db_name}")
    rows = cursor.fetchall()

    for row in rows:
        res+=", ".join(str(value) for value in row)+"\n"
    return res