class Entity:
    _id: str
    ENTITY_ID_PREFIX = ""

    __next_id = 0

    @classmethod
    def _generate_next_id(cls) -> str:
        cls.__next_id += 1
        return f"{cls.ENTITY_ID_PREFIX}{cls.__next_id:04}"

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
