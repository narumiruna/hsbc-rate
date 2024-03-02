from __future__ import annotations

from datetime import datetime
from enum import Enum

import requests
from pydantic import BaseModel
from pydantic import Field
from pydantic import model_validator


class Rate(BaseModel):
    open: float
    timestamp: int
    inverted_open: float = Field(default=0, serialization_alias="invertedOpen")
    time: datetime = Field(default=datetime(1, 1, 1))

    @model_validator(mode="after")
    def validate_inverted_open(self) -> Rate:
        self.time = datetime.fromtimestamp(self.timestamp / 1000)

        if self.inverted_open == 0:
            self.inverted_open = 1 / self.open
        return self


class RateResponse(BaseModel):
    ccy_pair: str = Field(validation_alias="ccyPair")
    data_set: list[Rate] = Field(validation_alias="dataSet")
    latest: Rate
    decimal_places: int = Field(validation_alias="decimalPlaces")
    decimal_places_for_inverted: int = Field(validation_alias="decimalPlacesForInverted")
    high: float
    low: float


class Range(str, Enum):
    ONE_DAY = "day"
    ONE_WEEK = "week"
    ONE_MONTH = "month"
    ONE_YEAR = "year"
    TWO_YEARS = "2y"


# https://currencyzone.hsbc.com/currency-zone/v1/ccypairsrates?ccyPairs=USDGBP&range=month
class RateRequest(BaseModel):
    ccy_pairs: list[str]
    range: Range = Field(default=Range.ONE_DAY)

    def do(self) -> list[RateResponse]:
        url = "https://currencyzone.hsbc.com/currency-zone/v1/ccypairsrates"

        params = {
            "ccyPairs": ",".join(self.ccy_pairs).upper(),
            "range": self.range,
        }

        resp = requests.get(url=url, params=params)

        return [RateResponse(**d) for d in resp.json()]
