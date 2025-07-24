import asyncio
from fastapi import HTTPException
from app.models.user import User, UserLogin, UserRegister, UserWithPassword
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
        
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        invalid_invite_code= next((u for u in mock_users_with_passwords if u.invite_code==user_data.invite_code))

        if invalid_invite_code:
            raise HTTPException(status_code=400, detail="Invite code already used")
        

        new_user_with_password=UserWithPassword(
        id=str(len(mock_users_with_passwords)+1),
        email=user_data.email,
        name=f"User{len(mock_users_with_passwords)+1}",
        wallets={
                "Main Wallet": f"5HNeh...{len(mock_users_with_passwords) + 1}"
            },
        balance=10.0,
        invite_code=user_data.invite_code,  # Store the invite code
        password=user_data.password)

        return User(
            id=new_user_with_password.id,
            email=new_user_with_password.email,
            name=new_user_with_password.name,
            wallets=new_user_with_password.wallets,
            balance=new_user_with_password.balance,
            invite_code=new_user_with_password.invite_code
        )
