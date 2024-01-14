from ninja import Schema
from pydantic import UUID4, EmailStr


class PartyCreate(Schema):
    owner_email: EmailStr



class ChatMessage(Schema):
    message: str
    sender: str
    party_pk: UUID4
    sender_pk: UUID4
    timestamp: str

