import sqlite3
    
def create_database():
    conn = sqlite3.connect('cisco.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cisco (
        no INTEGER PRIMARY KEY AUTOINCREMENT,
        Sw_Ip TEXT NOT NULL,
        Cicco TEXT NOT NULL,
        oid TEXT NOT NULL
    )
    ''')

    ip_addresses = [
        ('127.0.0.5', 'Cisco3750', '1.3.6.1.4.1.9.9.13.1.3.1.3'),
        ('127.0.0.5', 'Cisco3750', '1.3.6.1.4.1.9.9.13.1.3.1.3'),
        ('127.0.0.6', 'Cisco3750', '1.3.6.1.4.1.9.9.13.1.3.1.3'),
        ('127.0.0.7', 'Cisco3750', '1.3.6.1.4.1.9.9.13.1.3.1.3'),
        ('127.0.0.8', 'Cisco3750', '1.3.6.1.4.1.9.9.13.1.3.1.3'),
        ('127.0.0.9', 'Cisco3750', '1.3.6.1.4.1.9.9.13.1.3.1.3'),
        ('127.0.0.10', 'Cisco3750', '1.3.6.1.4.1.9.9.13.1.3.1.3'),
        ('127.0.0.11', 'Cisco3750', '1.3.6.1.4.1.9.9.13.1.3.1.3'),
        ('127.0.0.12', 'Cisco3750', '1.3.6.1.4.1.9.9.13.1.3.1.3'),
        ('127.0.0.13', 'Cisco3750', '1.3.6.1.4.1.9.9.13.1.3.1.3'),
        ('127.0.0.14', 'Cisco3750', '1.3.6.1.4.1.9.9.13.1.3.1.3'),
        ('127.0.0.15', 'Cisco3750', '1.3.6.1.4.1.9.9.13.1.3.1.3'),
    ]
    
    cursor.execute("SELECT COUNT(*) FROM cisco")
    row_count = cursor.fetchone()[0]

    if row_count == 0:
        cursor.executemany('INSERT INTO cisco (Sw_Ip, Cicco, oid) VALUES (?,?,?)', ip_addresses)
        conn.commit()
        print("Database, table, and IP addresses have been added successfully!")
    else:
        print("Data already exists in the table.")

    conn.close()

def retrieve_data():
    conn = sqlite3.connect('cisco.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM cisco")
    data = cursor.fetchall()

    if data:
        print("Retrieved data from the database:")
        for row in data:
            print(row)
    else:
        print("No data found in the database.")

    conn.close()

if __name__ == '__main__':
    create_database()
    retrieve_data()

