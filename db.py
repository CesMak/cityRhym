import sqlite3


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
                postcode INTEGER,
                city TEXT
                )
            ''')
        elif table_name == 'poem':
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS poem (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    postcode INTEGER,
                    poem TEXT
                )
            ''')
    conn.commit()
    return conn

def insert_address(conn, first_name, last_name, street, house_number, postcode, city):
    """Inserts a new address into the database, checking for duplicates."""
    cursor = conn.cursor()

    # Check if the address already exists
    cursor.execute('''
        SELECT * FROM addresses
        WHERE first_name = ? AND last_name = ? AND street = ? AND house_number = ? AND postcode = ? AND city = ?
    ''', (first_name, last_name, street, house_number, postcode, city))

    existing_address = cursor.fetchone()

    if existing_address:
        print("Address already exists.")
    else:
        cursor.execute('''
            INSERT INTO addresses (first_name, last_name, street, house_number, postcode, city)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (first_name, last_name, street, house_number, postcode, city))
        conn.commit()
        print("Address inserted successfully.")

def check_if_poem_exists(conn, postcode):
    """Checks if a poem exists for the given postcode."""
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM poem WHERE postcode = ?", (postcode,))
    existing_poem = cursor.fetchone()

    if existing_poem:
        return True
    else:
        return False

def get_poem_by_postcode(conn, postcode):
    """Retrieves the poem for the given postcode."""
    cursor = conn.cursor()

    cursor.execute("SELECT poem_text FROM poem WHERE postcode = ?", (postcode,))
    result = cursor.fetchone()

    if result:
        return result[0]  # Return the poem text
    else:
        return None  # Indicate no poem found

def insert_poem(conn, postcode, poem):
    """Inserts a new poem into the database"""
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO poem (postcode, poem)
        VALUES (?, ?)
    ''', (postcode, poem))
    conn.commit()

def print_table_entries(conn, db_name):
    """Prints all entries from a database"""
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM {db_name}")
    rows = cursor.fetchall()

    print("\n"+db_name)
    for row in rows:
        print(", ".join(str(value) for value in row))
    print("")