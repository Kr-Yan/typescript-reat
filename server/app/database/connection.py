import asyncpg
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://username:password@localhost:5432/gmgn_trading")

# Global connection pool
pool: Optional[asyncpg.Pool]=None

async def init_db():
    global pool

    try:
        # Create connection pool (this gives us performance benefits!)
        pool= await asyncpg.create_pool(
            DATABASE_URL,
            min_size= 10,
            max_size= 20,
            command_timeout=60
        )
        print("Database connection pool created!")

        # Read and execute schema
        schema_path= Path(__file__).parent/"schema.sql"

        async with pool.acquire() as connection:
            with open(schema_path, 'r') as file:
                schema_sql= file.read()
            
            await connection.execute(schema_sql)
            print("Database scheme initialized!")

        
    except Exception as e:
        print(f"Database initialization failed: {e}")
        raise e 


# Database shutdown
async def close_db():
    global pool
    if pool:
        await pool.close()
        print("🔌 Database connection closed")


# Dependency to get database session
async def get_db():
    global pool
    if not pool:
        raise Exception("Database pool not initialized")
    return pool.acquire()

# Database utinility functions
async def execute_query(query,*args):
    """execute a query and return results"""
    async with pool.acquire() as connection:
        return await connection.fetch(query, *args)

async def execute_one(query, *args):
    """ execute a query and return a result"""
    async with pool.acquire() as connection:
        return await connection.fetchrow(query, *args)

async def execute_commend(query, *args):
    """execute a command (insert, delete, update) and return status"""
    async with pool.acquire() as connection:
        return await connection.execute(query, *args)

async def execute_transaction(queries_and_args:list):
    async with pool.acquire() as connection:
        async with connection.transaction():
            results=[]
            for query, args in queries_and_args:
                result= await connection.execute(query, *args)
                results.append(result)
            return results
