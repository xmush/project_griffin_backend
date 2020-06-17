from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal, inputs
from sqlalchemy import desc
from .model import PaymentMethods
from datetime import datetime
import werkzeug
from blueprints import db, app, admin_required
from blueprints.helper.upload import UploadToFirebase


bp_payment_method = Blueprint('payment_method', __name__)
api = Api(bp_payment_method)

class PaymentMethodList(Resource):
    def __init__(self):
        pass

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry = PaymentMethods.query

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, PaymentMethods.response_field))

        return rows, 200


class PaymentMethodResource(Resource):
    def __init__(self):
        pass

    def get(self, id):
        qry = ProductTypes.query.get(id)
        if qry is not None:
            return marshal(qry, ProductTypes.response_field), 200
        return {'status': 'NOT_FOUND'}, 404

    @admin_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='form', required=True)
        parser.add_argument('bank_account_name', location='form', required=True)
        parser.add_argument('bank_account_number', location='form', required=True)
        parser.add_argument('bank_account_detail', location='form', required=True)
        parser.add_argument('picture', type=werkzeug.datastructures.FileStorage, location='files')
        data = parser.parse_args()

        img_picture = data['picture']
        upload_image = UploadToFirebase()
        link_picture = upload_image.UploadImage(img_picture, 'category_picture')


        payment_method = PaymentMethods(data['name'], data['bank_account_name'], data['bank_account_number'], data['bank_account_detail'], link_picture)
        db.session.add(payment_method)
        db.session.commit()

        app.logger.debug('DEBUG : %s', payment_method)

        return marshal(payment_method, PaymentMethods.response_field), 200, {'Content-Type': 'application/json'}

    @admin_required
    def patch(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='form')
        parser.add_argument('bank_account_name', location='form')
        parser.add_argument('bank_account_number', location='form')
        parser.add_argument('bank_account_detail', location='form')
        parser.add_argument('picture', type=werkzeug.datastructures.FileStorage, location='files')
        data = parser.parse_args()

        qry = PaymentMethods.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404

        if data['name'] is not None and data["name"] is not "":
                qry.name = data['name']
        else:
            qry.name = qry.name
        
        if data['bank_account_name'] is not None and data["bank_account_name"] is not "":
                qry.bank_account_name = data['bank_account_name']
        else:
            qry.bank_account_name = qry.bank_account_name
        
        if data['bank_account_number'] is not None and data["bank_account_number"] is not "":
                qry.bank_account_number = data['bank_account_number']
        else:
            qry.bank_account_number = qry.bank_account_number
        
        if data['bank_account_detail'] is not None and data["bank_account_detail"] is not "":
                qry.bank_account_detail = data['bank_account_detail']
        else:
            qry.bank_account_detail = qry.bank_account_detail
        
        if data['picture'] is not None and data["picture"] is not "":
            img_picture = data['picture']
            upload_image = UploadToFirebase()
            link = upload_image.UploadImage(img_picture, 'category_picture')
            qry.picture = link
        else:
            qry.picture = qry.picture

        
        qry.updated_at = datetime.now()

        db.session.commit()

        return marshal(qry, PaymentMethods.response_field), 200

    @admin_required
    def delete(self, id):
        qry = PaymentMethods.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
        db.session.delete(qry)
        db.session.commit()
        return {'status': 'DELETED'}, 200


api.add_resource(PaymentMethodList, '', '/list')
api.add_resource(PaymentMethodResource, '', '/<id>')