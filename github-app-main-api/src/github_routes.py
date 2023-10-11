from flask import Blueprint, request, jsonify
import requests
from dotenv import load_dotenv
import os


load_dotenv()

github_bp = Blueprint('github_service', __name__)

DATABASE_SERVICE_URL = os.getenv('DATABASE_SERVICE_URL') 
GITHUB_API_URL = os.getenv('GITHUB_API_URL')  
@github_bp.route('/github/users/<string:username>', methods=['GET'])
def fetch_github_data(username):
    

    github_api_url = f'{GITHUB_API_URL}/{username}/repos'

    try:
        response = requests.get(github_api_url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Prepare data to send to the database service
            user_data = {
                "username": username,
                "repositories": data[:5]
            }

            # Send a POST request to the database service to update data
            db_response = requests.post(f"{DATABASE_SERVICE_URL}/update_user_data", json=user_data)

            if db_response.status_code == 200:
                # Get the user status and repositories from the database service response
                user_status = db_response.json().get("user_status")
                repositories = db_response.json().get("repositories")

                # Return the data along with the user status to the frontend
                return jsonify({
                    "message": "Data fetched and updated successfully",
                    "user_status": user_status,
                    "repositories": repositories
                }), 200
            else:
                return jsonify({"error": "Failed to update data in the database"}), 500
        else:
            return jsonify({"error": "Failed to fetch data from GitHub"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500