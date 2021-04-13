"""SQLAlchemy models."""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )

    @classmethod
    def signup(cls, username, email, password):
        """Sign up user
        Hashes password and adds user 
        """
        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')
        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
        )
        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


class Favorites(db.Model):
    """A junction table for the many-to-many relationship between users and their favorite cryptos"""
    __tablename__ = 'favorites'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade')
    )

    crypto_id = db.Column(
        db.Integer,
        db.ForeignKey('cryptos.id', ondelete='cascade')
    )


class Cryptos(db.Model):
    """A table for the top 100 cryptos"""
    __tablename__='cryptos'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    crypto_name = db.Column(
        db.Text,
        unique=True,
        nullable=False
    )

def connect_db(app):
    db.app = app
    db.init_app(app)