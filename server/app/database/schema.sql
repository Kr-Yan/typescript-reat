-- app/database/schema.sql (Fixed)
-- Database schema for GMGN Trading Platform

-- Try to create UUID extension (might fail on some PostgreSQL installations)
-- This is why we're getting the error
DO $$ 
BEGIN
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
EXCEPTION 
    WHEN duplicate_object THEN NULL;
    WHEN insufficient_privilege THEN NULL;
END $$;

-- Alternative: Use gen_random_uuid() which is built into modern PostgreSQL
-- or just use regular UUIDs with application-generated values

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),  -- Changed from uuid_generate_v4()
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    wallet_address VARCHAR(100),
    balance DECIMAL(20, 8) DEFAULT 0.0,
    invite_code VARCHAR(50) UNIQUE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Tokens table
CREATE TABLE IF NOT EXISTS tokens (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),  -- Changed from uuid_generate_v4()
    symbol VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    contract_address VARCHAR(100) UNIQUE NOT NULL,
    current_price DECIMAL(20, 8) DEFAULT 0.0,
    price_change_24h DECIMAL(10, 4) DEFAULT 0.0,
    volume_24h DECIMAL(20, 8) DEFAULT 0.0,
    market_cap DECIMAL(20, 8) DEFAULT 0.0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- User portfolios
CREATE TABLE IF NOT EXISTS portfolios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),  -- Changed from uuid_generate_v4()
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token_id UUID NOT NULL REFERENCES tokens(id) ON DELETE CASCADE,
    amount DECIMAL(20, 8) NOT NULL DEFAULT 0.0,
    avg_buy_price DECIMAL(20, 8) NOT NULL DEFAULT 0.0,
    total_invested DECIMAL(20, 8) DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, token_id)
);

-- Trading history
CREATE TABLE IF NOT EXISTS trades (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),  -- Changed from uuid_generate_v4()
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token_id UUID NOT NULL REFERENCES tokens(id) ON DELETE CASCADE,
    trade_type VARCHAR(10) NOT NULL CHECK (trade_type IN ('buy', 'sell')),
    amount DECIMAL(20, 8) NOT NULL,
    price DECIMAL(20, 8) NOT NULL,
    total_value DECIMAL(20, 8) NOT NULL,
    status VARCHAR(20) DEFAULT 'completed' CHECK (status IN ('pending', 'completed', 'failed')),
    transaction_hash VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW()
);

-- User wallets
CREATE TABLE IF NOT EXISTS wallets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),  -- Changed from uuid_generate_v4()
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    address VARCHAR(100) NOT NULL,
    blockchain VARCHAR(50) DEFAULT 'solana',
    is_primary BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_wallet_address ON users(wallet_address);
CREATE INDEX IF NOT EXISTS idx_tokens_symbol ON tokens(symbol);
CREATE INDEX IF NOT EXISTS idx_tokens_contract_address ON tokens(contract_address);
CREATE INDEX IF NOT EXISTS idx_portfolios_user_id ON portfolios(user_id);
CREATE INDEX IF NOT EXISTS idx_portfolios_token_id ON portfolios(token_id);
CREATE INDEX IF NOT EXISTS idx_portfolios_user_token ON portfolios(user_id, token_id);
CREATE INDEX IF NOT EXISTS idx_trades_user_id ON trades(user_id);
CREATE INDEX IF NOT EXISTS idx_trades_token_id ON trades(token_id);
CREATE INDEX IF NOT EXISTS idx_trades_created_at ON trades(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_wallets_user_id ON wallets(user_id);
CREATE INDEX IF NOT EXISTS idx_wallets_address ON wallets(address);

-- Insert sample tokens (only if they don't exist)
INSERT INTO tokens (symbol, name, contract_address, current_price, price_change_24h) VALUES
('SOL', 'Solana', 'So11111111111111111111111111111111111111112', 25.50, 2.5),
('BTC', 'Bitcoin', 'bitcoin-contract-address', 43500.00, -1.2),
('ETH', 'Ethereum', 'ethereum-contract-address', 2650.00, 3.8),
('USDC', 'USD Coin', 'usdc-contract-address', 1.00, 0.0),
('RAY', 'Raydium', 'raydium-contract-address', 1.85, 5.2)
ON CONFLICT (symbol) DO NOTHING;

-- Trigger function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers
DROP TRIGGER IF EXISTS update_users_updated_at ON users;
CREATE TRIGGER update_users_updated_at 
    BEFORE UPDATE ON users 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_tokens_updated_at ON tokens;    
CREATE TRIGGER update_tokens_updated_at 
    BEFORE UPDATE ON tokens 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_portfolios_updated_at ON portfolios;
CREATE TRIGGER update_portfolios_updated_at 
    BEFORE UPDATE ON portfolios 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();