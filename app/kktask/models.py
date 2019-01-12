from kktask import db , login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#model
class User(db.Model , UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    registration_number = db.Column(db.Integer, unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.Integer , nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(300), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.registration_number}', '{self.email}', '{self.age}','{self.gender}','{self.address}','{self.image_file}')"
