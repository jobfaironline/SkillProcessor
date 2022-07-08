from pydantic import BaseModel


class ExtractKeyWordRequest(BaseModel):
    description: str = ""
