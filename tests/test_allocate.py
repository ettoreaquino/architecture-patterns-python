from datetime import date, timedelta
import pytest

from src.model import Batch, OrderLine
from src.services import allocate, OutOfStock

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)

# TESTS
def test_prefers_current_stock_batches_to_shipments():
    in_stock_batch = Batch("in-stock-batch", "RETRO-CLOCK", 100, eta=None)
    shipment_batch = Batch("shipment-batch", "RETRO-CLOCK", 100, eta=tomorrow)
    line = OrderLine("oref", "RETRO-CLOCK", 10)

    allocate(line, [in_stock_batch, shipment_batch])

    assert in_stock_batch.available_quantity == 90
    assert shipment_batch.available_quantity == 100

def test_prefers_earlier_batcher():
    earliest = Batch("speedy-batch", "MINIMALIST-SPOON", 100, eta=today)
    medium = Batch("normal-batch", "MINIMALIST-SPOON", 100, eta=tomorrow)
    latest = Batch("slow-batch", "MINIMALIST-SPOON", 100, eta=later)
    line = OrderLine("order-001", "MINIMALIST-SPOON", 10)

    allocate(line, [medium, earliest, latest])

    # TEST IF THE EARLIEST BATCH WAS THE ONE USED
    assert earliest.available_quantity == 90
    assert medium.available_quantity == 100
    assert latest.available_quantity == 100

def test_return_allocated_batches():
    in_stock_batch = Batch("in-stock-batch-ref", "HIGHBROWN-POSTER", 100, eta=None)
    shipment_batch = Batch("shipment-batch-ref", "HIGHBROWN-POSTER", 100, eta=tomorrow)
    line = OrderLine("oref", "HIGHBROWN-POSTER", 10)
    allocation = allocate(line, [in_stock_batch, shipment_batch])

    assert allocation == in_stock_batch.reference

def test_raises_out_of_stock_exception_if_cannot_allocate():
    batch = Batch("batch-001", "SMALL-FORK", 10, eta=today)
    allocate(OrderLine("order-001", "SMALL-FORK", 10), [batch])

    with pytest.raises(OutOfStock, match="SMALL-FORK"):
        allocate(OrderLine("order-002", "SMALL-FORK", 1), [batch])