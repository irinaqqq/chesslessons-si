from pydantic import BaseModel

class UpdateMessagesNumber(BaseModel):
    messages_number: int