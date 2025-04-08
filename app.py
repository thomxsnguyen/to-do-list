from flask import Flask, request, render_template, jsonify
import jwt
import json
import datetime
#token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoidGhvbXhzbmd1eWVuIn0.ZC6kmDkWC2YEcD7aVRORiRCifJ9t5el_91Mohj9kyw8
app = Flask(__name__)
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
    return jsonify({"token": token})
  return jsonify({"error": "Invalid credentials"}), 401


if __name__ == "__main__":
  app.run(debug=True, port=5000)