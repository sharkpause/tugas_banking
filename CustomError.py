class ValidationError(Exception):
    def __init__(self, errors):
        self.errors = errors

class DatabaseError(Exception):
    def __init__(self, errors):
        self.errors = errors

class Status:
    ERROR = 'error'
    SUCCESS = 'success'

class ErrorType:
    VALIDATION = 'validation'
    DATABASE = 'database'

class ValidationErrorCode:
    EMPTY = 'empty'
    INVALID_FORMAT = 'invalid format'
    DUPLICATE = 'duplicate'