# app/services/user_service.py (Fixed)
from typing import Optional, Dict, Any  # Added missing imports
import uuid
from datetime import datetime

from app.database.connection import execute_query, execute_one, execute_command  # Added missing imports
from app.models.user import UserRegister  # Added missing import

class UserService:
    @staticmethod
    async def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:  # Added type hints
        """Get user by email using raw SQL"""
        query = """
            SELECT id, email, password_hash, name, wallet_address, balance, 
                   invite_code, is_active, created_at, updated_at
            FROM users 
            WHERE email = $1 AND is_active = TRUE
        """
        result = await execute_one(query, email)
        return dict(result) if result else None
    
    @staticmethod
    async def get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:  # Added type hints
        """Get user by ID using raw SQL"""
        query = """
            SELECT id, email, password_hash, name, wallet_address, balance, 
                   invite_code, is_active, created_at, updated_at
            FROM users 
            WHERE id = $1 AND is_active = TRUE
        """
        result = await execute_one(query, user_id)
        return dict(result) if result else None
    
    @staticmethod
    async def create_user(user_data: UserRegister, password_hash:str) -> Dict[str, Any]:  # Fixed parameter name and added type hints
        """Create new user using raw SQL"""
        print(f"DEBUG: Creating user with email: {user_data.email}")

        # Check if email already exists
        existing_user = await UserService.get_user_by_email(user_data.email)
        print(f"DEBUG: Existing user check:{existing_user is not None}")
        if existing_user:
            raise ValueError("Email already registered")
        
        # Check invite code if provided
        if user_data.invite_code:
            invite_check_query = """
                SELECT id FROM users WHERE invite_code = $1
            """
            invite_exists = await execute_one(invite_check_query, user_data.invite_code)  # Fixed variable name
            if invite_exists:
                raise ValueError("Invite code already used")
        
        # Generate user ID and name
        user_id = str(uuid.uuid4())
        user_name = f"User{str(datetime.utcnow().timestamp()).replace('.', '')}"
        print(f"DEBUG: Generated user_id:{user_id}, user_name:{user_name}")
        
        # Insert new user
        insert_query = """
            INSERT INTO users (id, email, password_hash, name, balance, invite_code, created_at, updated_at)
            VALUES ($1, $2, $3, $4, $5, $6, NOW(), NOW())
            RETURNING id, email, name, wallet_address, balance, invite_code, is_active, created_at, updated_at
        """
        print("DEBUG: About to execute insert query")
        result = await execute_one(
            insert_query, 
            user_id, 
            user_data.email, 
            password_hash,
            user_name, 
            10.0,  # Starting balance
            user_data.invite_code
        )
        print(f"DEBUG: Insert result:{result}")
        return dict(result)
    
    @staticmethod
    async def update_user_password_hash(user_id: str, password_hash: str):
        """Update user password hash"""
        query = """
            UPDATE users 
            SET password_hash = $1, updated_at = NOW()
            WHERE id = $2
        """
        await execute_command(query, password_hash, user_id)
    
    @staticmethod
    async def update_user_profile(user_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update user profile using dynamic SQL"""
        # Build dynamic UPDATE query
        set_clauses = []
        params = []
        param_count = 1
        
        for field, value in updates.items():
            if field in ['name', 'wallet_address', 'balance']:  # Only allow certain fields
                set_clauses.append(f"{field} = ${param_count}")
                params.append(value)
                param_count += 1
        
        if not set_clauses:
            raise ValueError("No valid fields to update")
        
        # Add updated_at
        set_clauses.append(f"updated_at = ${param_count}")
        params.append(datetime.utcnow())  # Fixed typo: was "datatime"
        param_count += 1
        
        # Add user_id for WHERE clause
        params.append(user_id)
        
        query = f"""
            UPDATE users 
            SET {', '.join(set_clauses)}
            WHERE id = ${param_count}
            RETURNING id, email, name, wallet_address, balance, invite_code, is_active, created_at, updated_at
        """  # Fixed typo: was "wallet_Address"
        
        result = await execute_one(query, *params)
        return dict(result) if result else None
    
    @staticmethod
    async def get_user_stats(user_id: str) -> Dict[str, Any]:
        """Get user trading statistics using complex SQL"""
        query = """
            SELECT 
                u.id,
                u.name,
                u.balance,
                COALESCE(trade_stats.total_trades, 0) as total_trades,
                COALESCE(trade_stats.total_volume, 0) as total_volume,
                COALESCE(portfolio_stats.portfolio_value, 0) as portfolio_value,
                COALESCE(portfolio_stats.total_invested, 0) as total_invested,
                COALESCE(portfolio_stats.portfolio_value - portfolio_stats.total_invested, 0) as unrealized_pnl
            FROM users u
            LEFT JOIN (
                SELECT 
                    user_id,
                    COUNT(*) as total_trades,
                    SUM(total_value) as total_volume
                FROM trades 
                WHERE status = 'completed'
                GROUP BY user_id
            ) trade_stats ON u.id = trade_stats.user_id
            LEFT JOIN (
                SELECT 
                    p.user_id,
                    SUM(p.amount * t.current_price) as portfolio_value,
                    SUM(p.total_invested) as total_invested
                FROM portfolios p
                JOIN tokens t ON p.token_id = t.id
                GROUP BY p.user_id
            ) portfolio_stats ON u.id = portfolio_stats.user_id  -- Fixed typo: was "portfolio stats"
            WHERE u.id = $1
        """
        
        result = await execute_one(query, user_id)
        return dict(result) if result else None
    
    @staticmethod
    async def delete_user(user_id: str):
        """Soft delete user (set is_active = FALSE)"""
        query = """
            UPDATE users 
            SET is_active = FALSE, updated_at = NOW()
            WHERE id = $1
        """
        await execute_command(query, user_id)
    

