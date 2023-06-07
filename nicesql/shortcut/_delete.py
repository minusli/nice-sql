from nicesql.shortcut._base import SQL


def delete(nsql: str, **kwargs) -> "Delete":
    return Delete(nsql, **kwargs)


class Delete(SQL):
    def __init__(self, nsql: str, **kwargs):
        super().__init__(nsql, **kwargs)

    def execute(self, **kwargs) -> int:
        result = super().execute(**kwargs)
        return result.rowcount()
