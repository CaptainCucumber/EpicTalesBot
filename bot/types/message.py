from types import SimpleNamespace


class Message(SimpleNamespace):
    def __init__(self, **kwargs):
        super().__init__(**{k: self.dict_to_object(v) for k, v in kwargs.items()})

    @staticmethod
    def dict_to_object(d):
        if isinstance(d, dict):
            # Adjust the key name for 'from' to 'from_user' to avoid syntax error
            return Message(
                **{
                    (k if k != "from" else "from_user"): Message.dict_to_object(v)
                    for k, v in d.items()
                }
            )
        elif isinstance(d, list):
            return [Message.dict_to_object(v) for v in d]
        else:
            return d

    def __contains__(self, key):
        return hasattr(self, key)

    def get(self, key, default=None):
        return getattr(self, key, default)
