# app/services/auth_service.py (Fixed)
from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext  # Fixed typo: was "CryptContent"
from jose import JWTError, jwt
import os
from dotenv import load_dotenv

from app.models.user import User, UserLogin, UserRegister, Token, TokenData
from app.services.user_service import UserService  # Added missing import

load_dotenv()

# Security configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key-change-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Password hashing - Fixed typo
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Bearer token
security = HTTPBearer()

class AuthService:
    @staticmethod
    def hash_password(password: str) -> str:  # Added type hints
        """Hash a password using bcrypt"""
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:  # Added type hints
        """Verify a password against its hash"""
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:  # Added type hints
        """Create a JWT access token"""
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    async def create_user(user_data: UserRegister) -> dict:  # Fixed parameter name and added type hints
        """Create a new user with hashed password"""
        try:
            # Create user record (without password initially)
            hashed_password = AuthService.hash_password(user_data.password)
            user_dict = await UserService.create_user(user_data,hashed_password)  # Fixed variable name
            
            return user_dict
            
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"User creation failed: {str(e)}"
            )
    
    @staticmethod
    async def authenticate_user(credentials: UserLogin) -> Optional[dict]:  # Added type hints
        """Authenticate user with email and password"""
        user = await UserService.get_user_by_email(credentials.email)
        
        if not user:
            return None
        
        if not AuthService.verify_password(credentials.password, user['password_hash']):
            return None
        
        if not user['is_active']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user account"
            )
        
        return user
    
    @staticmethod
    async def login(credentials: UserLogin) -> Token:  
        """Login user and return JWT token"""
        user = await AuthService.authenticate_user(credentials)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Create access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = AuthService.create_access_token(
            data={"sub": user['email'], "user_id": str(user['id'])},
            expires_delta=access_token_expires
        )
        
        # Convert to Pydantic model (remove sensitive data)
        user_response = User(
            id=user['id'],
            email=user['email'],
            name=user['name'],
            wallet_address=user['wallet_address'],
            balance=float(user['balance']),
            invite_code=user['invite_code'],
            is_active=user['is_active'],
            created_at=user['created_at']
        )
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=user_response
        )

# Dependency to get current user from JWT token
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    """Get current authenticated user from JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},  # Fixed typo: was "WWW-Authentication"
    )
    
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])  # Fixed: should be list
        email: str = payload.get("sub")
        user_id: str = payload.get("user_id")
        
        if email is None or user_id is None:
            raise credentials_exception
        
        token_data = TokenData(email=email, user_id=user_id)
    except JWTError:
        raise credentials_exception
    
    user_data = await UserService.get_user_by_id(token_data.user_id)
    if user_data is None:
        raise credentials_exception
    
    # Convert to Pydantic model
    return User(
        id=user_data['id'],
        email=user_data['email'],
        name=user_data['name'],
        wallet_address=user_data['wallet_address'],
        balance=float(user_data['balance']),
        invite_code=user_data['invite_code'],
        is_active=user_data['is_active'],
        created_at=user_data['created_at']
    )



        

