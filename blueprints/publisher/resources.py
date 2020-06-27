from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal, inputs
from sqlalchemy import desc
from .model import Publishers
from datetime import datetime
import werkzeug
from blueprints.helper.upload import UploadToFirebase
from blueprints import db, app, admin_required
from flask_jwt_extended import get_jwt_claims, jwt_required

bp_publisher = Blueprint('publisher', __name__)
api = Api(bp_publisher)

class PublisherList(Resource):
    def __init__(self):
        pass

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('name', location='args')

        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry = Publishers.query

        if args['name'] is not None:
            qry = qry.filter_by(status=args["name"])

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, Publishers.response_fields))

        return rows, 200

class PublisherResourceSelf(Resource):
    def __init__(self):
        pass

    @jwt_required
    def get(self):
        claims = get_jwt_claims()
        user_id = claims['id']
        qry = Publishers.query.filter_by(user_id=user_id).first()

        if qry is not None:
            return marshal(qry, Publishers.response_fields), 200
        return {'status': 'NOT_FOUND'}, 404

class PublisherEdit(Resource):
    def __init__(self):
        pass

    @jwt_required
    def patch(self):
        parser = reqparse.RequestParser()
        parser.add_argument('publisher_name', location='form')
        parser.add_argument('address', location='form')
        parser.add_argument('publisher_pict', location='files', type=werkzeug.datastructures.FileStorage)
        parser.add_argument('company_sertificate', location='files', type=werkzeug.datastructures.FileStorage)
        parser.add_argument('npwp_number', location='form')
        parser.add_argument('npwp_pict', location='files', type=werkzeug.datastructures.FileStorage)
        parser.add_argument('bank_account_name', location='form')
        parser.add_argument('bank_account_number', location='form')
        parser.add_argument('bank_account_detail', location='form')
        args = parser.parse_args()

        claims = get_jwt_claims()

        qry = Publishers.query.filter_by(user_id=claims['id']).first()
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404

        if args['publisher_name'] is not None and args["publisher_name"] is not "":
            qry.publisher_name = args['publisher_name']
        else:
            qry.publisher_name = qry.publisher_name

        if args['address'] is not None and args["address"] is not "":
            qry.address = args['address']
        else:
            qry.address = qry.address
        
        publisher_pict = args['publisher_pict']
        if publisher_pict.filename != "":
            upload_image = UploadToFirebase()
            link_publisher_pict = upload_image.UploadImage(publisher_pict, 'user_publisher_pict')
            qry.publisher_pict = link_publisher_pict
        else:
            qry.publisher_pict = qry.publisher_pict
        
        company_sertificate = args['company_sertificate']
        if company_sertificate.filename != "":
            upload_image = UploadToFirebase()
            link_company_sertificate = upload_image.UploadImage(company_sertificate, 'user_company_sertificate')
            qry.company_sertificate = link_company_sertificate
        else:
            qry.company_sertificate = qry.company_sertificate
        
        if args['npwp_number'] is not None and args["npwp_number"] is not "":
            qry.npwp_number = args['npwp_number']
        else:
            qry.npwp_number = qry.npwp_number
        
        npwp_pict = args['npwp_pict']
        if npwp_pict.filename != "":
            upload_image = UploadToFirebase()
            link_npwp_pict = upload_image.UploadImage(npwp_pict, 'user_npwp_pict')
            qry.npwp_pict = link_npwp_pict
        else:
            qry.npwp_pict = qry.npwp_pict

        if args['bank_account_name'] is not None and args["bank_account_name"] is not "":
            qry.bank_account_name = args['bank_account_name']
        else:
            qry.bank_account_name = qry.bank_account_name

        if args['bank_account_number'] is not None and args["bank_account_number"] is not "":
            qry.bank_account_number = args['bank_account_number']
        else:
            qry.bank_account_number = qry.bank_account_number
        
        if args['bank_account_detail'] is not None and args["bank_account_detail"] is not "":
            qry.bank_account_detail = args['bank_account_detail']
        else:
            qry.bank_account_detail = qry.bank_account_detail

        qry.updated_at = datetime.now()

        db.session.commit()

        return marshal(qry, Publishers.response_fields), 200
    

    @jwt_required
    def delete(self):
        claims = get_jwt_claims()
        qry = Publishers.query.filter_by(user_id=claims['id']).first()
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
        db.session.delete(qry)
        db.session.commit()
        return {'status': 'DELETED'}, 200


    

class PublisherResource(Resource):
    def __init__(self):
        pass

    def get(self, id):
        qry = Publishers.query.get(id)
        if qry is not None:
            return marshal(qry, Publishers.response_fields), 200
        return {'status': 'NOT_FOUND'}, 404
    
    @admin_required
    def patch(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('is_authorized', location='form',  choices=(
            'true', 'false'), required=True)
        args = parser.parse_args()

        qry = Publishers.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404


        if args['is_authorized'] is not None and args["is_authorized"] is not "":
            qry.is_authorized = args['is_authorized']
        else:
            qry.is_authorized = qry.is_authorized
        
        
        qry.updated_at = datetime.now()

        db.session.commit()

        return marshal(qry, Publishers.response_fields), 200

class UserPostData(Resource):
    def __init__(self):
        pass

    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('publisher_name', location='form', required=True)
        parser.add_argument('address', location='form', required=True)
        parser.add_argument('publisher_pict', location='files', type=werkzeug.datastructures.FileStorage, required=True)
        parser.add_argument('company_sertificate', location='files', type=werkzeug.datastructures.FileStorage, required=True)
        parser.add_argument('npwp_number', location='form', required=True)
        parser.add_argument('npwp_pict', location='files', type=werkzeug.datastructures.FileStorage, required=True)
        parser.add_argument('bank_account_name', location='form', required=True)
        parser.add_argument('bank_account_number', location='form', required=True)
        parser.add_argument('bank_account_detail', location='form', required=True)
        
        data = parser.parse_args()
        
        claims = get_jwt_claims()
        user_id = claims['id']
        qry = Publishers.query.filter_by(user_id=user_id).first()

        if qry is not None:
            return {"Status":"You are already a publisher"}, 404

        publisher_pict = data['publisher_pict']
        company_sertificate = data['company_sertificate']
        npwp_pict = data['npwp_pict']

        upload_image = UploadToFirebase()
        link_publisher_pict = upload_image.UploadImage(publisher_pict, 'user_publisher_pict')
        link_company_sertificate = upload_image.UploadImage(company_sertificate, 'user_company_sertificate')
        link_npwp_pict = upload_image.UploadImage(npwp_pict, 'user_npwp_pict')

        publisher = Publishers(claims["id"], data['publisher_name'], data['address'], link_publisher_pict, link_company_sertificate, data['npwp_number'], link_npwp_pict, data['bank_account_name'], data['bank_account_number'], data['bank_account_detail'])
        db.session.add(publisher)
        db.session.commit()

        app.logger.debug('DEBUG : %s', publisher)

        return marshal(publisher, Publishers.response_fields), 200, {'Content-Type': 'application/json'}




api.add_resource(PublisherList, '', '')
api.add_resource(PublisherResourceSelf,'/profile/self')
api.add_resource(UserPostData,'')
api.add_resource(PublisherEdit,'/edit')
api.add_resource(PublisherResource, '', '/<id>')
