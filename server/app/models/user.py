from pydantic import BaseModel
from typing import Optional, Dict

class User(BaseModel):
    id: str
    email: str
    name: str
    wallets: Dict[str, str]
    balance: float
    invite_code: Optional[str] = None
    # No password in public User model

class UserWithPassword(BaseModel):
    """Internal model with password for storage"""
    id: str
    email: str
    name: str
    wallets: Dict[str, str]
    balance: float
    invite_code: Optional[str] = None
    password: str  # Plain text password for development

class UserLogin(BaseModel):
    email: str
    password: str

class UserRegister(BaseModel):
    email: str
    password: str
    invite_code: str

class UserResponse(BaseModel):
    success: bool
    user: Optional[User] = None
    message: Optional[str] = None

class addWalletRequest(BaseModel):
    wallet_name: str
    wallet_address: str


