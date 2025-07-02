import mariadb
from dotenv import load_dotenv
import os
load_dotenv()

def get_connection():
    try:
        connection=mariadb.connect(
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            port=3306

        )
    except Exception as e:
        print(e)
    return connection