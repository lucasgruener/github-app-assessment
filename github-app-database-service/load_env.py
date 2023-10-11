from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access the environment variables
DATABASE_URL = os.getenv('DATABASE_URL')

# Optionally, set the environment variables for the current session
os.environ['DATABASE_URL'] = DATABASE_URL