import types


class SqlModel:
    pass

    def fill(self, **kwargs) -> "SqlModel":
        for k, v in kwargs.items():
            if not hasattr(self, k):
                continue

            origin_v = getattr(self, k, None)
            if origin_v and isinstance(origin_v, types.FunctionType):
                continue

            setattr(self, k, v)

        return self
