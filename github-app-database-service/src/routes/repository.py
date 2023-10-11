from flask import Blueprint, request, jsonify
from models.models import db, User, Repository

repository_routes = Blueprint('repository_routes', __name__)

@repository_routes.route('/repositories', methods=['GET'])
def get_repositories():
    repositories = Repository.query.all()
    repo_list = [
        {
            "id": repo.id,
            "name": repo.name,
            "html_url": repo.html_url,
            "description": repo.description,
            "language": repo.language,
            "user_id": repo.user_id
        }
        for repo in repositories
    ]
    return jsonify(repo_list)

@repository_routes.route('/repositories/<int:repo_id>', methods=['GET'])
def get_repository(repo_id):
    repository = Repository.query.get(repo_id)
    if repository is None:
        return jsonify({"error": "Repository not found"}), 404
    return jsonify({
        "id": repository.id,
        "name": repository.name,
        "html_url": repository.html_url,
        "description": repository.description,
        "language": repository.language,
        "user_id": repository.user_id
    })

@repository_routes.route('/repositories', methods=['POST'])
def create_repository():
    data = request.json
    name = data.get('name')
    html_url = data.get('html_url')
    description = data.get('description')
    language = data.get('language')
    user_id = data.get('user_id')

    if not (name and html_url and user_id):
        return jsonify({"error": "Name, HTML URL, and User ID are required"}), 400

    repository = Repository(
        name=name,
        html_url=html_url,
        description=description,
        language=language,
        user_id=user_id
    )
    db.session.add(repository)
    db.session.commit()

    return jsonify({
        "id": repository.id,
        "name": repository.name,
        "html_url": repository.html_url,
        "description": repository.description,
        "language": repository.language,
        "user_id": repository.user_id
    }), 201

@repository_routes.route('/repositories/<int:repo_id>', methods=['PUT'])
def update_repository(repo_id):
    repository = Repository.query.get(repo_id)
    if repository is None:
        return jsonify({"error": "Repository not found"}), 404

    data = request.json
    name = data.get('name')
    html_url = data.get('html_url')
    description = data.get('description')
    language = data.get('language')
    user_id = data.get('user_id')

    if not (name and html_url and user_id):
        return jsonify({"error": "Name, HTML URL, and User ID are required"}), 400

    repository.name = name
    repository.html_url = html_url
    repository.description = description
    repository.language = language
    repository.user_id = user_id

    db.session.commit()

    return jsonify({
        "id": repository.id,
        "name": repository.name,
        "html_url": repository.html_url,
        "description": repository.description,
        "language": repository.language,
        "user_id": repository.user_id
    })

@repository_routes.route('/repositories/<int:repo_id>', methods=['DELETE'])
def delete_repository(repo_id):
    repository = Repository.query.get(repo_id)
    if repository is None:
        return jsonify({"error": "Repository not found"}), 404

    db.session.delete(repository)
    db.session.commit()

    return jsonify({"message": "Repository deleted"}), 204