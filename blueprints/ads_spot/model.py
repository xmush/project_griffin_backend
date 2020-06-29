from blueprints import db
from flask_restful import fields
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from datetime import datetime
from blueprints.publisher.model import Publishers
from blueprints.product_type.model import ProductTypes
from sqlalchemy.orm import relationship


class AdsSpots(db.Model):
    __tablename__ = 'ads_spot'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text())
    street = db.Column(db.Text(), nullable=False)
    subdistrict = db.Column(db.String(255), nullable=False)
    district = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    province = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.Float())
    longitude = db.Column(db.Float())
    length = db.Column(db.String(255))
    width = db.Column(db.String(255))
    orientation = db.Column(db.String(255))
    facing = db.Column(db.String(255))
    price = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(255), nullable=False, default="Belum Disewa")
    minimum_duration = db.Column(db.Integer, nullable=False)
    side = db.Column(db.String(255))
    lighting = db.Column(db.String(255))
    lighting_price = db.Column(db.Integer, default=0)
    banner_price_per_meter = db.Column(db.Integer, nullable=False)
    is_authorized = db.Column(db.String(10), nullable=False, default="false")
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())

    publisher_id = db.Column(db.Integer, ForeignKey(
        Publishers.id, ondelete='CASCADE'), nullable=False)
    product_type_id = db.Column(db.Integer, ForeignKey(
        ProductTypes.id, ondelete='CASCADE'), nullable=False)
    ads_image = db.relationship(
        "AdsImages", cascade="all, delete-orphan", passive_deletes=True)

    response_fields = {
        'id': fields.Integer,
        "publisher_id": fields.Integer,
        "product_type_id": fields.Integer,
        'name': fields.String,
        'description': fields.String,
        'street': fields.String,
        'subdistrict': fields.String,
        'district': fields.String,
        'city': fields.String,
        'province': fields.String,
        'latitude': fields.Float,
        'longitude': fields.Float,
        'length': fields.String,
        'width': fields.String,
        'orientation': fields.String,
        'facing': fields.String,
        'price': fields.Integer,
        'status': fields.String,
        "minimum_duration": fields.Integer,
        'side': fields.String,
        'lighting': fields.String,
        "lighting_price": fields.Integer,
"banner_price_per_meter":fields.Integer,
        "is_authorized": fields.String,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime,
    }

    response_images = {
        'name': fields.String
    }

    def __init__(self,
                 publisher_id,
                 product_type_id,
                 name,
                 description,
                 street,
                 subdistrict,
                 district,
                 city,
                 province,
                 latitude,
                 longitude,
                 length,
                 width,
                 orientation,
                 facing,
                 price,
                 minimum_duration,
                 side,
                 lighting,
                 lighting_price,
                 banner_price_per_meter):

        self.publisher_id = publisher_id
        self.product_type_id = product_type_id
        self.name = name
        self.description = description
        self.street = street
        self.subdistrict = subdistrict
        self.district = district
        self.city = city
        self.province = province
        self.latitude = latitude
        self.longitude = longitude
        self.length = length
        self.width = width
        self.orientation = orientation
        self.facing = facing
        self.price = price
        self.minimum_duration = minimum_duration
        self.side = side
        self.lighting = lighting,
        self.lighting_price = lighting_price,
        self.banner_price_per_meter = banner_price_per_meter

    def __repr__(self):
        return '<AdsSpot %r>' % self.id
