from pydantic import BaseModel


class Move(BaseModel):
    player: int
    first: int
    second: int
