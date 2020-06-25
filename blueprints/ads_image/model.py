from blueprints import db
from flask_restful import fields
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from datetime import datetime
from blueprints.ads_spot.model import AdsSpots
from sqlalchemy.orm import relationship

class AdsImages(db.Model):
    __tablename__ = 'ads_image'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text(), nullable=False)
    description = db.Column(db.Text())
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())
    ads_spot_id = db.Column(db.Integer, ForeignKey(AdsSpots.id, ondelete='CASCADE'), nullable=False)

    

    response_field = {
        'id': fields.Integer,
        "ads_spot_id": fields.Integer,
        'name': fields.String,
        'description': fields.String,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime,
    }

    def __init__(self, ads_spot_id, name, description):

        self.ads_spot_id = ads_spot_id
        self.name = name
        self.description = description
        

    def __repr__(self):
        return '<AdsImage %r>' % self.id