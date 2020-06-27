from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal, inputs
from sqlalchemy import desc
from .model import ProductTypes
from datetime import datetime
import werkzeug
from blueprints import db, app, admin_required
from blueprints.helper.upload import UploadToFirebase


bp_product_type = Blueprint('product_type', __name__)
api = Api(bp_product_type)


class ProductTypeList(Resource):
    def __init__(self):
        pass

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('orderby', location='args', help='invalid orderby value', choices=('created_at'))
        parser.add_argument('sort', location='args', help='invalid sort value', choices=('desc', 'asc'))
        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry = ProductTypes.query

        if args['orderby'] is not None:
            if args['orderby'] == 'created_at':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(ProductTypes.created_at))
                else:
                    qry = qry.order_by(ProductTypes.created_at)

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, ProductTypes.response_field))

        return rows, 200


class ProductTypeResource(Resource):

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
        parser.add_argument('icon', type=werkzeug.datastructures.FileStorage, location='files')
        data = parser.parse_args()

        img_icon = data['icon']
        upload_image = UploadToFirebase()
        link = upload_image.UploadImage(img_icon, 'category_icon')


        product_type = ProductTypes(data['name'], link)
        db.session.add(product_type)
        db.session.commit()

        app.logger.debug('DEBUG : %s', product_type)

        return marshal(product_type, ProductTypes.response_field), 200, {'Content-Type': 'application/json'}

    @admin_required
    def patch(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='form')
        parser.add_argument('icon', type=werkzeug.datastructures.FileStorage, location='files')
        data = parser.parse_args()

        qry = ProductTypes.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404

        if data['name'] is not None and data["name"] is not "":
                qry.name = data['name']
        else:
            qry.name = qry.name
        
        img_icon = data['icon']
        if img_icon.filename != "":
            upload_image = UploadToFirebase()
            link = upload_image.UploadImage(img_icon, 'category_icon')
            qry.icon = link
        else:
            qry.icon = qry.icon

        
        qry.updated_at = datetime.now()

        db.session.commit()

        return marshal(qry, ProductTypes.response_field), 200

    @admin_required
    def delete(self, id):
        qry = ProductTypes.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
        db.session.delete(qry)
        db.session.commit()
        return {'status': 'DELETED'}, 200


api.add_resource(ProductTypeList, '', '')
api.add_resource(ProductTypeResource, '', '/<id>')
