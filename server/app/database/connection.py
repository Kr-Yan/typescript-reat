# app/database/connection.py (Fixed)
import asyncpg
import os
from typing import Optional  # Added missing import
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Database configuration - FIXED URL format
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://username:password@localhost:5432/gmgn_trading")  # Removed +asyncpg

# Global connection pool
pool: Optional[asyncpg.Pool] = None

async def init_db():
    """Initialize database connection pool and create tables"""
    global pool
    
    try:
        # Create connection pool (this gives us performance benefits!)
        pool = await asyncpg.create_pool(
            DATABASE_URL,
            min_size=10,  # Minimum connections
            max_size=20,  # Maximum connections
            command_timeout=60
        )
        
        print("✅ Database connection pool created!")
        
        # Read and execute schema
        schema_path = Path(__file__).parent / "schema.sql"
        
        async with pool.acquire() as connection:
            with open(schema_path, 'r') as file:
                schema_sql = file.read()
            
            await connection.execute(schema_sql)
            print("✅ Database schema initialized!")
            
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        raise e

async def close_db():
    """Close database connection pool"""
    global pool
    if pool:
        await pool.close()
        print("🔌 Database connection pool closed")

async def get_db():
    """Get database connection from pool"""
    global pool
    if not pool:
        raise Exception("Database pool not initialized")
    
    return pool.acquire()

# Database utility functions
async def execute_query(query: str, *args):
    """Execute a query and return results"""
    async with pool.acquire() as connection:
        return await connection.fetch(query, *args)

async def execute_one(query: str, *args):
    """Execute a query and return one result"""
    async with pool.acquire() as connection:
        return await connection.fetchrow(query, *args)

async def execute_command(query: str, *args):  # Fixed typo: was "execute_commend"
    """Execute a command (INSERT, UPDATE, DELETE) and return status"""
    async with pool.acquire() as connection:
        return await connection.execute(query, *args)

async def execute_transaction(queries_and_args: list):
    """Execute multiple queries in a transaction"""
    async with pool.acquire() as connection:
        async with connection.transaction():
            results = []
            for query, args in queries_and_args:
                result = await connection.execute(query, *args)
                results.append(result)
            return results
