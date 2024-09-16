from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os
from dotenv import load_dotenv

load_dotenv()

import pymysql
pymysql.version_info = (1, 4, 6, 'final', 0)
pymysql.install_as_MySQLdb()

app = Flask(__name__)
application = app

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    student_id = db.Column(db.String(20), unique=True, nullable=False)
    department = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

# Resource Model
class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    course_code = db.Column(db.String(20), nullable=False)
    public_url = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('created_resources', lazy=True))

# UserResource Model (To save/unsave resources)
class UserResource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    resource_id = db.Column(db.Integer, db.ForeignKey('resource.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('saved_resources', lazy=True))
    resource = db.relationship('Resource', backref=db.backref('saved_by_users', lazy=True))

with app.app_context():
    db.create_all()


# Home Route
@app.route('/')
def home():
    return jsonify({'message': 'Welcome to EduVault!'})

# Register User
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    existing_user = User.query.filter((User.email == data['email']) | (User.student_id == data['student_id'])).first()
    if existing_user:
        return jsonify({'message': 'User with that email or student ID already exists.'}), 409
    
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(
        full_name=data['full_name'],
        student_id=data['student_id'],
        department=data['department'],
        email=data['email'],
        password=hashed_password
    )
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'User created successfully!'},
                   {'user_data': {
                        'id': new_user.id,
                        'full_name': new_user.full_name,
                        'student_id': new_user.student_id,
                        'department': new_user.department,
                        'email': new_user.email
                   }
                   }
                   ), 201


# Login User
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    
    if user and bcrypt.check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Login successful!'},
                       {'user_data': {
                            'id': user.id,
                            'full_name': user.full_name,
                            'student_id': user.student_id,
                            'department': user.department,
                            'email': user.email
                       }
                       }
                       ), 200
    else:
        return jsonify({'message': 'Invalid email or password.'}), 401


# Create Resource
@app.route('/resources', methods=['POST'])
def create_resource():
    data = request.get_json()
    new_resource = Resource(
        title=data['title'],
        description=data['description'],
        category=data['category'],
        course_code=data['course_code'],
        public_url=data['public_url'],
        user_id=data['user_id']
    )
    db.session.add(new_resource)
    db.session.commit()
    return jsonify({'message': 'Resource created successfully'}), 201


# Get All Resources
@app.route('/resources', methods=['GET'])
def get_resources():
    resources = Resource.query.all()
    result = [{
        'id': resource.id,
        'title': resource.title,
        'description': resource.description,
        'category': resource.category,
        'course_code': resource.course_code,
        'public_url': resource.public_url
    } for resource in resources]
    return jsonify(result)


# Get Resource by ID
@app.route('/resources/<int:id>', methods=['GET'])
def get_resource(id):
    resource = Resource.query.get_or_404(id)
    return jsonify({
        'id': resource.id,
        'title': resource.title,
        'description': resource.description,
        'category': resource.category,
        'course_code': resource.course_code,
        'public_url': resource.public_url,
        'user_id': resource.user_id
    })


# Update Resource
@app.route('/resources/<int:id>', methods=['PUT'])
def update_resource(id):
    data = request.get_json()
    resource = Resource.query.get_or_404(id)
    resource.title = data['title']
    resource.description = data['description']
    resource.category = data['category']
    resource.course_code = data['course_code']
    resource.public_url = data['public_url']
    
    db.session.commit()
    return jsonify({'message': 'Resource updated successfully'})



# Delete Resource
@app.route('/resources/<int:id>', methods=['DELETE'])
def delete_resource(id):
    resource = Resource.query.get_or_404(id)
    db.session.delete(resource)
    db.session.commit()
    return jsonify({'message': 'Resource deleted successfully'})


# Save Resource to User's Profile
@app.route('/save_resource', methods=['POST'])
def save_resource():
    data = request.get_json()
    existing_entry = UserResource.query.filter_by(user_id=data['user_id'], resource_id=data['resource_id']).first()
    if existing_entry:
        return jsonify({'message': 'Resource already saved.'}), 409
    
    new_user_resource = UserResource(user_id=data['user_id'], resource_id=data['resource_id'])
    db.session.add(new_user_resource)
    db.session.commit()
    
    return jsonify({'message': 'Resource saved successfully.'}), 201


# Unsave Resource from User's Profile
@app.route('/unsave_resource', methods=['POST'])
def unsave_resource():
    data = request.get_json()
    user_resource = UserResource.query.filter_by(user_id=data['user_id'], resource_id=data['resource_id']).first()
    if user_resource:
        db.session.delete(user_resource)
        db.session.commit()
        return jsonify({'message': 'Resource unsaved successfully.'})
    else:
        return jsonify({'message': 'Resource not found in saved list.'}), 404


# View User's Saved Resources
@app.route('/user/<int:user_id>/saved_resources', methods=['GET'])
def get_saved_resources(user_id):
    user = User.query.get_or_404(user_id)
    saved_resources = [{
        'id': resource.id,
        'title': resource.title,
        'description': resource.description,
        'category': resource.category,
        'course_code': resource.course_code,
        'public_url': resource.public_url
    } for user_resource in user.saved_resources for resource in [user_resource.resource]]
    return jsonify(saved_resources)


# View User's Created Resources
@app.route('/user/<int:user_id>/created_resources', methods=['GET'])
def get_created_resources(user_id):
    user = User.query.get_or_404(user_id)
    created_resources = [{
        'id': resource.id,
        'title': resource.title,
        'description': resource.description,
        'category': resource.category,
        'course_code': resource.course_code,
        'public_url': resource.public_url
    } for resource in user.created_resources]
    return jsonify(created_resources)



if __name__ == '__main__':
    app.run(debug=True)