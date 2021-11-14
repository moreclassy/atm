from logger import log_error


class ErrorHandler:

    @classmethod
    def inform_to_user(cls, error_message):
        print(error_message)  # Todo: inform error to user

    @classmethod
    def raise_error(cls, error):
        log_error(error)
        raise error
