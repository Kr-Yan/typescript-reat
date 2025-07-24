# from app.models.user import User
# from app.models.user import UserWithPassword

from app.services.data_service import data_service


mock_users_with_passwords = data_service.load_users()

if not mock_users_with_passwords:
    from app.models.user import UserWithPassword
    default_users=[ UserWithPassword(
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
    )]

    mock_users_with_passwords.extend(default_users)
    data_service.save_users(mock_users_with_passwords)



