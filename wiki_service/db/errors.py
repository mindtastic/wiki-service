class EntityDoesNotExist(Exception):
    """Raised when entity was not found in database."""

class InvalidRequestEntity(Exception):
    """Raised when entity is not sufficient for a repository operation"""
