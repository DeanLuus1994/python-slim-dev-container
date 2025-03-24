"""Custom exceptions for the functions module."""

class FunctionError(Exception):
    """Base exception for all function module errors."""
    pass

class ResourceError(FunctionError):
    """Raised when there's an issue with resource detection or allocation."""
    pass

class OptimizationError(FunctionError):
    """Raised when an optimization operation fails."""
    pass

class RepositoryError(FunctionError):
    """Raised when there's an issue with repository operations."""
    pass

class ConcurrencyError(FunctionError):
    """Raised when there's an issue with parallel execution."""
    pass

class UserInteractionError(FunctionError):
    """Raised when there's an issue with user interaction."""
    pass

class GPUError(ResourceError):
    """Raised when there's an issue with GPU detection or configuration."""
    pass

class CompilerError(OptimizationError):
    """Raised when there's an issue with compiler configuration."""
    pass

class GitError(RepositoryError):
    """Raised when there's an issue with Git operations."""
    def __init__(self, command: str, message: str, code: int = 1):
        self.command = command
        self.code = code
        super().__init__(f"Git command '{command}' failed: {message}")