
from pydantic import BaseModel
from redis import Redis
import logging
from config import settings
from exceptions import PeerAlreadyExistsError
from schemas.peer import Peer, AddPeer

logger = logging.getLogger(__name__)
redis = Redis(
    host=settings.redis.connection.host,
    port=settings.redis.connection.port,
    db=settings.redis.db.users,
)

class PeerStorage(BaseModel):
    hash_name: str

    def save_peer(self, peer: Peer ) -> None:
        redis.hset(
            name=self.hash_name,
            key=peer.name,
            value=peer.model_dump_json(),
        )

    def get_by_public_key(self, public_key: str) -> Peer | None:
        if data := redis.hget(name=self.hash_name, key=public_key):
            logger.debug("Peer with key <s> was found", public_key)
            return Peer.model_validate_json(data)
        return None

    def exists(self, public_key: str) -> bool:
        return bool(
            redis.hexists(
                name=self.hash_name,
                key=public_key,
            )
        )

    def create(self, peer_in: AddPeer) -> Peer:
        peer = Peer(
            **peer_in.model_dump(),
        )
        self.save_peer(peer)
        logger.debug('Peer with key <s> was created', peer_in.public_key)
        return peer

    def create_or_raise_if_exists(self, peer_in: AddPeer) -> Peer:
        if not self.exists(peer_in.public_key):
            return self.create(peer_in)

        logger.error('Peer with key <s> already exists', peer_in.public_key)
        raise PeerAlreadyExistsError(peer_in.public_key)

    def delete_by_public_key(self, public_key: str) -> None:
        redis.hdel(
            self.hash_name,
            public_key,
        )

    def delete(self, peer: Peer) -> None:
        logger.info('Deleting peer <s> from storage', peer.public_key)
        self.delete_by_public_key(peer.public_key)


storage = PeerStorage(
    hash_name=settings.redis.collections.user_set,
)
