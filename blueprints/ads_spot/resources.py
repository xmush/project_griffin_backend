from flask import Blueprint, jsonify
from flask_restful import Api, reqparse, Resource, marshal, inputs
from sqlalchemy import desc
from .model import AdsSpots
from datetime import datetime
import werkzeug
import json
from blueprints import db, app, admin_required
from flask_jwt_extended import get_jwt_claims, jwt_required
from blueprints.user.model import Users
from blueprints.publisher.model import Publishers
from blueprints.ads_image.model import AdsImages
from blueprints.product_type.model import ProductTypes
from blueprints.helper.upload import UploadToFirebase


bp_ads_spot = Blueprint('ads_spot', __name__)
api = Api(bp_ads_spot)


class AdsSpotList(Resource):
    def __init__(self):
        pass

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('created_at', location='args')
        parser.add_argument('publisher_id', location='args')
        parser.add_argument('is_authorized', location='args')

        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry = AdsSpots.query

        if args['created_at'] is not None:
            qry = qry.filter_by(created_at=args["created_at"])

        if args['publisher_id'] is not None:
            qry = qry.filter_by(publisher_id=args["publisher_id"])

        if args['is_authorized'] is not None:
            qry = qry.filter_by(is_authorized=args["is_authorized"])

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, AdsSpots.response_fields))

        return rows, 200


