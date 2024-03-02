from datetime import datetime

from pytest import approx

from hsbcrate import Range
from hsbcrate import Rate
from hsbcrate import RateRequest


def check_rate(r: Rate) -> None:
    assert r.open > 0
    assert r.open * r.inverted_open == approx(1)
    assert datetime.fromtimestamp(r.timestamp / 1000) == r.time


def test_rate_request() -> None:
    pairs = ["USDTWD", "GBPUSD"]
    ranges = list(Range)

    for range in ranges:
        resp_list = RateRequest(ccy_pairs=pairs, range=range).do()

        assert len(resp_list) == len(pairs)

        for resp in resp_list:
            assert resp.ccy_pair in pairs

            for rate in resp.data_set:
                check_rate(rate)

            check_rate(resp.latest)
