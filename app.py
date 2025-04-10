from flask import Flask, request, jsonify
import jwt
from flask_sqlalchemy import SQLAlchemy
import json
import datetime

#token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoidGhvbXhzbmd1eWVuIn0.ZC6kmDkWC2YEcD7aVRORiRCifJ9t5el_91Mohj9kyw8
'''
curl -X GET http://127.0.0.1:5000/dashboard \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoidGhvbXhzbmd1eWVuIn0.ZC6kmDkWC2YEcD7aVRORiRCifJ9t5el_91Mohj9kyw8"
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super_secret_key' 

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

USER = {
  "username": "thomxsnguyen",
  "password": "thomas123"
}

class Post(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(50), nullable=False)
  description = db.Column(db.String(150), nullable=False)

  def to_dict(self):
    return {
      "id": self.id, "title": self.title, "description": self.description
    }
  

@app.route('/login', methods=['POST'])
def login():
  data = request.get_json()
  username = data.get('username')
  password = data.get('password')

  if username == USER['username'] and password == USER['password']:
    token = jwt.encode({'user': username}, app.config['SECRET_KEY'], algorithm="HS256")
    return jsonify({"token": token}), 200
  
  return jsonify({"error": "Invalid credentials"}), 401

@app.route('/dashboard', methods=['GET'])
def dashboard():
  auth_header = request.headers.get('Authorization')

  if not auth_header:
    return jsonify({"message": "header is missing"}), 401
  
  try:
    token = auth_header.split(" ")[1]
  except Exception as e:
    return jsonify({'message': str(e)})
  
  try:
    data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
    user = data['user']
    return jsonify({'message': f'Welcome {user}!'}), 200
  except Exception as e:
    return jsonify({"message": str(e)}), 401


@app.route('/todos', methods=['POST'])
def create_post():
  try:
    auth_header = request.headers.get('Authorization')
    token = auth_header.split(" ")[1]
    auth = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
  except Exception as e:
    return jsonify({'message': str(e)}), 401
  
  if not auth:
    return jsonify({'error': "Unauthorized"})
  
  data = request.get_json()
  title = data.get('title')
  description = data.get('description')
 
  post = Post(title=title, description=description)
  db.session.add(post)
  db.session.commit()

  return jsonify({'message': 'post created'}), 200

@app.route('/todos/<int:post_id>', methods=['POSTS'])
def update_post(post_id):
  try:
    auth_header = request.headers.get('Authorization')
    token = auth_header.split(" ")[1]
    auth = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
  except Exception as e:
    return jsonify({'message': str(e)}), 401
  
  if not auth:
    return jsonify({'error': "Unauthorized"})
  
  data = request.json()
  post = Post.query.get(post_id)

  post.title = data.get("title")
  post.description = data.get("description")

  db.session.commit()

  return jsonify({'status': 'recieved'}), 200
  

# @app.route('/todos', methods=['GET'])
# def view_all():
#   try:
#     auth_header = request.headers.get('Authorization')
#     token = auth_header.split(" ")[1]
#     auth = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
#   except Exception as e:
#     return jsonify({'message': str(e)}), 401
  
#   if not auth:
#     return jsonify({'error': "Unauthorized"})
  
#   posts = [p.to_dict() for p in Post.query.all()]
#   return jsonify({"posts": posts})

# @app.route('/todos/<int:post_id>', methods=['GET'])
# def view_post(post_id):
#   try:
#     auth_header = request.headers.get('Authorization')
#     token = auth_header.split(" ")[1]
#     auth = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
#   except Exception as e:
#     return jsonify({'message': str(e)}), 401
  
#   if not auth:
#     return jsonify({'error': "Unauthorized"})
  
#   post = Post.query.get(post_id)
#   return jsonify({'post': post.to_dict()}), 200

@app.route('/todos/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
  try:
    auth_header = request.headers.get('Authorization')
    token = auth_header.split(" ")[1]
    auth = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
  except Exception as e:
    return jsonify({'message': str(e)}), 401
  
  if not auth:
    return jsonify({'error': "Unauthorized"})
  
  post = Post.querey.get(post_id)
  db.session.delete(post)
  db.session.commit()
  return jsonify({'message': 'post deleted'}), 200

@app.route('/todos', methods=['GET'])
def get_todos():
  page = request.args.get('page', default=1, type=int)
  limit = request.args.get('limit', default=10, type=int)

  offset = (page - 1) * limit

  posts = Post.query.offset(offset).limit(limit).all()
  total = Post.query.count()

  return jsonify({'posts': [p.to_dict() for p in posts ], 'total': total, 'page': page, 'limit': limit}), 200

if __name__ == "__main__":
  with app.app_context():
    db.create_all()
  app.run(debug=True, port=5000)

  
