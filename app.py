from flask import Flask, request, render_template, jsonify
import jwt
import json
import datetime
#token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoidGhvbXhzbmd1eWVuIn0.ZC6kmDkWC2YEcD7aVRORiRCifJ9t5el_91Mohj9kyw8

'''
curl -X GET http://127.0.0.1:5000/dashboard \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoidGhvbXhzbmd1eWVuIn0.ZC6kmDkWC2YEcD7aVRORiRCifJ9t5el_91Mohj9kyw8"
app = Flask(__name__)
'''

app.config['SECRET_KEY'] = 'super_secret_key' 

USER = {
  "username": "thomxsnguyen",
  "password": "thomas123"
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
    return jsonify({"error": "header is missing"}), 401
  
  try:
    token = auth_header.split(" ")[1]
  except Exception as e:
    return jsonify({'error': str(e)})
  
  try:
    data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
    user = data['user']
    return jsonify({'message': f'Welcome {user}!'}), 200
  except Exception as e:
    return jsonify({"error": str(e)}), 401





if __name__ == "__main__":
  app.run(debug=True, port=5000)