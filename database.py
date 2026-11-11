import sqlite3

def get_connection(db_name):
        try:
                return sqlite3.connect(db_name)
        except Exception as e:
                print(f"Error: {e}")
                raise

def create_table_recipient(connection):
        query="""
        CREATE TABLE IF NOT EXISTS recipient (
            id INTEGER PRIMARY KEY,
            email TEXT UNIQUE
        )
        """

        try:
                with connection:
                        connection.execute(query)
                print("Table recipient created!")
        except Exception as e:
                print(f"Error: {e}")

def create_table_sender(connection):
        query="""
        CREATE TABLE IF NOT EXISTS sender (
            id INTEGER PRIMARY KEY,
            email TEXT UNIQUE
        )
        """

        try:
                with connection:
                        connection.execute(query)
                print("Table sender created!")
        except Exception as e:
                print(f"Error: {e}")


def main():
        connection = get_connection("testpostalservice.db")
        try:
                create_table_sender(connection)
                create_table_recipient(connection)

        finally:
                connection.close()
if __name__ == "__main__":
        main()