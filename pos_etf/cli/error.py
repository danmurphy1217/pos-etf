class AddressError(Exception):
    
    def __init__(self, message: str):
        Exception.__init__(self, message)


class AccountNameError(Exception):

    def __init__(self, message: str = "Provided Account Name does not exist. Run `algoetf --signup` to begin."):
        self.message = message
        super().__init__(message)

class DuplicateAcctNameError(Exception):
    def __init__(self, msg: str):
        self.msg = msg
        super().__init__(msg)