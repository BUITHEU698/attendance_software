import pyodbc

# Set up the connection string
# Replace 'your_access_database.accdb' with the path to your Access database file
# If your Access database has a password, add 'PWD=password' to the connection string
conn_str = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=database.accdb;'

# Establish the connection
conn = pyodbc.connect(conn_str)

# Create a cursor from the connection
cursor = conn.cursor()

# Example: Execute a query
cursor.execute('SELECT * FROM 勤怠;')

# Fetch and print the results
for row in cursor.fetchall():
    print(row)

# Close the cursor and connection
cursor.close()
conn.close()
