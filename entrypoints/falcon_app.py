# pylint: disable=maybe-no-member
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


class Resource:
    def __init__(self):
        pass

    def on_post(self, req, res):
        print("POST REQUESTED")
        session = get_session()
        repo = repository.SqlAlchemyRepository(session)
        print("media", req.media)
        line = model.OrderLine(
            req.media['orderid'],
            req.media['sku'],
            req.media['qty']
        )
        try:
            batchref = services.allocate(line, repo, session)
        except (model.OutOfStock, services.InvalidSku) as e:
            res.body = json.dumps({'message': str(e)})
            res.status = falcon.HTTP_400
            return None
        
        res.body = json.dumps({'batchref': batchref})
        res.status = falcon.HTTP_201
        return None


app = falcon.API()
app.add_route('/allocate', Resource())

# If a responder ever raised an instance of StorageError, pass control to
# the given handler.
app.add_error_handler(StorageError, StorageError.handle)


