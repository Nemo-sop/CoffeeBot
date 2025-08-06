from pydantic import BaseModel

class UserQuery(BaseModel):
    question: str
    history: list[str] = []

class BotResponse(BaseModel):
    answer: str
    retries: int  