from django.contrib.auth import get_user_model, authenticate
from ninja import Router
from .schemas import ChatMessage, PartyCreate
from .models import Party, Message
from ..schemas import MessageOut

User = get_user_model()

party_controller = Router(tags=['party'])


@party_controller.post('create_party', response={
    200: MessageOut,
})
def create_party(request, party_in: PartyCreate, ):
    initiator = User.objects.get(email=party_in.owner_email)
    party = Party.objects.create(initiator=initiator)
    return 200, {'detail': 'Party created!'}


@party_controller.post('send_message', response={
    200: MessageOut,
})
def send_message(request, message: ChatMessage):
    party = Party.objects.get(pk=request.data['party_pk'])
    message = Message.objects.create(
        party=party,
        sender=request.user,
        content=message.message,
    )
    return 200, {'detail': 'Message sent!'}


@party_controller.get('get_messages')
def get_messages(request, party_pk: str):
    party = Party.objects.get(pk=party_pk)
    messages = Message.objects.filter(party=party)
    return messages
