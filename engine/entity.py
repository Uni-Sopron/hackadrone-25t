class Entity:

    def status(self, **kargs) -> dict:
        return {
            **self._public_status(),
            **(self._private_status() if self._can_access_private(**kargs) else {})
        }

    def _can_access_private(self, **kargs) -> bool:
        return False

    def _public_status(self) -> dict:
        return {}

    def _private_status(self) -> dict:
        return {}

