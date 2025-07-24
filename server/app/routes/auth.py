from fastapi import APIRouter, HTTPException, status
from app.controllers.auth_controller import AuthController
from app.models.user import UserLogin, UserRegister, UserResponse

router= APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login")
async def login(credentials:UserLogin):
    try: 
        user= await AuthController.login(credentials)
        return user
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
    

@router.post("/signup")
def signup(user_date: UserRegister):    
    try:
        user= AuthController.register(user_date)
        return user
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
    
    



