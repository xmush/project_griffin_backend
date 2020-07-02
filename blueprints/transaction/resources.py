from flask import Blueprint
from flask_restful import Api, Resource, marshal, reqparse, inputs
from .model import Transactions
from blueprints.user.model import Users
from blueprints.publisher.model import Publishers
from blueprints.ads_spot.model import AdsSpots
from sqlalchemy import desc
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims
from blueprints.transaction_detail.model import TransactionDetails
from datetime import datetime
from blueprints import db, app 

bp_transaction = Blueprint('transaction', __name__)
api = Api(bp_transaction)

class TransactionlList(Resource):
    def __init__(self):
        pass

    @jwt_required
    def get(self): #advertiser get unfinished transaction data 
        claims = get_jwt_claims()
        user = Users.query.get(claims["id"])
        user_id = user.id

        transaction_user = Transactions.query.filter_by(user_id=user_id, status=True)
        # transaction_status = transaction_user.filter_by(status=True)
        transaction_order = transaction_user.order_by(desc(Transactions.updated_at))

        transaction_order = transaction_order.all()
        
        transactions = []

        for transaction in transaction_order:
            QRY_transaction = marshal(transaction, Transactions.response_field)
            publisher = Publishers.query.filter_by(id=QRY_transaction["publisher_id"]).first()
            QRY_transaction["publisher"] = marshal(publisher, Publishers.response_show)
            
            transaction_details = TransactionDetails.query.filter_by(transaction_id=QRY_transaction["id"]).all()

            list_transaction_detail = []

            for transaction_detail in transaction_details:
                QRY_transaction_detail = marshal(transaction_detail, TransactionDetails.response_field)
                ads_spot = AdsSpots.query.filter_by(id=QRY_transaction_detail["ads_spot_id"]).first()
                QRY_transaction_detail["ads_spot"] =  marshal(ads_spot, AdsSpots.response_fields)

                list_transaction_detail.append(QRY_transaction_detail)

            transactions.append({"transaction":QRY_transaction, "transaction_detail":list_transaction_detail})
        
        return transactions, 200

class TransactionResource(Resource):
    def __init__(self):
        pass

    @jwt_required #advertiser try to rent ads_spotS
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("payment_method_id", type=int, location="json")
        parser.add_argument("ads_spot_id", type=int, location="json")
        parser.add_argument("starting_date", type=lambda x: datetime.strptime(x,'%Y-%m-%dT%H:%M:%S'), location="json")
        parser.add_argument("durations", location="json")
        parser.add_argument("purpose", location="json")
        parser.add_argument("design", location="json")
        parser.add_argument("add_text", location="json")


        data = parser.parse_args()
        
        claims = get_jwt_claims()

        user = Users.query.get(claims["id"])
        user_id = user.id

        ads_spot = AdsSpots.query.get(data["ads_spot_id"])

        if ads_spot is None:
            return { "Status":" Spot Not Available"}, 404
        
        transaction_status = Transactions.query.filter_by(status=True)
        transaction_user = transaction_status.filter_by(user_id=user_id)
        transaction = transaction_user.filter_by(publisher_id=ads_spot.publisher_id).first()


        if transaction is None:
            transaction = Transactions(user_id, data["payment_method_id"], ads_spot.publisher_id)
            db.session.add(transaction)
            db.session.commit()

        
        transaction_detail = TransactionDetails.query.filter_by(transaction_id=transaction.id,ads_spot_id=data["ads_spot_id"]).first()
        price = ads_spot.price * durations
        if transaction_detail is None:
            td = TransactionDetails(transaction.id, ads_spot.id, data["starting_date"], data["durations"], data["purpose"], price, data["design"], data["add_text"])
            db.session.add(td)
            db.session.commit()
        
        transaction.quantity += 1
        transaction.total_price += price
        
        transaction.updated_at = datetime.now()
        db.session.commit()

        return {'status': 'Success'}, 200

    @jwt_required #advertiser try to cancel order 
    def delete(self, id):
        claims = get_jwt_claims()
        user = Users.query.get(claims["id"])
        user_id = user.id

        if user is None:
            app.logger.debug('DEBUG:pembeli tidak terdaftar')
            return {"Status":"User tidak terdaftar"}, 404
        
        transaction_detail = TransactionDetails.query.filter_by(id=id).first()
        transaction_id = transaction_detail.transaction_id
        transaction = Transactions.query.filter_by(status=True)
        transaction_user = transaction.filter_by(user_id=user_id)
        transaction_present = transaction_user.filter_by(id=transaction_id).first()

        transaction_present.quantity -= 1
        transaction_present.total_price -= transaction_detail.price

        if transaction_present.quantity == 0:
            db.session.delete(transaction_present)
        
        db.session.delete(transaction_detail)
        db.session.commit()

        app.logger.debug('DEBUG: data telah terhapus')
        return {'status': 'DELETED'}, 200


