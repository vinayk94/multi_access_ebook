from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, unset_jwt_cookies
from werkzeug.security import generate_password_hash, check_password_hash
from database import create_tables, add_user, get_user, add_session, get_active_sessions, remove_session

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Replace with your own secret key
jwt = JWTManager(app)

# Create database tables
create_tables()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.json.get('username', None)
        password = request.json.get('password', None)

        if not username or not password:
            return jsonify({"msg": "Username and password are required"}), 400

        existing_user = get_user(username)
        if existing_user:
            return jsonify({"msg": "Username already exists"}), 409

        hashed_password = generate_password_hash(password)
        add_user(username, hashed_password)

    #return jsonify({"msg": "User registered successfully"}), 201
    return render_template('register.html')

@app.route('/dashboard')
@jwt_required()
def dashboard():
    username = get_jwt_identity()
    return render_template('dashboard.html', username=username)

@app.route('/logout')
def logout():
    # Implement logout logic, e.g., clear session or token
    response = redirect(url_for('index'))
    unset_jwt_cookies(response)
    return response

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    user = get_user(username)

    if not user:
        return jsonify({"msg": "Invalid username"}), 401

    if not check_password_hash(user[2], password):
        return jsonify({"msg": "Invalid password"}), 401

    access_token = create_access_token(identity=user[0])
    add_session(user[0], request.remote_addr)
    return jsonify(access_token=access_token), 200

@app.route('/ebook')
@jwt_required()
def ebook():
    user_id = get_jwt_identity()

    active_sessions = get_active_sessions()

    if active_sessions >= 2:
        return jsonify({"msg": "The e-book is currently being accessed by two users. Please try again later"}), 429

    return render_template('ebook.html')

@app.route('/release_ebook', methods=['GET'])
@jwt_required()
def release_ebook():
    user_id = get_jwt_identity()
    remove_session(user_id)
    return jsonify({"msg": "E-book access released"}), 200

@app.route('/static/ebook.pdf')
def serve_ebook():
    return send_from_directory('static', 'ebook.pdf')

if __name__ == '__main__':
    app.run()