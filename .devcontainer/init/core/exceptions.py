"""Custom exceptions for the core module."""

class CoreError(Exception):
    """Base exception for all core module errors."""
    pass

class ConfigurationError(CoreError):
    """Raised when there is an issue with configuration loading or validation."""
    pass

class ValidationError(CoreError):
    """Raised when validation of inputs or paths fails."""
    pass

class EnvironmentError(CoreError):
    """Raised when there is an issue with environment variables."""
    pass

class SystemError(CoreError):
    """Raised when there is an issue with system operations."""
    pass

class ResourceError(CoreError):
    """Raised when there's an issue with resource detection or allocation."""
    pass

class CommandError(CoreError):
    """Raised when there's an issue executing a system command."""
    def __init__(self, command: str, return_code: int, output: str = "", error: str = ""):
        self.command = command
        self.return_code = return_code
        self.output = output
        self.error = error
        message = f"Command '{command}' failed with return code {return_code}"
        if error:
            message += f": {error}"
        super().__init__(message)