class TransactionChoice(Resource):
    def __init__(self):
        pass

    @jwt_required #advertiser try to cancel order
    def delete(self):
        claims = get_jwt_claims()
        user = Users.query.get(claims["id"])
        user_id = user.id

        if user is None:
            app.logger.debug('DEBUG:pembeli tidak terdaftar')
            return {"Status":"User tidak terdaftar"}, 404

        transaction_status = Transactions.query.filter_by(status=True)
        transaction_user = transaction_status.filter_by(user_id=user_id).first()

        if transaction_user is None:
            return {"status":"Tidak ada transaksi"}, 404
        
        db.session.delete(transaction_user)
        db.session.commit()

        app.logger.debug('DEBUG: data telah terhapus')
        return {'status': 'DELETED'}, 200

class TransactionCheckout(Resource):
    def __init__(self):
        pass

    @jwt_required  #advertiser do checkout
    def patch(self):
        parser = reqparse.RequestParser()
        parser.add_argument("status", type=bool, location="json")

        data = parser.parse_args()

        claims = get_jwt_claims()
        user = Users.query.get(claims["id"])

        user_id = user.id

        transaction_status = Transactions.query.filter_by(status=True)
        transaction_user = transaction_status.filter_by(user_id=user_id).all()

        for idx_transaction in range(len(transaction_user)):
            transaction_user[idx_transaction].status = data["status"]
            db.session.commit()
        
        return {"Status":"Anda berhasil checkout"}, 200
    
    def get(self): #publisher get finished transaction data 
        claims = get_jwt_claims()
        publisher = Publishers.query.filter_by(user_id=claims["id"]).first()
        publisher_id = publisher.id

        transaction_publisher = Transactions.query.filter_by(publisher_id=publisher_id)
        transaction_status = transaction_publisher.filter_by(status=False)
        transaction_order = transaction_status.order_by(desc(Transactions.updated_at))
        
        transactions = []

        for transaction in transaction_order.all():
            QRY_transaction = marshal(transaction. Transactions.response_field)
            user = Users.query.filter_by(id=QRY_transaction["user_id"]).first()
            QRY_transaction["user"] = marshal(user, Users.response_fields)
            
            transaction_details = TransactionDetails.query.filter_by(transaction_id=QRY_transaction["id"]).all()

            list_transaction_detail = []

            for transaction_detail in transaction_details:
                QRY_transaction_detail = marshal(transaction_detail, TransactionDetails.response_field)
                ads_spot = AdsSpots.query.filter_by(id=QRY_transaction_detail["ads_spot_id"]).first()
                QRY_transaction_detail["ads_spot"] =  marshal(ads_spot, AdsSpots.response_fields)

                list_transaction_detail.append(QRY_transaction_detail)

            transactions.append({"transaction":QRY_transaction, "transaction_detail":list_transaction_detail})
        
        return transactions, 200

class HistoryTransaction(Resource):
    def __init__(self):
        pass
    
    @jwt_required
    def get(self):
        claims = get_jwt_claims()
        user = Users.query.get(claims["id"])
        user_id = user.id

        transaction_user = Transactions.query.filter_by(user_id=user_id)
        transaction_status = transaction_user.filter_by(status=False)
        transaction_order = transaction_status.order_by(desc(Transactions.updated_at))
        
        transactions = []

        for transaction in transaction_order.all():
            QRY_transaction = marshal(transaction. Transactions.response_field)
            publisher = Publishers.query.filter_by(id=QRY_transaction["publisher_id"]).first()
            QRY_transaction["publisher"] = marshal(publisher, Publishers.response_fields)
            
            transaction_details = TransactionDetails.query.filter_by(transaction_id=QRY_transaction["id"]).all()

            list_transaction_detail = []

            for transaction_detail in transaction_details:
                QRY_transaction_detail = marshal(transaction_detail, TransactionDetails.response_field)
                ads_spot = AdsSpots.query.filter_by(id=QRY_transaction_detail["ads_spot_id"]).first()
                QRY_transaction_detail["ads_spot"] =  marshal(ads_spot, AdsSpots.response_fields)

                list_transaction_detail.append(QRY_transaction_detail)

            transactions.append({"transaction":QRY_transaction, "transaction_detail":list_transaction_detail})
        
        return transactions, 200




api.add_resource(TransactionlList, '', '')
api.add_resource(TransactionChoice, '/choice ', '')
api.add_resource(TransactionCheckout, '/checkout', '')
api.add_resource(HistoryTransaction, '/history', '')
api.add_resource(TransactionResource, '', '/<id>')