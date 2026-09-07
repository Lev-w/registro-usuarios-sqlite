from sqlalchemy import select

from app.modules.db.db import get_session
from app.modules.db.models import AuditoriaModel


def registrar_accion(actor_id, accion, objetivo_id=None, entidad=None, descripcion=None):
    session = get_session()
    try:
        session.add(AuditoriaModel(
            actor_id=actor_id,
            accion=accion,
            objetivo_id=objetivo_id,
            entidad=entidad,
            descripcion=descripcion,
        ))
        session.commit()
    finally:
        session.close()


def obtener_auditoria(filtros, orden, limit, offset):
    session = get_session()
    try:
        columnas_validas = {
            "id": AuditoriaModel.id,
            "objetivo_id": AuditoriaModel.objetivo_id,
            "fecha": AuditoriaModel.fecha,
            "actor_id": AuditoriaModel.actor_id,
        }
        columna_orden = columnas_validas.get(orden, AuditoriaModel.id)

        query = select(AuditoriaModel)

        if filtros.get("actor_id") is not None:
            query = query.where(AuditoriaModel.actor_id == filtros["actor_id"])

        if filtros.get("accion") is not None:
            query = query.where(AuditoriaModel.accion == filtros["accion"])

        if filtros.get("entidad") is not None:
            query = query.where(AuditoriaModel.entidad == filtros["entidad"])

        query = (
            query.order_by(columna_orden.desc())
            .limit(limit)
            .offset(offset)
        )

        logs = session.scalars(query).all()
        return [log.to_dict() for log in logs]
    finally:
        session.close()
