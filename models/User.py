from sqlalchemy.orm import relationship
from extensions import db

class User(db.Model):
    __tablename__ = "user"

    firebase_user_id = db.Column(db.String(200), primary_key=True)  # Firebase User ID field
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    subscription_id = db.Column(db.String(200))
    role = db.Column(db.String(100), default='No Plan')

    @classmethod
    def find_by_firebase_id(cls, firebase_user_id):
        return cls.query.filter_by(firebase_user_id=firebase_user_id).first()

    @property
    def data(self):
        return {
            'id': self.firebase_user_id,
            'username': self.username,
            'email': self.email,
            'subscription_id': self.subscription_id,
            'role': self.role,
        }

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
