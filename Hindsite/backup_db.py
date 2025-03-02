import sqlite3

def export_db_to_txt(db_name, txt_filename):
    try:
        # Connect to the database
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Fetch all tables in the database
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        with open(txt_filename, "w", encoding="utf-8") as file:
            for table in tables:
                table_name = table[0]
                file.write(f"\n===== TABLE: {table_name} =====\n")

                # Fetch table data
                cursor.execute(f"SELECT * FROM {table_name}")
                rows = cursor.fetchall()

                # Fetch column names
                col_names = [description[0] for description in cursor.description]
                file.write(" | ".join(col_names) + "\n")  # Write column headers
                file.write("-" * 50 + "\n")

                # Write each row of data
                for row in rows:
                    file.write(" | ".join(str(value) for value in row) + "\n")
                
                file.write("\n")

        print(f"Database successfully exported to {txt_filename}")

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

    finally:
        if conn:
            conn.close()

# Example Usage
db_name = "small_db.db"  # Change to your database file name
txt_filename = "database_backup.txt"  # Change to desired output file name
export_db_to_txt(db_name, txt_filename)