from fastapi import APIRouter, HTTPException, Depends, status
from app.models.user import UserLogin, UserRegister, User, AuthResponse
from app.services.auth_service import AuthService, get_current_user
from app.services.user_service import UserService

router = APIRouter(prefix="/auth", tags= ["Authentication"])


@router.post("/login", response_model=AuthResponse)
async def login(credentials:UserLogin):
    """
    User login endpoint
    - Take email and password
    -Return JWT token and user info
    """
    try:
        token = await AuthService.login(credentials)
        return AuthResponse(
            success=True,
            token=token,
            message = "Login successful"
        )
    
    except HTTPException as e:
        return AuthResponse(
            success=False,
            message=e.detail
        )

    except Exception as e:
        print(f'login error: {e}')
        return AuthResponse(
            success=False,
            message="Login failed. Please try again"
        )

@router.post("/signup", response_model=AuthResponse)
async def signup(user_data: UserRegister):
    try:
        user_dict= await AuthService.create_user(user_data)
        # Auto-login
        login_credentials= UserLogin(email=user_data.email, password=user_data.password)
        token= await AuthService.login(login_credentials)

        return AuthResponse(
            success=True,
            token=token,
            message="Registration successful!"
        )

    except HTTPException as e:
        return AuthResponse(
            success=False,
            message=e.detail
        )

    except Exception as e:
        print(f'login error: {e}')
        return AuthResponse(
            success=False,
            message="Login failed. Please try again"
        )
        
@router.get('/me',response_model=User)
async def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """
    Get current authenticated user profile
    - Require JWT token in Authorization header
    -Returns user information
    """

    return current_user

@router.post("/logout")
async def logout():
    """
    Logout endpoint
    - JWT tokens are stateless, so logout is client-side
    - Client should remove token from storage
    """
    return {
        "success": True, 
        "message": "Logged out successfully. Please remove token from client storage."
    }

@router.get('/protected')
async def protected_route(current_user: User= Depends(get_current_user)):
    """
    Example protected route for testing authentication
    """
    return {
        "message": f"Hello {current_user.name}! This is a protected route.",
        "user_id": current_user.id,
        "email": current_user.email,
        "balance": current_user.balance
    }
