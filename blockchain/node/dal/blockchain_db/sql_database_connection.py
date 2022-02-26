from psycopg2 import connect
from psycopg2.extras import RealDictCursor


class DatabaseConnection:
    def __init__(self):
        self.conn = None
        self.cursor = None

        try:
            self.conn = connect(host='localhost',
                                database='blockchain', 
                                user='postgres',
                                password='wrongPassword',
                                cursor_factory=RealDictCursor)
            self.cursor = self.conn.cursor()

        except Exception as error:
            print(f"Connection Failed. The error is: {error}")
