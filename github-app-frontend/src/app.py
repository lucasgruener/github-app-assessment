from flask import Flask, render_template, request, jsonify
import requests
from dotenv import load_dotenv
import os


load_dotenv()
app = Flask(__name__)


WEB_SERVER_URL = os.getenv('WEB_SERVER_URL')  
@app.route('/', methods=['GET', 'POST'])
def index():
    user_data = None
    is_new_user = False
    error_message = None  

    if request.method == 'POST':
        username = request.form['username']
        response = get_user_data(username)

        if response[0]:
            user_data, is_new_user = response
        else:
            error_message = f"Error: Unable to fetch user data for {username}"

    return render_template('index.html', user_data=user_data, is_new_user=is_new_user, error_message=error_message)

def get_user_data(username):
    response = requests.get(f'{WEB_SERVER_URL}/github/users/{username}')
    
    if response.status_code == 200:
        data = response.json()
        is_new_user = data.get('user_status') == 'new'
        user_data = data.get('repositories', [])
        return user_data, is_new_user
    elif response.status_code == 500:
        # Handle the case when the user doesn't exist
        return [], False
    else:
        # Handle other errors
        return None, False

PORT = os.getenv('PORT')
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT, debug= True)