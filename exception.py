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


class ATMServiceException:

    class ReadCardException(Exception):
        def __init__(self, message):
            super().__init__(message)

    class WrongInput(Exception):
        def __init__(self, message):
            super().__init__(message)

    class InsufficientBalance(Exception):
        def __init__(self, message):
            super().__init__(message)


class CashBinException:

    class WrongInput(Exception):
        def __init__(self, message):
            super().__init__(message)

    class InsufficientReserve(Exception):
        def __init__(self, message):
            super().__init__(message)

