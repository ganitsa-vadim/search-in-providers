import choicesenum
import pydantic

from app.schemas.response import FlightInfo


class SearchStatusTypes(choicesenum.ChoicesEnum):
    PENDING: str = 'PENDING'
    COMPLETED: str = 'COMPLETED'


class SearchResults(pydantic.BaseModel):
    search_id: str
    status: str
    items: list[FlightInfo] | None
