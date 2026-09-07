from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class UsuarioModel(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    rol: Mapped[str] = mapped_column(String, nullable=False, default="user", server_default="user")

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "rol": self.rol,
        }


class AuditoriaModel(Base):
    __tablename__ = "auditoria"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    actor_id: Mapped[int] = mapped_column(Integer, nullable=False)
    accion: Mapped[str] = mapped_column(String, nullable=False)
    objetivo_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    entidad: Mapped[str | None] = mapped_column(String, nullable=True)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    fecha: Mapped[datetime | None] = mapped_column(
        DateTime,
        server_default=func.current_timestamp(),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "actor_id": self.actor_id,
            "accion": self.accion,
            "objetivo_id": self.objetivo_id,
            "entidad": self.entidad,
            "descripcion": self.descripcion,
            "fecha": str(self.fecha) if self.fecha is not None else None,
        }
