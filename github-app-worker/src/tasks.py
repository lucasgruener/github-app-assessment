import requests
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_SERVICE_URL = os.getenv('DATABASE_SERVICE_URL')
GITHUB_API_URL = os.getenv('GITHUB_API_URL')


def update_all_users_data_task():
    print("Updating data for all users...")
    try:
        # Fetch a list of all users from the database service's API endpoint
        get_users_url = f'{DATABASE_SERVICE_URL}/users'
        response = requests.get(get_users_url)

        if response.status_code == 200:
            users = response.json()

            for user in users:
                username = user.get('username')
                fetch_github_data(username) 
            print('Task finished, next update in 1 hour...')
        else:
            print("Failed to fetch user list from the database service")
            print(f"Database API response: {response.status_code}, {response.content}")

    except Exception as e:
        print(f"Error: {str(e)}")

def fetch_github_data(username):
    github_api_url = f'{GITHUB_API_URL}/{username}/repos'

    try:
        response = requests.get(github_api_url)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()

            # Prepare data to send to the database service
            user_data = {
                "username": username,
                "repositories": data[:5]
            }

            # Send a POST request to the database service to update data
            db_response = requests.post(f"{DATABASE_SERVICE_URL}/update_user_data", json=user_data)

            if db_response.status_code == 200:
                # Data updated successfully
                print(f"Data updated for user: {username}")
            else:
                print(f"Failed to update data for user: {username}")
                print(f"Database API response: {db_response.status_code}, {db_response.content}")
        else:
            print(f"Failed to fetch data from GitHub for user: {username}")
            print(f"GitHub API response: {response.status_code}, {response.content}")
    except Exception as e:
        print(f"Error: {str(e)}")

