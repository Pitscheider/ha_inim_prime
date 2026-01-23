class InimPrimeError(Exception):
    """Base exception for all Inim Prime errors."""
    pass


class InimPrimeParamError(InimPrimeError):
    """Parameter error (ERROR_PARAM)."""
    pass


class InimPrimeApiKeyError(InimPrimeError):
    """Authentication error (ERROR_APIKEY)."""
    pass


class InimPrimeCommandError(InimPrimeError):
    """Command error (ERROR_COMMAND)."""
    pass


class InimPrimeExecutionError(InimPrimeError):
    """Execution error (ERROR_EXECUTION)."""
    pass


class InimPrimeProtocolError(InimPrimeError):
    """HTTPS/protocol error (ERROR_PROTOCOL)."""
    pass


class InimPrimeAuthorizationError(InimPrimeError):
    """Authorization error (ERROR_AUTHORIZATION)."""
    pass
