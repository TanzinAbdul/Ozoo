"""
Staff classes for zoo personnel management.
"""

from core.exceptions import StaffError

class Staff:
    """
    Base class for all zoo staff members.
    
    Relationships:
        - Parent class for Zookeeper, etc.
    """
    
    def __init__(self, name: str, role: str, salary: float):
        """Initialize staff member with basic information."""
        self._name = name
        self._role = role
        self._salary = salary
        self._is_working = False
    
    def start_work(self) -> None:
        """Start staff member's work shift."""
        pass
    
    def end_work(self) -> None:
        """End staff member's work shift."""
        pass

class Zookeeper(Staff):
    """
    Zookeeper class for animal care staff.
    
    Relationships:
        - Inherits from Staff
        - Interacts with Animals and Enclosures
    """
    
    def __init__(self, name: str, salary: float, specialization: str = "general"):
        """Initialize zookeeper with specialization."""
        super().__init__(name, "Zookeeper", salary)
        self._specialization = specialization
    
    def feed_animals(self, enclosure: 'Enclosure') -> bool:
        """Feed all animals in specified enclosure."""
        pass
    
    def clean_enclosure(self, enclosure: 'Enclosure') -> bool:
        """Clean specified enclosure."""
        pass