import asyncio
from fastapi import HTTPException
from app.models.user import User, UserLogin, UserRegister
from app.data.users import mock_users
from app.data.users import mock_users_with_passwords


class AuthController:
    @staticmethod
    def login(credentials:UserLogin)-> User:

        user_with_password=next((u for u in mock_users_with_passwords if u.email==credentials.email),None)

        if not user_with_password:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        if user_with_password.password!=credentials.password: raise HTTPException(status_code=401, detail="Invalid email or passwords")

        return User(id=user_with_password.id,
                   email= user_with_password.email,
                    name=user_with_password.name,
                     wallet= user_with_password.wallets,
                      balance=user_with_password.balance,
                       invite_code=user_with_password.invite_code )
    
    @staticmethod
    def register(user_data: UserRegister) -> User:
        existing_user= next((u for u in mock_users_with_passwords if u.email==user_data.email), None)
        