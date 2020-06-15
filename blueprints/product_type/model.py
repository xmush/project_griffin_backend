from blueprints import db
from flask_restful import fields
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from datetime import datetime
from sqlalchemy.orm import relationship

class ProductTypes(db.Model):
    __tablename__ = "product_type"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True ,nullable=False)
    icon = db.Column(db.Text())
    created_at = db.Column(db.DateTime(timezone=True),server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True),onupdate=func.now())
    
    response_field = {
        'id': fields.Integer,
        'name': fields.String,
        'icon': fields.String,
        'created_at':fields.DateTime,
        'updated_at':fields.DateTime,
        
    }
    
    def __init__(self, name, icon):
        self.name = name
        self.icon = icon
    
    def __repr__(self):
        return '<ProductType %r>' % self.id