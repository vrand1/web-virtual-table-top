import httpx
from fastapi import HTTPException, status
from sqlalchemy import select 
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.users.schemas import DiscordUserSchema
from src.modules.users.models import User 
from src.config import settings

class DiscordAuthService:
    @staticmethod
    async def get_discord_user_data(code: str) -> dict:
        async with httpx.AsyncClient() as client:
            token_url = "https://discord.com/api/oauth2/token"
            data = {
                "client_id": settings.DISCORD_CLIENT_ID,
                "client_secret": settings.DISCORD_CLIENT_SECRET,
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": settings.DISCORD_REDIRECT_URI,
            }
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            
            response = await client.post(token_url, data=data, headers=headers)
            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Discord error: {response.text}"
                )
            
            access_token = response.json().get("access_token")
            
            user_url = "https://discord.com/api/users/@me"
            user_headers = {"Authorization": f"Bearer {access_token}"}
            user_response = await client.get(user_url, headers=user_headers)
            if user_response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Discord error: {user_response.text}"
                )
                
            return user_response.json()
        
    @staticmethod   
    async def login_or_register_user(db: AsyncSession, discord_data: DiscordUserSchema):
        query = select(User).where(User.external_id == discord_data.id)
        result = await db.execute(query)
        user = result.scalar_one_or_none()

        if not user:
            user = User(
                external_id=discord_data.id,
                username=discord_data.username,
                email=discord_data.email,
                avatar=discord_data.avatar
            )
            db.add(user)
            await db.commit()
            await db.refresh(user)
        
        elif user.avatar != discord_data.avatar:
            user.avatar = discord_data.avatar
            await db.commit()
    
        return user