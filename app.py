import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ \
                os.path.join(basedir, 'user.sqlite3')

db = SQLAlchemy(app)
ma = Marshmallow(app)


class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    UserName = db.Column(db.String(100))
    Password = db.Column(db.String(255))
    Email = db.Column(db.String(255))
    PhoneNumber = db.Column(db.String(255))
    CompanyName = db.Column(db.String(255))
    JobTitle = db.Column(db.String(255))
    Twitter = db.Column(db.String(255))
    Linkldin = db.Column(db.String(255))

    def __init__(self, UserName, Password, Email, PhoneNumber, CompanyName, JobTitle, Twitter, Linkldin):
        self.UserName = UserName
        self.Password = Password
        self.Email = Email
        self.CompanyName = CompanyName
        self.JobTitle = JobTitle
        self.Twitter = Twitter
        self.Linkldin = Linkldin


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel

user_schema = UserSchema()
user_schema = UserSchema(many=True)


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/user/')
def user_list():
    all_users = UserModel.query.all()
    return jsonify(user_schema.dump(all_users))


@app.route('/user/', methods=['POST'])
def create_user():
    UserName = request.form['name']
    Password = request.form['password']
    Email = request.form['email']
    PhoneNumber = request.form['phone']
    CompanyName = request.form['companyname']
    JobTitle = request.form['jobtitle']
    Twitter = request.form['twitter']
    Linkldin = request.form['linkidn']

    user = UserModel(UserName=UserName, Password=Password, Email = Email, PhoneNumber = PhoneNumber, CompanyName = CompanyName, JobTitle = JobTitle, Twitter = Twitter, Linkldin = Linkldin)
    
    db.session.add(user)
    db.session.commit()
    
    return user_schema.jsonify(user)


@app.route('/user/<int:user_id>/', methods=["GET"])
def user_detail(user_id):
    user = UserModel.query.get(user_id)
    return user_schema.jsonify(user)


@app.route('/user/<int:user_id>/', methods=['PATCH'])
def update_user(user_id):
    UserName = request.form['name']
    Password = request.form['password']
    Email = request.form['email']
    PhoneNumber = request.form['phone']
    CompanyName = request.form['companyname']
    JobTitle = request.form['jobtitle']
    Twitter = request.form['twitter']
    Linkldin = request.form['linkidn']

    user = UserModel.query.get(user_id)
    
    user.UserName = UserName
    user.Password = Password
    user.Email = Email
    user.PhoneNumber = PhoneNumber
    user.CompanyName = CompanyName
    user.JobTitle = JobTitle
    user.Twitter = Twitter
    user.Linkldin = Linkldin

    db.session.add(user)
    db.session.commit()

    return user_schema.jsonify(user)


@app.route('/user/<int:user_id>/', methods=["DELETE"])
def delete_user(user_id):
    user = UserModel.query.get(user_id)
    
    db.session.delete(user)
    db.session.commit()

)


if __name__ == '__main__':
    app.run(debug=True)