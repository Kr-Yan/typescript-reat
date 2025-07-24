from app.models.user import User
from app.models.user import UserWithPassword

mock_users = [
    User(
        id="1",
        email="demo@gmgn.ai",
        name="Demo User",
        wallets={
            "Main Wallet": "5HNeh...rzq2",
            "Trading Wallet": "8xKp2...mz9",
            "DeFi Wallet": "3nL9s...4vX"
        },
        balance=84.54
    ),
    User(
        id="2", 
        email="trader@gmgn.ai",
        name="Pro Trader",
        wallets={
            "Primary": "9QwE3...7yH",
            "Backup": "2Mn8v...3kL"
        },
        balance=156.23
    )
]

mock_users_with_passwords = [
    UserWithPassword(
        id="1",
        email="demo@gmgn.ai",
        name="Demo User",
        wallets={
            "Main Wallet": "5HNeh...rzq2",
            "Trading Wallet": "8xKp2...mz9",
            "DeFi Wallet": "3nL9s...4vX"
        },
        balance=84.54,
        password="demo123",
        invite_code="DEMO123ABC"  # This invite code is already used
    ),
    UserWithPassword(
        id="2",
        email="trader@gmgn.ai",
        name="Pro Trader",
        wallets={
            "Primary": "9QwE3...7yH",
            "Backup": "2Mn8v...3kL"
        },
        balance=156.23,
        password="trader456",
        invite_code="TRADER456XYZ"  # This invite code is already used
    )
]