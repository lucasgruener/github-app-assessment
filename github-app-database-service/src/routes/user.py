from flask import Blueprint, request, jsonify
from models.models import db, User, Repository

user_routes = Blueprint('user_routes', __name__)


# Main route 

# List of desired repository parameters
desired_repo_params = ["name", "html_url", "description", "language"]
@user_routes.route('/update_user_data', methods=['POST'])
def update_user_data():
    data = request.json
    username = data.get('username')
    repositories = data.get('repositories')

    if not username:
        return jsonify({"error": "Invalid request data"}), 400

    # Find or create a user in the database and determine its status
    user = User.query.filter_by(username=username).first()
    
    user_status = "new" if not user else "existing"
    
    if not user:
        user = User(username=username)
        db.session.add(user)
   
    # Update or create repositories for the user
    for repo_data in repositories:
        repository = Repository.query.filter_by(name=repo_data['name'], user_id=user.id).first()
        if repository:
            # If the repository exists, update it
            for param in desired_repo_params:
                setattr(repository, param, repo_data.get(param))
        else:
            # If the repository doesn't exist, create a new entry
            new_repository = Repository(
                user_id=user.id,
                **{param: repo_data.get(param) for param in desired_repo_params}
            )
            db.session.add(new_repository)

    # Commit the changes to the database
    db.session.commit()
    
    # Prepare the response data with desired repository parameters only
    response_data = {
        "message": "Data updated successfully",
        "user_status": user_status,
        "repositories": [
            {param: repo_data.get(param) for param in desired_repo_params}
            for repo_data in repositories
        ]
    }

    return jsonify(response_data), 200


#CRUD user_routes for users

@user_routes.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = [{"id": user.id, "username": user.username} for user in users]
    return jsonify(user_list)

@user_routes.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"id": user.id, "username": user.username})

@user_routes.route('/users', methods=['POST'])
def create_user():
    username = request.json.get('username')
    if not username:
        return jsonify({"error": "Username is required"}), 400

    user = User(username=username)
    db.session.add(user)
    db.session.commit()
    return jsonify({"id": user.id, "username": user.username}), 201


@user_routes.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404

    new_username = request.json.get('username')
    if not new_username:
        return jsonify({"error": "Username is required"}), 400

    user.username = new_username
    db.session.commit()
    return jsonify({"id": user.id, "username": user.username})

@user_routes.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"}), 204


