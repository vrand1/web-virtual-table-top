from sqlalchemy import Identity, Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column


class IdMixin:
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, server_default=Identity())
