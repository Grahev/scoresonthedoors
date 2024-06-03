import psycopg2
from django.db import connection

# List of tables to keep
tables_to_keep = [
    'auth_user',
    'auth_user_groups',
    'auth_user_user_permissions',
    # Add other user-related tables if any
]

# Connect to the database
conn = connection.cursor()

# Fetch all table names
conn.execute("""
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public'
""")

tables = conn.fetchall()

# Generate DROP TABLE statements for tables not in the keep list
drop_statements = []
for table in tables:
    table_name = table[0]
    if table_name not in tables_to_keep:
        drop_statements.append(f'DROP TABLE IF EXISTS "{table_name}" CASCADE;')

# Execute drop statements
for statement in drop_statements:
    conn.execute(statement)

# Close the connection
conn.close()
