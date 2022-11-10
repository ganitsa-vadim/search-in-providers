import pydantic


class FlightDateAndPlace(pydantic.BaseModel):
    at: str
    airport: str


class Destination(FlightDateAndPlace):
    pass


class Arrival(FlightDateAndPlace):
    pass


class Segment(pydantic.BaseModel):
    operation_airline: str | None
    marketing_airline: str
    flight_number: int
    equipment: str | None
    dep: Destination
    arr: Arrival
    baggage: str | None


class Flight(pydantic.BaseModel):
    duration: int
    segments: list[Segment]


class Pricing(pydantic.BaseModel):
    total: float
    base: float
    taxes: float
    currency: str


class FlightInfo(pydantic.BaseModel):
    flights: list[Flight]
    refundable: bool
    validating_airline: str
    pricing: Pricing
