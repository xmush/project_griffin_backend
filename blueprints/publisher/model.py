from blueprints import db
from sqlalchemy import ForeignKey
from flask_restful import fields
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from datetime import datetime
from sqlalchemy.orm import relationship

class Publishers(db.Model):
    __tablename__ = "publisher"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    publisher_name = db.Column(db.String(100), nullable=False, unique=True)
    address = db.Column(db.Text(), nullable=True, default="")
    publisher_pict = db.Column(db.Text(), nullable=True, default="")
    company_sertificate = db.Column(db.Text(), nullable=False, default="")
    npwp_number = db.Column(db.String(100), nullable=True, default="")
    npwp_pict = db.Column(db.Text(), nullable=True, default="")
    bank_account_name = db.Column(db.String(100), nullable=True, default="")
    bank_account_number = db.Column(db.String(100), nullable=True, default="")
    bank_account_detail = db.Column(db.Text(), nullable=True, default="")
    is_authorized =  db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
   

    response_fields ={
        'id' : fields.Integer,
        'user_id' : fields.Integer,
        'publisher_name' : fields.String,
        'address' : fields.String,
        'publisher_pict' : fields.String,
        'company_sertificate' : fields.String,
        'npwp_number' : fields.String,
        'npwp_pict' : fields.String,
        'bank_account_name':fields.String,
        'bank_account_number':fields.String,
        'bank_account_detail':fields.String,
        'is_authorized' : fields.Boolean,
        'created_at' : fields.DateTime,
        'updated_at' : fields.DateTime
        }


    def __init__(self, user_id, publisher_name, address, publisher_pict, company_sertificate, npwp_number, npwp_pict, bank_account_name, bank_account_number, bank_account_detail):
        self.user_id = user_id
        self.publisher_name = publisher_name
        self.address = address
        self.publisher_pict = publisher_pict
        self.company_sertificate = company_sertificate
        self.npwp_number = npwp_number
        self.npwp_pict = npwp_pict
        self.bank_account_name = bank_account_name
        self.bank_account_number = bank_account_number
        self.bank_account_detail = bank_account_detail
      

    def __repr__(self):
        return '<Publisher %r>'%self.id