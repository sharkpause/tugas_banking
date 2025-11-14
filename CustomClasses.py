class ValidationError(Exception):
    def __init__(self, errors):
        self.errors = errors

class DatabaseError(Exception):
    def __init__(self, errors):
        self.errors = errors

class InsufficientFundsError(Exception):
    def __init__(self, message="Saldo tidak mencukupi"):
        super().__init__(message)

class Status:
    ERROR: int = 1
    SUCCESS: int = 0

class ErrorType:
    VALIDATION: int = 1
    DATABASE: int = 2
    INSUFFICIENT_FUNDS: int = 3
    MISSING_ARGUMENT: int = 4

class ValidationErrorCode:
    EMPTY: int = 1
    INVALID_FORMAT: int = 2
    DUPLICATE: int = 3

class DataChanges:
    JUMLAH_SALDO: int = 1

class JenisTransaksi:
    DEPOSIT: int = 1
    WITHDRAW: int = 2
    TRANSFER: int = 3