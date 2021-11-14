class Code:

    class Success:
        code = 200
        message = 'success'

    class NegativeAmount:
        code = 400
        message = 'amount cannot be negative'

    class Unauthorized:
        code = 401
        message = 'unauthorized'

    class InsufficientBalance:
        code = 402
        message = 'insufficient balance'

    class NotFound:
        code = 404
        message = 'not found'

    class InternalError:
        code = 500
        message = 'internal error'
