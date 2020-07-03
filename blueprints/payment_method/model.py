from blueprints import db
from flask_restful import fields
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from datetime import datetime
from sqlalchemy.orm import relationship

class PaymentMethods(db.Model):
    __tablename__ = "payment_method"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True ,nullable=False)
    bank_account_name = db.Column(db.String(100), unique=True ,nullable=False)
    bank_account_number = db.Column(db.String(100), unique=True ,nullable=False)
    bank_account_detail = db.Column(db.Text(),nullable=False)
    picture = db.Column(db.Text())
    created_at = db.Column(db.DateTime(timezone=True),server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True),onupdate=func.now())
    transaction = db.relationship("Transactions", cascade="all, delete-orphan", passive_deletes=True)

    
    response_field = {
        'id': fields.Integer,
        'name': fields.String,
        'bank_account_name': fields.String,
        'bank_account_number': fields.String,
        'bank_account_detail': fields.String,
        'picture': fields.String,
        'created_at':fields.DateTime,
        'updated_at':fields.DateTime,
        
    }
    
    def __init__(self, name, bank_account_name, bank_account_number, bank_account_detail, picture):
        self.name = name
        self.bank_account_name = bank_account_name
        self.bank_account_number = bank_account_number
        self.bank_account_detail = bank_account_detail
        self.picture = picture
    
    def __repr__(self):
        return '<PaymentMethod %r>' % self.id