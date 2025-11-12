"""
Custom exceptions for OzZoo simulation.
"""

class ZooError(Exception):
    """Base exception for zoo-related errors."""
    pass

class AnimalError(ZooError):
    """Exception raised for animal-related operations."""
    pass

class EnclosureError(ZooError):
    """Exception raised for enclosure-related operations."""
    pass

class StaffError(ZooError):
    """Exception raised for staff-related operations."""
    pass

class ResourceError(ZooError):
    """Exception raised for resource management issues."""
    pass

class FinancialError(ZooError):
    """Exception raised for financial operations."""
    def __init__(self, message: str, current_balance: float, required_amount: float):
        super().__init__(message)
        self.current_balance = current_balance
        self.required_amount = required_amount

class CompatibilityError(ZooError):
    """Exception raised for incompatible animal species."""
    def __init__(self, message: str, animal1_species: str, animal2_species: str):
        super().__init__(message)
        self.animal1_species = animal1_species
        self.animal2_species = animal2_species