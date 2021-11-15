class BankServiceException:

    class NotFound(Exception):
        def __init__(self, message):
            super().__init__(message)

    class InternalError(Exception):
        def __init__(self, message):
            super().__init__(message)

    class Unauthorized(Exception):
        def __init__(self, message):
            super().__init__(message)

    class WrongInput(Exception):
        def __init__(self, message):
            super().__init__(message)

    class InsufficientBalance(Exception):
        def __init__(self, message):
            super().__init__(message)
