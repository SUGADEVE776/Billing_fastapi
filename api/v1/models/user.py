from api.v1.models import AbstractBaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    String,
    Table,
    func,
    )


class User(AbstractBaseModel):

    __tablename__ = "user"

    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    username: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(1024), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)

    access_tokens = relationship(
        "AccessToken", back_populates="user", cascade="all, delete-orphan"
    )


    def __str__(self) -> str:
        return self.username