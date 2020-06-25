from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal, inputs
from sqlalchemy import desc
from .model import AdsImages
from datetime import datetime
import werkzeug
from blueprints import db, app, admin_required
from blueprints.helper.upload import UploadToFirebase
from flask_jwt_extended import get_jwt_claims, jwt_required



bp_ads_image = Blueprint('ads_image', __name__)
api = Api(bp_ads_image)

class ImageList(Resource):
    def __init__(self):
        pass

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('ads_spot_id', location='args')
        parser.add_argument('name', location='args')

        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry = AdsImages.query

        if args['name'] is not None:
            qry = qry.filter_by(name=args["name"])

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, Users.response_field))

        return rows, 200
    
class ImagesResource(Resource):
    def __init__(self):
        pass

    def get(self, id):
        image = AdsImages.query.filter_by(ads_spot_id=id).all()

        if image is not None:
            return marshal(image, AdsImages.response_field), 200
        return {'status': 'NOT_FOUND'}, 404
    
    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ads_spot_id', location='form', required=True)
        parser.add_argument('name', location='files', type=werkzeug.datastructures.FileStorage, required=True)
        parser.add_argument('description', location='form', required=True)
        data = parser.parse_args()

        img_icon = data['name']
        upload_image = UploadToFirebase()
        link = upload_image.UploadImage(img_icon, 'ads_spot')

        ads_image = AdsImages(data["ads_spot_id"], link, data["description"])
        db.session.add(ads_image)
        db.session.commit()

        app.logger.debug('DEBUG : %s', ads_image)

        return marshal(ads_image, AdsImages.response_field), 200, {'Content-Type': 'application/json'}

api.add_resource(ImageList, '', '')
api.add_resource(ImagesResource, '', '/<id>')
    



