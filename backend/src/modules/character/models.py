
import uuid 
from datetime import datetime
from sqlalchemy import ForeignKey, String, DateTime
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship
from utils.db_mixins import IdMixin
from utils.enums import PlayerRole
from src.database import Base

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.modules.users import User


    
class Player(Base, IdMixin):
    __tablename__ = "players"
    
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    characters: Mapped[list["Character"]] = relationship("Character", back_populates="player", cascade="all, delete-orphan")
    
    name: Mapped[str] = mapped_column(String(128)) # Имя игрока в системе, не nicknama из дискорда.
    role: Mapped[PlayerRole] = mapped_column(ENUM(PlayerRole), default=PlayerRole.PLAYER)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    
    user: Mapped["User"] = relationship("User", back_populates="players")  # noqa: F821
    


class Character(Base, IdMixin):
    __tablename__ = "characters"
    
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id"))
    player: Mapped["Player"] = relationship("Player", back_populates="characters")
    
    name: Mapped[str] = mapped_column(String(128)) # Имя персонажа
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)