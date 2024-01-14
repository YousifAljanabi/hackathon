from django.contrib.auth import get_user_model, authenticate
from django.shortcuts import get_object_or_404
from ninja import Router
from .authorization import GlobalAuth, get_tokens_for_user
from .schemas import AccountCreate, AuthOut, SigninSchema, AccountOut, AccountUpdate
from backend.schemas import MessageOut
from django.conf import settings
User = get_user_model()

account_controller = Router(tags=['auth'])


@account_controller.post('signup', response={
    400: MessageOut,
    201: AuthOut,
})
def signup(request, account_in: AccountCreate):
    if account_in.password1 != account_in.password2:
        return 400, {'detail': 'Passwords do not match!'}

    try:
        User.objects.get(email=account_in.email)
    except User.DoesNotExist:
        new_user = User.objects.create_user(
            contact_name=account_in.contact_name,
            email=account_in.email,
            password=account_in.password1
        )

        token = get_tokens_for_user(new_user)

        return 201, {
            'token': token,
            'account': new_user,
        }

    return 400, {'detail': 'User already registered!'}

from jose import jwt
@account_controller.post('signin', response={
    200: AuthOut,
    404: MessageOut,
})

def signin(request, signin_in: SigninSchema):
    user = authenticate(request, email=signin_in.email, password=signin_in.password)

    if not user:
        return 404, {'detail': 'User does not exist'}

    token = get_tokens_for_user(user)

    return {
        'token': token,
        'account': user
    }
@account_controller.get('check', auth=GlobalAuth(), response=AccountOut)
def check(request):
    user = get_object_or_404(User, pk=request.auth.get('pk'))
    if user:
        return 200, user
    else:
        return 404, {'detail': 'User does not exist'}
