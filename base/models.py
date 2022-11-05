import uuid
from datetime import datetime
import pyotp

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()


def generate_uuid():
    return str(uuid.uuid4())


def generate_secret():
    return pyotp.random_base32()


class User(db.Model):
    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    secret = db.Column(db.String, default=generate_secret)

    def __repr__(self):
        return f"<User> {self.id}"

    def verify_password(self, pwd):
        return pyotp.TOTP(self.secret).verify(pwd)

    @property
    def qr(self):
        return pyotp.TOTP(self.secret).provisioning_uri(
            name="pabs'base", issuer_name="webapp"
        )


class Secret(db.Model):
    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    user_id = db.Column(db.String)
    text = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Secret> <{self.user_id}> {self.text}"
