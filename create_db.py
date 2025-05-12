import sqlite3

conn = sqlite3.connect('database.db')

# Create users table
conn.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);
''')

# Create vehicles table
conn.execute('''
    CREATE TABLE IF NOT EXISTS vehicles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        model TEXT NOT NULL,
        year INTEGER NOT NULL,
        brand TEXT NOT NULL,
        reg_number TEXT NOT NULL,
        image_url TEXT NOT NULL
    );
''')



# Optional: Insert sample data
conn.execute("INSERT OR IGNORE INTO users (username, email, password) VALUES ('admin', 'admin@dektra.com', 'adminpass');")

conn.execute("INSERT OR IGNORE INTO vehicles (name, model, year, image) VALUES \
('Tesla Model S', 'Electric', '2022', 'images/car1.png'), \
('Ford Mustang', 'GT', '2021', 'images/car2.png'), \
('Yamaha FZ', 'Motorbike', '2023', 'images/bike.png');")

conn.commit()
conn.close()
print("Database created with users and vehicles.")
