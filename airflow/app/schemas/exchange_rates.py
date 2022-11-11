import pydantic


class Item(pydantic.BaseModel):
    fullname: str
    title: str
    description: float
    quant: int
    index: str
    change: float


class Rates(pydantic.BaseModel):
    generator: str
    title: str
    link: str
    description: str
    copyright: str
    date: str
    items: list[Item] = pydantic.Field(alias="item")


class NationalBankResponse(pydantic.BaseModel):
    rates: Rates
