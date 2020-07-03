from blueprints import db
from flask_restful import fields
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from datetime import datetime
from sqlalchemy.orm import relationship

class Users(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    user_type = db.Column(db.String(100), nullable=False, default='user')
    is_publisher =  db.Column(db.String(10), nullable=False, default="false")
    address = db.Column(db.Text(), nullable=True, default="")
    profil_pict = db.Column(db.Text(), nullable=True, default="")
    KTP_number = db.Column(db.String(100), nullable=True, default="")
    KTP_pict = db.Column(db.Text(), nullable=True, default="")
    password = db.Column(db.String(255))
    salt = db.Column(db.String(255))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    publishers = db.relationship("Publishers", cascade="all, delete-orphan", passive_deletes=True)
    transaction = db.relationship("Transactions", cascade="all, delete-orphan", passive_deletes=True)
   

    response_fields ={
        'id' : fields.Integer,
        'name' : fields.String,
        'phone' : fields.String,
        'email' : fields.String,
        'user_type' : fields.String,
        'is_publisher' : fields.String,
        'address':fields.String,
        'profil_pict':fields.String,
        'KTP_number':fields.String,
        'KTP_pict':fields.String,
        'password' : fields.String,
        'created_at' : fields.DateTime,
        'updated_at' : fields.DateTime
        }

    jwt_claims_fields = {
        'id' : fields.Integer,
        'name' : fields.String,
        'user_type' : fields.String,
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