class AdsSpotResource(Resource):
    def __init__(self):
        pass

    def get(self, id):
        qry = AdsSpots.query.get(id)
        QRY = marshal(qry, AdsSpots.response_fields)
        image = AdsImages.query.filter_by(ads_spot_id=id)
        kategori = ProductTypes.query.filter_by(id=QRY["product_type_id"]).first()
        QRY["category"] = marshal(kategori, ProductTypes.response_field)
        rows = []
        for row in image.all():
            rows.append(marshal(row, AdsImages.response_field))
        QRY["images"] = json.dumps(rows)
        if qry is not None:
            return QRY, 200
        return {"status": "Data Not Found"}, 404

    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('product_type_id', location='form', required=True)
        parser.add_argument('name', location='form', required=True)
        parser.add_argument('description', location='form', required=True)
        parser.add_argument('street', location='form', required=True)
        parser.add_argument('subdistrict', location='form', required=True)
        parser.add_argument('district', location='form', required=True)
        parser.add_argument('city', location='form', required=True)
        parser.add_argument('province', location='form', required=True)
        parser.add_argument('latitude', location='form', required=True)
        parser.add_argument('longitude', location='form', required=True)
        parser.add_argument('length', location='form', required=True)
        parser.add_argument('width', location='form', required=True)
        parser.add_argument('orientation', location='form', required=True)
        parser.add_argument('facing', location='form', required=True)
        parser.add_argument('price', location='form', required=True)
        parser.add_argument('minimum_duration', location='form', required=True)
        parser.add_argument('side', location='form', required=True)
        parser.add_argument('lighting', location='form', required=True)
        parser.add_argument('lighting_price', location='form')
        parser.add_argument('banner_price_per_meter',
                            location='form', required=True)
        parser.add_argument('images', type=werkzeug.datastructures.FileStorage,
                            location='files', action='append', required=True)
        data = parser.parse_args()

        claims = get_jwt_claims()
        publisher = Publishers.query.filter_by(user_id=claims["id"]).first()
        publisher_id = publisher.id

        is_authorized = publisher.is_authorized

        if is_authorized == "false":
            return {"Status": "You are not authorize yet"}, 404

        ads_spot = AdsSpots(
            publisher_id,
            data["product_type_id"],
            data["name"],
            data["description"],
            data["street"],
            data["subdistrict"],
            data["district"],
            data["city"],
            data["province"],
            data["latitude"],
            data["longitude"],
            data["length"],
            data["width"],
            data["orientation"],
            data["facing"],
            data["price"],
            data["minimum_duration"],
            data["side"],
            data["lighting"],
            data["lighting_price"],
            data["banner_price_per_meter"])
        db.session.add(ads_spot)
        db.session.flush()

        for image in data['images']:

            ads_spot_id = ads_spot.id
            upload_image = UploadToFirebase()
            link = upload_image.UploadImage(image, 'ads_spot')
            description = image.filename
            images = AdsImages(ads_spot_id, link, description)
            db.session.add(images)

        db.session.commit()

        app.logger.debug('DEBUG : %s', ads_spot)

        return marshal(ads_spot, AdsSpots.response_fields), 200, {'Content-Type': 'application/json'}

    @jwt_required
    def patch(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('product_type_id', location='form')
        parser.add_argument('name', location='form')
        parser.add_argument('description', location='form')
        parser.add_argument('street', location='form')
        parser.add_argument('subdistrict', location='form')
        parser.add_argument('district', location='form')
        parser.add_argument('city', location='form')
        parser.add_argument('province', location='form')
        parser.add_argument('latitude', location='form')
        parser.add_argument('longitude', location='form')
        parser.add_argument('length', location='form')
        parser.add_argument('width', location='form')
        parser.add_argument('orientation', location='form')
        parser.add_argument('facing', location='form')
        parser.add_argument('price', location='form')
        parser.add_argument('minimum_duration', location='form')
        parser.add_argument('side', location='form')
        parser.add_argument('lighting', location='form')
        parser.add_argument('lighting_price', location='form')
        parser.add_argument('banner_price_per_meter', location='form')
        data = parser.parse_args()

        claims = get_jwt_claims()
        publisher = Publishers.query.filter_by(user_id=claims["id"]).first()
        publisher_id = publisher.id

        product = AdsSpots.query.filter_by(publisher_id=publisher_id)
        qry = product.filter_by(id=id).first()

        if qry is None:
            return {"Status": "Data not found"}, 404

        if data['product_type_id'] is not None and data["product_type_id"] != "":
            qry.product_type_id = data['product_type_id']
        else:
            qry.product_type_id = qry.product_type_id

        if data['name'] is not None and data["name"] != "":
            qry.name = data['name']
        else:
            qry.name = qry.name

        if data['description'] is not None and data["description"] != "":
            qry.description = data['description']
        else:
            qry.description = qry.description

        if data['street'] is not None and data["street"] != "":
            qry.street = data['street']
        else:
            qry.street = qry.street

        if data['subdistrict'] is not None and data["subdistrict"] != "":
            qry.subdistrict = data['subdistrict']
        else:
            qry.subdistrict = qry.subdistrict

        if data['district'] is not None and data["district"] != "":
            qry.district = data['district']
        else:
            qry.district = qry.district

        if data['city'] is not None and data["city"] != "":
            qry.city = data['city']
        else:
            qry.city = qry.city

        if data['province'] is not None and data["province"] != "":
            qry.province = data['province']
        else:
            qry.province = qry.province

        if data['latitude'] is not None and data["latitude"] != "":
            qry.latitude = data['latitude']
        else:
            qry.latitude = qry.latitude

        if data['longitude'] is not None and data["longitude"] != "":
            qry.longitude = data['longitude']
        else:
            qry.longitude = qry.longitude

        if data['length'] is not None and data["length"] != "":
            qry.length = data['length']
        else:
            qry.length = qry.length

        if data['width'] is not None and data["width"] != "":
            qry.width = data['width']
        else:
            qry.width = qry.width

        if data['orientation'] is not None and data["orientation"] != "":
            qry.orientation = data['orientation']
        else:
            qry.orientation = qry.orientation

        if data['facing'] is not None and data["facing"] != "":
            qry.facing = data['facing']
        else:
            qry.facing = qry.facing

        if data['price'] is not None and data["price"] != "":
            qry.price = data['price']
        else:
            qry.price = qry.price

        if data['minimum_duration'] is not None and data["minimum_duration"] != "":
            qry.minimum_duration = data['minimum_duration']
        else:
            qry.minimum_duration = qry.minimum_duration

        if data['side'] is not None and data["side"] != "":
            qry.side = data['side']
        else:
            qry.side = qry.side

        if data['lighting'] is not None and data["lighting"] != "":
            qry.lighting = data['lighting']
        else:
            qry.lighting = qry.lighting

        if data['lighting_price'] is not None and data["lighting_price"] != "":
            qry.lighting_price = data['lighting_price']
        else:
            qry.lighting_price = qry.lighting_price

        if data['banner_price_per_meter'] is not None and data["banner_price_per_meter"] != "":
            qry.banner_price_per_meter = data['banner_price_per_meter']
        else:
            qry.banner_price_per_meter = qry.banner_price_per_meter

        qry.updated_at = datetime.now()

        db.session.commit()

        return marshal(qry, AdsSpots.response_fields), 200

    @jwt_required
    def delete(self, id):
        claims = get_jwt_claims()
        publisher = Publishers.query.filter_by(user_id=claims['id']).first()

        product = AdsSpots.query.filter_by(publisher_id=publisher.id)
        qry = product.filter_by(id=id).first()

        if qry is None and image is None:
            return {'status': 'NOT_FOUND'}, 404
        db.session.delete(qry)
        db.session.commit()
        return {'status': 'DELETED'}, 200


class AdsSpotPublisher(Resource):
    def __init__(self):
        pass

    @jwt_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('created_at', location='args')

        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']
        claims = get_jwt_claims()
        publisher = Publishers.query.filter_by(user_id=claims["id"]).first()
        publisher_id = publisher.id

        qry = AdsSpots.query
        qry = qry.filter_by(publisher_id=publisher.id)

        if args['created_at'] is not None:
            qry = qry.filter_by(created_at=args["created_at"])

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, AdsSpots.response_fields))

        return rows, 200


class AuthorizedSpot(Resource):
    def __init__(self):
        pass

    @admin_required
    def patch(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('is_authorized', location='form',  choices=(
            'true', 'false'), required=True)
        data = parser.parse_args()

        qry = AdsSpots.query.get(id)

        if qry is None:
            return {"Status": "Data not Found"}, 404

        if data['is_authorized'] is not None and data["is_authorized"] != "":
            qry.is_authorized = data['is_authorized']
        else:
            qry.is_authorized = qry.is_authorized

        qry.updated_at = datetime.now()

        db.session.commit()

        return marshal(qry, AdsSpots.response_fields), 200


api.add_resource(AdsSpotList, '', '')
api.add_resource(AdsSpotPublisher, '/publisher', '')
api.add_resource(AdsSpotResource, '', '/<id>')
api.add_resource(AuthorizedSpot, '', '/admin/<id>')
