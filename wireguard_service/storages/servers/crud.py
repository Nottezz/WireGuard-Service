import logging

from fastapi import HTTPException

from wireguard_service.schemas import ServerCreate, ServerUpdate, ServerRead
from wireguard_service.models import Server
from sqlalchemy.orm import Session
from sqlalchemy.future import select

logger = logging.getLogger(__name__)

def add_server(db: Session, server_in: ServerCreate) -> ServerRead:
    data = server_in.model_dump()
    data["host"] = str(data["host"])

    server = Server(**data)
    db.add(server)
    db.commit()
    db.refresh(server)

    logging.info("Server <%s> will be added", server.server_name)
    logging.debug("Server info: %s", server_in.model_dump())

    return ServerRead.model_validate(server)

def get_list_servers(db: Session) -> list[ServerRead]:
    stmt = select(Server).order_by(Server.id)
    servers = db.execute(stmt).scalars().all()

    return [ServerRead.model_validate(server) for server in servers]

def get_server(db: Session, server_name: str) -> ServerRead:
    stmt = select(Server).where(Server.server_name == server_name)
    result = db.execute(stmt).scalar()

    if not result:
        logger.error("Server <%s> not found", server_name)
        raise HTTPException(status_code=404, detail="Server <%s> not found" % server_name)

    return ServerRead.model_validate(result)

def partial_update_server_info(db: Session, server_update: ServerUpdate, server_name: str) -> ServerRead:
    stmt = select(Server).where(Server.server_name == server_name)
    server = db.execute(stmt).scalar()

    if not server:
        logger.error("Server <%s> not found", server_name)
        raise HTTPException(status_code=404, detail="Server <%s> not found" % server_name)

    for field, value in server_update.model_dump(exclude_unset=True).items():
        setattr(server, field, value)

    db.commit()
    db.refresh(server)

    logging.info("Server <%s> will be updated", server.server_name)

    return ServerRead.model_validate(server)


def delete_server(db: Session, server_name: str) -> ServerRead:
    result = db.execute(select(Server).where(Server.server_name == server_name))
    server = result.scalars().first()

    if not server:
        logger.error("Server <%s> not found", server_name)
        raise HTTPException(status_code=404, detail="Server <%s> not found" % server_name)

    db.delete(server)
    db.commit()

    logger.info("Server <%s> deleted", server_name)
    return ServerRead.model_validate(server)
