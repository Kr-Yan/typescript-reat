# app/models/user.py (Raw SQL Version)
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, List
from datetime import datetime
import uuid

# Request models (for incoming data)
class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, description="Password must be at least 6 characters")

class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, description="Password must be at least 6 characters")
    invite_code: Optional[str] = Field(None, max_length=50, description="Optional invite code")

class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    wallet_address: Optional[str] = Field(None, max_length=100)
    balance: Optional[float] = Field(None, ge=0, description="Balance must be non-negative")

# Response models (for outgoing data)
class UserBase(BaseModel):
    id: uuid.UUID
    email: str
    name: str
    wallet_address: Optional[str] = None
    balance: float
    invite_code: Optional[str] = None
    is_active: bool
    created_at: datetime

class User(UserBase):
    """Public user model (no sensitive data like password_hash)"""
    
    @classmethod
    def from_db_row(cls, row: dict):
        """Create User from database row"""
        return cls(
            id=row['id'],
            email=row['email'],
            name=row['name'],
            wallet_address=row['wallet_address'],
            balance=float(row['balance']) if row['balance'] else 0.0,
            invite_code=row['invite_code'],
            is_active=row['is_active'],
            created_at=row['created_at']
        )

class UserWithStats(UserBase):
    """User with additional trading statistics"""
    total_trades: int = 0
    total_volume: float = 0.0
    portfolio_value: float = 0.0
    total_invested: float = 0.0
    unrealized_pnl: float = 0.0
    win_rate: float = 0.0
    
    @classmethod
    def from_db_row(cls, row: dict):
        """Create UserWithStats from database row with stats"""
        return cls(
            id=row['id'],
            email=row['email'],
            name=row['name'],
            wallet_address=row['wallet_address'],
            balance=float(row['balance']) if row['balance'] else 0.0,
            invite_code=row['invite_code'],
            is_active=row['is_active'],
            created_at=row['created_at'],
            total_trades=int(row.get('total_trades', 0)),
            total_volume=float(row.get('total_volume', 0)),
            portfolio_value=float(row.get('portfolio_value', 0)),
            total_invested=float(row.get('total_invested', 0)),
            unrealized_pnl=float(row.get('unrealized_pnl', 0)),
            win_rate=float(row.get('win_rate', 0))
        )

# Authentication models
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: User

class TokenData(BaseModel):
    email: Optional[str] = None
    user_id: Optional[str] = None

# Wallet models
class WalletCreate(BaseModel):
    name: str = Field(..., max_length=100, description="Wallet name")
    address: str = Field(..., max_length=100, description="Wallet address")
    blockchain: str = Field(default="solana", max_length=50)
    is_primary: bool = Field(default=False, description="Set as primary wallet")

class WalletResponse(BaseModel):
    id: uuid.UUID
    name: str
    address: str
    blockchain: str
    is_primary: bool
    created_at: datetime
    
    @classmethod
    def from_db_row(cls, row: dict):
        """Create WalletResponse from database row"""
        return cls(
            id=row['id'],
            name=row['name'],
            address=row['address'],
            blockchain=row['blockchain'],
            is_primary=row['is_primary'],
            created_at=row['created_at']
        )

# Portfolio models
class PortfolioItem(BaseModel):
    token_symbol: str
    token_name: str
    amount: float
    avg_buy_price: float
    current_price: float
    total_invested: float
    current_value: float
    unrealized_pnl: float
    pnl_percentage: float
    
    @classmethod
    def from_db_row(cls, row: dict):
        """Create PortfolioItem from database row"""
        amount = float(row['amount'])
        avg_buy_price = float(row['avg_buy_price'])
        current_price = float(row['current_price'])
        total_invested = float(row['total_invested'])
        current_value = amount * current_price
        unrealized_pnl = current_value - total_invested
        pnl_percentage = (unrealized_pnl / total_invested * 100) if total_invested > 0 else 0
        
        return cls(
            token_symbol=row['symbol'],
            token_name=row['name'],
            amount=amount,
            avg_buy_price=avg_buy_price,
            current_price=current_price,
            total_invested=total_invested,
            current_value=current_value,
            unrealized_pnl=unrealized_pnl,
            pnl_percentage=pnl_percentage
        )

class UserPortfolio(BaseModel):
    user: User
    portfolio_items: List[PortfolioItem]
    total_value: float
    total_invested: float
    total_unrealized_pnl: float
    total_pnl_percentage: float

# Trade models
class TradeResponse(BaseModel):
    id: uuid.UUID
    token_symbol: str
    trade_type: str
    amount: float
    price: float
    total_value: float
    status: str
    transaction_hash: Optional[str]
    created_at: datetime
    
    @classmethod
    def from_db_row(cls, row: dict):
        """Create TradeResponse from database row"""
        return cls(
            id=row['id'],
            token_symbol=row['symbol'],
            trade_type=row['trade_type'],
            amount=float(row['amount']),
            price=float(row['price']),
            total_value=float(row['total_value']),
            status=row['status'],
            transaction_hash=row['transaction_hash'],
            created_at=row['created_at']
        )

# Response wrapper models
class UserResponse(BaseModel):
    success: bool
    user: Optional[User] = None
    message: Optional[str] = None

class AuthResponse(BaseModel):
    success: bool
    token: Optional[Token] = None
    message: Optional[str] = None

class PortfolioResponse(BaseModel):
    success: bool
    portfolio: Optional[UserPortfolio] = None
    message: Optional[str] = None

class TradeHistoryResponse(BaseModel):
    success: bool
    trades: List[TradeResponse] = []
    total_count: int = 0
    page: int = 1
    per_page: int = 20
    message: Optional[str] = None

# Error models
class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)