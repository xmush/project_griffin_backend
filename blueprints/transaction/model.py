from blueprints import db
from flask_restful import fields
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from datetime import datetime
from sqlalchemy.orm import relationship
from blueprints.payment_method.model import PaymentMethods
from blueprints.user.model import Users
from blueprints.publisher.model import Publishers


class Transactions(db.Model):
    __tablename__ = 'transaction'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    total_price = db.Column(db.Integer, default=0)
    quantity = db.Column(db.Integer, default=0)
    status = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())
    payment_method_id = db.Column(db.Integer, ForeignKey(PaymentMethods.id, ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, ForeignKey(Users.id, ondelete='CASCADE'), nullable=False)
    publisher_id = db.Column(db.Integer, ForeignKey(Publishers.id, ondelete='CASCADE'), nullable=False)
    transaction_detail = db.relationship("TransactionDetails", cascade="all, delete-orphan", passive_deletes=True)

    
    
    response_field = {
        'id': fields.Integer,
        "user_id": fields.Integer,
        "payment_method_id": fields.Integer,
        'publisher_id': fields.Integer,
        "total_price": fields.Integer,
        "quantity": fields.Integer,
        'status': fields.Boolean,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime,
    }

    def __init__(self, user_id, payment_method_id, publisher_id):
        self.user_id = user_id
        self.payment_method_id = payment_method_id
        self.publisher_id = publisher_id

    def __repr__(self):
        return '<Transaction %r>' % self.id