from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.users.schemas import DiscordUserSchema
from src.modules.auth.dependencies import get_current_user

from src.config import settings
from src.database import get_db_session
from src.modules.users.models import User 

from .service import DiscordAuthService
from .jwt import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.get("/discord/login")
async def discord_login():
    discord_url = (
        f"https://discord.com/api/oauth2/authorize"
        f"?client_id={settings.DISCORD_CLIENT_ID}"
        f"&redirect_uri={settings.DISCORD_REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=identify+email"
    )
    return RedirectResponse(url=discord_url)

@router.get("/callback")
async def discord_callback(
    code: str, 
    db: AsyncSession = Depends(get_db_session)
):
    discord_user_data = await DiscordAuthService.get_discord_user_data(code)
    
    if not discord_user_data:
        raise HTTPException(status_code=400, detail="Не удалось получить данные из Discord")

    validated_data = DiscordUserSchema(**discord_user_data)
    user = await DiscordAuthService.login_or_register_user(db, validated_data)

    access_token = create_access_token(
        data={"sub": str(user.id)}
    )

    redirect_url = f"{settings.FRONTEND_URL}/main"
    response = RedirectResponse(url=redirect_url)
    
    MAX_AGE_SECONDS = settings.ACCESS_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
    response.set_cookie(
        key="auth_token",
        value=access_token,
        httponly=True,   
        secure=False,   
        samesite="lax",
        max_age=MAX_AGE_SECONDS     
    )

    return response

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(
        key="auth_token",
        httponly=True,
        samesite="lax",
        secure=False
    )
    return {"detail": "Удачный выход"}

@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user