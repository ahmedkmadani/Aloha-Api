import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ \
                os.path.join(basedir, 'user.sqlite3')

db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    UserName = db.Column(db.String(100))
    Email = db.Column(db.String(255))
    Password = db.Column(db.String(255))
    PhoneNumber = db.Column(db.String(255))
    CompanyName = db.Column(db.String(255))
    JobTitle = db.Column(db.String(255))
    Twitter = db.Column(db.String(255))
    Linkdin = db.Column(db.String(255))


    def __init__(self, UserName, Email, Password, PhoneNumber, CompanyName, JobTitle, Twitter, Linkdin):
        self.UserName = UserName
        self.Email = Email
        self.Password = Password
        self.PhoneNumber = PhoneNumber
        self.CompanyName = CompanyName
        self.JobTitle = JobTitle
        self.Twitter = Twitter
        self.Linkdin = Linkdin



class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

user_schema = UserSchema()
users_schema = UserSchema(many=True)


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/user/')
def user_list():
    all_user = User.query.all()
    return jsonify(users_schema.dump(all_user))


@app.route('/user/', methods=['POST'])
def create_user():
    UserName = request.form['UserName']
    Email = request.form['Email']
    Password = bcrypt.generate_password_hash(request.form['Password'])
    PhoneNumber = request.form['PhoneNumber']
    CompanyName = request.form['CompanyName']
    JobTitle = request.form['JobTitle']
    Twitter = request.form['Twitter']
    Linkdin = request.form['Linkdin']

    user = User(UserName = UserName, Email = Email, Password = Password, PhoneNumber = PhoneNumber, CompanyName = CompanyName, 
    JobTitle = JobTitle, Twitter = Twitter, Linkdin = Linkdin)
    
    db.session.add(user)
    db.session.commit()
    
    return user_schema.jsonify(user)


@app.route('/user/<int:user_id>/', methods=["GET"])
def user_detail(user_id):
    user = User.query.get(user_id)
    return user_schema.jsonify(user)


@app.route('/user/<int:user_id>/', methods=['PATCH'])
def update_(user_id):
    UserName = request.form['UserName']
    Email = request.form['Email']
    Password = bcrypt.generate_password_hash(request.form['Password'])
    PhoneNumber = request.form['PhoneNumber']
    CompanyName = request.form['CompanyName']
    JobTitle = request.form['JobTitle']
    Twitter = request.form['Twitter']
    Linkdin = request.form['Linkdin']

    user = User.query.get(user_id)
    
    user.UserName = UserName
    user.Email = Email
    user.Password = Password
    user.PhoneNumber = PhoneNumber
    user.CompanyName = CompanyName
    user.JobTitle = JobTitle
    user.Twitter = Twitter
    user.Linkdin = Linkdin

    db.session.add(user)
    db.session.commit()

    return user_schema.jsonify(user)


@app.route('/user/<int:user_id>/', methods=["DELETE"])
def delete_note(user_id):
    user = User.query.get(user_id)
    
    db.session.delete(user)
    db.session.commit()

    return user_schema.jsonify(user)


if __name__ == '__main__':
    app.run(debug=True)