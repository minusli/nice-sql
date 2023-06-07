from nicesql.shortcut._base import SQL


def update(nsql: str, **kwargs) -> "Update":
    return Update(nsql, **kwargs)


class Update(SQL):
    def __init__(self, nsql: str, **kwargs):
        super().__init__(nsql, **kwargs)

    def execute(self, **kwargs) -> int:
        result = super().execute(**kwargs)
        return result.rowcount()
