from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal

from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims

import hashlib
import uuid
from ..user.model import Users

bp_auth = Blueprint('auth', __name__)
api = Api(bp_auth)

class CreateTokenResource(Resource):
    
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', location='args')
        parser.add_argument('phone', location='args')
        parser.add_argument('password', location='args', required=True)
        args = parser.parse_args()

        if args['email'] is None:
            qry_user = Users.query.filter_by(
            phone=args['phone']).first()
        else:
            qry_user = Users.query.filter_by(
            email=args['email']).first()

        if qry_user is not None:
            user_salt = qry_user.salt
            user_type = qry_user.user_type
            encoded = ('%s%s' %
                       (args['password'], user_salt)).encode('utf-8')
            hash_pass = hashlib.sha512(encoded).hexdigest()
            if hash_pass == qry_user.password and qry_user.email == args['email']:
                qry_user = marshal(qry_user, Users.jwt_claims_fields)
                qry_user['identifier'] = "ads_marketplace"
                token = create_access_token(
                    identity=args['email'], user_claims=qry_user)
                return {'token': token}, 200
            elif hash_pass == qry_user.password and qry_user.phone == args['phone']:
                qry_user = marshal(qry_user, Users.jwt_claims_fields)
                qry_user['identifier'] = "ads_marketplace"
                token = create_access_token(
                    identity=args['phone'], user_claims=qry_user)
                return {'token': token}, 200
        return {'status': 'UNAUTHORIZED', 'message': 'invalid key or secret'}, 404


api.add_resource(CreateTokenResource, '')