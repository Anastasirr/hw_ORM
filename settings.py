import os

from dotenv import load_dotenv
load_dotenv()

db_user_name = os.getenv('DB_USER_N')
db_pass_user = os.getenv('DB_PASS_USER')
db_name = os.getenv('DB_NAME')
