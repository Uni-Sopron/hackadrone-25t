from uuid import uuid4

class Entity:
    _id: str
    ENTITY_ID_PREFIX = ""

    @classmethod
    def _generate_next_id(cls) -> str:
        return cls.ENTITY_ID_PREFIX + "_" + uuid4().hex[:8]

    def __init__(self, **_):
        self._id = self._generate_next_id()

    def get_status(self, **kargs) -> dict:
        return {
            **self._public_status(),
            **(self._private_status() if self._can_access_private(**kargs) else {}),
        }

    def _can_access_private(self, **_) -> bool:
        return False

    def _public_status(self) -> dict:
        return {}

    def _private_status(self) -> dict:
        return {}
