from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal, inputs
from sqlalchemy import desc
from .model import Users
from datetime import datetime
import werkzeug, hashlib, uuid
from blueprints.helper.upload import UploadToFirebase
from blueprints import db, app, admin_required
from flask_jwt_extended import get_jwt_claims, jwt_required

bp_user = Blueprint('User', __name__)
api = Api(bp_user)


class UserList(Resource):
    def __init__(self):
        pass
    @admin_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('user_type', location='args',
                            choices=('user', 'admin'))

        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry = Users.query

        if args['user_type'] is not None:
            qry = qry.filter_by(status=args["user_type"])

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, Users.response_fields))

        return rows, 200
    
class UserResourceSelf(Resource):
    def __init__(self):
        pass

    @jwt_required
    def get(self):
        claims = get_jwt_claims()
        qry = Users.query.get(claims['id'])

        if qry is not None:
            return marshal(qry, Users.response_fields), 200
        return {'status': 'NOT_FOUND'}, 404


class UserResource(Resource):
    def __init__(self):
        pass
    @admin_required
    def get(self, id):
        qry = Users.query.get(id)
        if qry is not None:
            return marshal(qry, Users.response_fields), 200
        return {'status': 'NOT_FOUND'}, 404

    @jwt_required
    def patch(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='form')
        parser.add_argument('phone', location='form')
        parser.add_argument('email', location='form')
        parser.add_argument('is_publisher', location='form', type=bool)
        parser.add_argument('address', location='form')
        parser.add_argument('profil_pict', type=werkzeug.datastructures.FileStorage, location='files')
        parser.add_argument('KTP_number', location='form')
        parser.add_argument('KTP_pict', type=werkzeug.datastructures.FileStorage, location='files')
        parser.add_argument('password', location='form')
        args = parser.parse_args()

        claims = get_jwt_claims()

        qry = Users.query.get(claims['id'])
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404

        salt = uuid.uuid4().hex
        encoded = ('%s%s' % (args['password'], salt)).encode('utf-8')
        hash_pass = hashlib.sha512(encoded).hexdigest()

        
        if args['name'] is not None and args["name"] is not "":
            qry.name = args['name']
        else:
            qry.name = qry.name

        if args['phone'] is not None and args["phone"] is not "":
            qry.phone = args['phone']
        else:
            qry.phone = qry.phone
        
        if args['email'] is not None and args["email"] is not "":
            qry.email = args['email']
        else:
            qry.email = qry.email
        
        if args['is_publisher'] is not None and args["is_publisher"] is not "":
            qry.is_publisher = args['is_publisher']
        else:
            qry.is_publisher = qry.is_publisher
        
        if args['address'] is not None and args["address"] is not "":
            qry.address = args['address']
        else:
            qry.address = qry.address
        
        if args['profil_pict'] is not None and args["profil_pict"] is not "":
            img_profil = args['profil_pict']
            upload_image = UploadToFirebase()
            link = upload_image.UploadImage(img_profil, 'user_profil_pict')
            qry.profil_pict = link
        else:
            qry.profil_pict = qry.profil_pict

        if args['KTP_number'] is not None and args["KTP_number"] is not "":
            qry.KTP_number = args['KTP_number']
        else:
            qry.KTP_number = qry.KTP_number

        if args['KTP_pict'] is not None and args["KTP_pict"] is not "":
            img_ktp = args['KTP_pict']
            upload_image = UploadToFirebase()
            link = upload_image.UploadImage(img_ktp, 'user_KTP_pict')
            qry.KTP_pict = link
        else:
            qry.KTP_pict = qry.KTP_pict

        if args['password'] is not None and args["password"] is not "":
            qry.password = hash_pass
        else:
            qry.password = qry.password

        qry.salt = salt
        qry.updated_at = datetime.now()

        db.session.commit()

        return marshal(qry, Users.response_fields), 200

    @admin_required
    def delete(self, id):
        qry = Users.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
        db.session.delete(qry)
        db.session.commit()
        return {'status': 'DELETED'}, 200

class UserPost(Resource):
    def __init__(self):
        pass
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json', required=True)
        parser.add_argument('phone', location='json', required=True)
        parser.add_argument('email', location='json', required=True)
        parser.add_argument('user_type', location='json',  choices=('user', 'admin'))
        parser.add_argument('password', location='json', required=True)
        
        
        data = parser.parse_args()

        salt = uuid.uuid4().hex
        encoded = ('%s%s' % (data['password'], salt)).encode('utf-8')
        hash_pass = hashlib.sha512(encoded).hexdigest()

        user = Users(data['name'], data['phone'], data['email'], data['user_type'], hash_pass, salt)
        db.session.add(user)
        db.session.commit()

        app.logger.debug('DEBUG : %s', user)

        return marshal(user, Users.response_fields), 200, {'Content-Type': 'application/json'}




api.add_resource(UserList, '', '')
api.add_resource(UserResourceSelf,'/profile/self')
api.add_resource(UserPost,'/profile')
api.add_resource(UserResource, '', '/<id>')