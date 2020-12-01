# pylint: disable=maybe-no-member
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import falcon
import json

from domain import model
from adapters import orm, repository
from service import services

import config

orm.start_mappers()
get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))


class StorageError(Exception):

    @staticmethod
    def handle(ex, req, resp, params):
        description = ('Sorry, couldn\'t write your thing to the '
                       'database. It worked on my box.')

        raise falcon.HTTPError(falcon.HTTP_725,
                               'Database Error',
                               description)


class Router:
    def __init__(self):
        pass

    def on_post_add_batch(self, req, res):
        print("POST REQUESTED")

        session = get_session()
        repo = repository.SqlAlchemyRepository(session)
        eta = req.media['eta']
        ref = req.media['ref']
        sku = req.media['sku']
        qty = req.media['qty']

        if eta is not None:
            eta = datetime.fromisoformat(eta).date()

        services.add_batch(
            ref, sku, qty, eta,
            repo, session
        )
        
        res.body = "OK"
        res.status = falcon.HTTP_201
        return None

    def on_post_allocate(self, req, res):
        print("POST REQUESTED")

        session = get_session()
        repo = repository.SqlAlchemyRepository(session)
        orderid = req.media['orderid']
        sku = req.media['sku']
        qty = req.media['qty']

        try:
            batchref = services.allocate(
                orderid=orderid,
                sku=sku,
                qty=qty,
                repo=repo,
                session=session)
        except (model.OutOfStock, services.InvalidSku) as e:
            res.body = json.dumps({'message': str(e)})
            res.status = falcon.HTTP_400
            return None
        
        res.body = json.dumps({'batchref': batchref})
        res.status = falcon.HTTP_201
        return None


app = falcon.API()
app.add_route('/allocate', Router(), suffix='allocate')
app.add_route('/add_batch', Router(), suffix='add_batch')

# If a responder ever raised an instance of StorageError, pass control to
# the given handler.
app.add_error_handler(StorageError, StorageError.handle)


