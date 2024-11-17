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
                zipcode INTEGER,
                city TEXT
                )
            ''')
        elif table_name == 'poem':
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS poem (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    zipcode INTEGER,
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
        cursor.execute("SELECT poem_text FROM poem WHERE zipcode = ?", (zipcode,))
        result = cursor.fetchone()
        if result:
            return result[0]  # Return the poem text
        else:
            return None  # Indicate no poem found
    except Exception as e:
        return None

def insert_poem(conn, zipcode, poem):
    """Inserts a new poem into the database"""
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO poem (zipcode, poem)
        VALUES (?, ?)
    ''', (zipcode, poem))
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