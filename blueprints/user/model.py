from blueprints import db
from flask_restful import fields
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from datetime import datetime
from sqlalchemy.orm import relationship

class Users(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(15), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    user_type = db.Column(db.String(100), nullable=False, default='user')
    is_publisher =  db.Column(db.Boolean, nullable=False, default=False)
    password = db.Column(db.String(255))
    salt = db.Column(db.String(255))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
   

    response_fields ={
        'id' : fields.Integer,
        'name' : fields.String,
        'phone' : fields.String,
        'email' : fields.String,
        'user_type' : fields.String,
        'is_publisher' : fields.Boolean,
        'password' : fields.String,
        'created_at' : fields.DateTime,
        'updated_at' : fields.DateTime
        }

    jwt_claims_fields = {
        'id' : fields.Integer,
        'name' : fields.String,
        'user_type' : fields.String,
        'is_publisher' : fields.Boolean
    }

    def __init__(self, name, phone, email, user_type, password, salt):
        self.name = name
        self.phone = phone
        self.email = email
        self.user_type = user_type
        self.password = password
        self.salt = salt
      

    def __repr__(self):
        return '<User %r>'%self.id