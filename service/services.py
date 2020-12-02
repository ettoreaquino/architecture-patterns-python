from __future__ import annotations
from typing import Optional
from datetime import date
import abc

from domain import model
from adapters import repository

class InvalidSku(Exception):
    pass


def is_valid_sku(sku, batches):
    return sku in {b.sku for b in batches}


def add_batch(
        ref: str, sku: str, qty: int, eta: Optional[date],
        repo: repository.AbstractRepository, session,
):
    repo.add(model.Batch(ref, sku, qty, eta))
    session.commit()


def allocate(
        orderid: str, sku: str, qty: int, repo: repository.AbstractRepository, session
) -> str:
    line = model.OrderLine(orderid, sku, qty)
    batches = repo.list()
    if not is_valid_sku(line.sku, batches):
        raise InvalidSku(f'Invalid sku {line.sku}')
    batchref = model.allocate(line, batches)
    session.commit()
    return batchref

class AbstractUnitOfWork(abc.ABC):
    #  The UoW provides an attribute called .batches,
    # which will give us access to the batches repository.
    batches: repository.AbstractRepository  

    #  If you’ve never seen a context manager, 
    # enter__ and __exit__ are the two magic methods
    # that execute when we enter the with block and when
    # we exit it, respectively. They’re our setup and teardown phases.
    def __exit__(self, *args):  
        self.rollback()  


    # We’ll call this method to explicitly commit our work when we’re ready.
    @abc.abstractmethod
    def commit(self):  
        raise NotImplementedError

    #  If we don’t commit, or if we exit the context manager by raising an
    # error, we do a rollback. (The rollback has no effect if commit() has been
    # called. Read on for more discussion of this.)
    @abc.abstractmethod
    def rollback(self):  
        raise NotImplementedError

