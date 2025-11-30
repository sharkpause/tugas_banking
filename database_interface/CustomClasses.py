from enum import Enum

class ValidationError(Exception):
    def __init__(self, errors):
        self.errors = errors

class DatabaseError(Exception):
    def __init__(self, errors):
        self.errors = errors

class InsufficientFundsError(Exception):
    def __init__(self, message):
        super().__init__(message)

class TransactionError(Exception):
    def __init__(self, message):
        super().__init__(message)

class CredentialsError(Exception):
    def __init__(self, message):
        super().__init__(message)

class Status(Enum):
    ERROR = 1
    SUCCESS = 0

class ErrorType(Enum):
    VALIDATION = 1
    DATABASE = 2
    INSUFFICIENT_FUNDS = 3
    MISSING_ARGUMENT = 4
    CREDENTIALS = 5

class ValidationErrorCode(Enum):
    EMPTY = 1
    INVALID_FORMAT = 2
    DUPLICATE = 3

class DataChanges(Enum):
    JUMLAH_SALDO = 1

class JenisTransaksi(Enum):
    DEPOSIT = 1
    WITHDRAW = 2
    TRANSFER = 3
