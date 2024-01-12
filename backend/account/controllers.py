from django.contrib.auth import get_user_model, authenticate
from django.shortcuts import get_object_or_404
from ninja import Router
from .authorization import GlobalAuth, get_tokens_for_user
from .schemas import AccountCreate, AuthOut, SigninSchema, AccountOut, AccountUpdate
from backend.schemas import MessageOut

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


@account_controller.post('signin', response={
    200: AuthOut,
    404: MessageOut,
})
def signin(request, signin_in: SigninSchema):
    user = authenticate(request, email=signin_in.email, password=signin_in.password)
    print(user)
    if not user:
        return 404, {'detail': 'User does not exist'}

    token = get_tokens_for_user(user)

    return {
        'token': token,
        'account': user
    }





@account_controller.get('', auth=GlobalAuth(), response=AccountOut)
def me(request):
    return get_object_or_404(User, id=request.auth['pk'])

@account_controller.put('', auth=GlobalAuth(), response={
    200: AccountOut,
})
def update_account(request, update_in: AccountUpdate):
    User.objects.filter(id=request.auth['pk']).update(**update_in.dict())
    return get_object_or_404(User, id=request.auth['pk'])


