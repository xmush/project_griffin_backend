from blueprints import db
from flask_restful import fields
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from datetime import datetime
from sqlalchemy.orm import relationship
from blueprints.transaction.model import Transactions
from blueprints.ads_spot.model import AdsSpots



class TransactionDetails(db.Model):
    __tablename__ = 'transaction_detail'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    starting_date = db.Column(db.DateTime(timezone=True))
    durations = db.Column(db.Integer, nullable=False, default=0)
    purpose = db.Column(db.Text())
    price = db.Column(db.Integer, nullable=False, default=0)
    design = db.Column(db.Text())
    add_text = db.Column(db.Text())
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())
     
    ads_spot_id = db.Column(db.Integer, ForeignKey(AdsSpots.id, ondelete='CASCADE'), nullable=False)
    transaction_id = db.Column(db.Integer, ForeignKey(Transactions.id, ondelete='CASCADE'), nullable=False)

    response_field = {
        'id':fields.Integer,
        "transaction_id": fields.Integer,
        "ads_spot_id": fields.Integer,
        'starting_date':fields.DateTime,
        'durations': fields.Integer,
        'purpose':fields.String,
        'price': fields.Integer,
        'design':fields.String,
        'add_text':fields.String,
        'created_at':fields.DateTime, 
        'updated_at':fields.DateTime, 
    }
 
    def __init__(self, transaction_id, ads_spot_id, starting_date, durations, purpose, price, design, add_text):
    
        self.transaction_id = transaction_id
        self.ads_spot_id = ads_spot_id
        self.starting_date = starting_date
        self.durations = durations
        self.purpose = purpose
        self.price = price
        self.design = design
        self.add_text = add_text

    def __repr__(self):
        return '<TransactionDetail %r>' % self.id