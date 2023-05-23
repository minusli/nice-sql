class NotFoundError(RuntimeError):
    pass


class UnsupportedError(RuntimeError):
    pass


class NotImplementError(RuntimeError):
    pass


class DuplicateError(RuntimeError):
    pass


class BadRequestError(RuntimeError):
    pass


class InternalError(RuntimeError):
    pass


class AuthError(RuntimeError):
    pass
