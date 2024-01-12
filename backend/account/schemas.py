from typing import Optional
from ninja import Schema
from pydantic import EmailStr, Field, UUID4


class AccountCreate(Schema):
    contact_name: str
    email: EmailStr
    password1: str
    password2: str


class AccountOut(Schema):
    email: EmailStr



class TokenOut(Schema):
    access: str


class AuthOut(Schema):
    token: TokenOut
    account: AccountOut


class SigninSchema(Schema):
    email: EmailStr
    password: str


class AccountUpdate(Schema):
    contact_name: str


class ChangePasswordSchema(Schema):
    old_password: str
    new_password1: str
    new_password2: str