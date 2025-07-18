import sqlite3

# Create or connect to a SQLite database file
conn = sqlite3.connect('database/banking.db')

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Read and execute SQL statements from a file
with open('sql/schema.sql', 'r') as init_sql_file:
    init_sql = init_sql_file.read()

cursor.executescript(init_sql)
conn.commit()
# Close the database connection
conn.close()
print("Database initialized successfully.")

