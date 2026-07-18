import os
import sqlite3

def init_db():
    db_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    os.makedirs(db_dir, exist_ok=True)
    db_path = os.path.join(db_dir, 'sales_data.db')
    
    schema_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'schema', 'create_tables.sql')
    
    print(f"Connecting to database at: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    print(f"Reading schema from: {schema_path}")
    with open(schema_path, 'r') as f:
        sql_script = f.read()
        
    print("Executing table creation DDL...")
    cursor.executescript(sql_script)
    conn.commit()
    
    # Verify tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("\nSuccessfully created tables:")
    for table in tables:
        print(f" - {table[0]}")
        
    conn.close()
    print("\nDatabase initialization complete!")

if __name__ == '__main__':
    init_db()
