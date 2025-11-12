"""
Resource Manager for tracking food, medicine, and finances.
Demonstrates encapsulation and exception handling.
"""

from core.exceptions import ResourceError, FinancialError
from typing import Dict

class ResourceManager:
    """
    Manages zoo resources including food, medicine, and finances.
    
    Attributes:
        _food_supply (Dict[str, float]): Food types and quantities in kg
        _medicine_supply (Dict[str, int]): Medicine types and quantities
        _funds (float): Available funds in dollars
        _daily_costs (float): Accumulated daily costs
    """
    
    def __init__(self, initial_funds: float = 100000.0):
        """
        Initialize resource manager with starting supplies.
        
        Args:
            initial_funds: Starting amount of money
        """
        self._food_supply = {
            "meat": 100.0,      # kg
            "fish": 50.0,       # kg
            "seeds": 200.0,     # kg
            "fruits": 150.0,    # kg
            "vegetables": 100.0,# kg
            "insects": 20.0     # kg
        }
        
        self._medicine_supply = {
            "vaccine": 10,
            "antibiotics": 15,
            "pain_reliever": 20,
            "vitamins": 25
        }
        
        self._funds = initial_funds
        self._daily_costs = 0.0
        self._daily_income = 0.0
    
    @property
    def funds(self) -> float:
        """Get current available funds."""
        return self._funds
    
    @property
    def food_supply(self) -> Dict[str, float]:
        """Get copy of food supply (encapsulation protection)."""
        return self._food_supply.copy()
    
    @property
    def medicine_supply(self) -> Dict[str, int]:
        """Get copy of medicine supply (encapsulation protection)."""
        return self._medicine_supply.copy()
    
    def spend_funds(self, amount: float, purpose: str = "expense") -> bool:
        """
        Spend funds if available.
        
        Args:
            amount: Amount to spend
            purpose: Description of the expense
            
        Returns:
            True if successful, False otherwise
            
        Raises:
            FinancialError: If insufficient funds
        """
        if amount < 0:
            raise FinancialError("Cannot spend negative amount", self._funds, amount)
        
        if self._funds >= amount:
            self._funds -= amount
            self._daily_costs += amount
            print(f"💰 Spent ${amount:.2f} on {purpose}. Remaining: ${self._funds:.2f}")
            return True
        else:
            raise FinancialError(
                f"Insufficient funds for {purpose}",
                self._funds,
                amount
            )
    
    def add_funds(self, amount: float, source: str = "income") -> None:
        """
        Add funds to zoo budget.
        
        Args:
            amount: Amount to add
            source: Source of the funds
        """
        if amount < 0:
            raise ValueError("Cannot add negative funds")
        
        self._funds += amount
        self._daily_income += amount
        print(f"💰 Added ${amount:.2f} from {source}. Total: ${self._funds:.2f}")
    
    def use_food(self, food_type: str, amount: float) -> bool:
        """
        Use food from supply if available.
        
        Args:
            food_type: Type of food to use
            amount: Amount to use in kg
            
        Returns:
            True if successful, False otherwise
        """
        if food_type not in self._food_supply:
            raise ResourceError(f"Unknown food type: {food_type}")
        
        if self._food_supply[food_type] >= amount:
            self._food_supply[food_type] -= amount
            return True
        else:
            raise ResourceError(
                f"Insufficient {food_type}. Available: {self._food_supply[food_type]:.1f}kg, "
                f"Required: {amount:.1f}kg"
            )
    
    def use_medicine(self, medicine_type: str, quantity: int = 1) -> bool:
        """
        Use medicine from supply if available.
        
        Args:
            medicine_type: Type of medicine to use
            quantity: Quantity to use
            
        Returns:
            True if successful, False otherwise
        """
        if medicine_type not in self._medicine_supply:
            raise ResourceError(f"Unknown medicine type: {medicine_type}")
        
        if self._medicine_supply[medicine_type] >= quantity:
            self._medicine_supply[medicine_type] -= quantity
            return True
        else:
            raise ResourceError(
                f"Insufficient {medicine_type}. Available: {self._medicine_supply[medicine_type]}, "
                f"Required: {quantity}"
            )
    
    def order_food(self, food_type: str, amount: float, cost_per_kg: float) -> bool:
        """
        Order food and add to supply.
        
        Args:
            food_type: Type of food to order
            amount: Amount to order in kg
            cost_per_kg: Cost per kilogram
            
        Returns:
            True if successful
        """
        total_cost = amount * cost_per_kg
        
        try:
            self.spend_funds(total_cost, f"ordering {amount}kg of {food_type}")
            
            if food_type in self._food_supply:
                self._food_supply[food_type] += amount
            else:
                self._food_supply[food_type] = amount
            
            print(f"📦 Ordered {amount}kg of {food_type}. New supply: {self._food_supply[food_type]:.1f}kg")
            return True
            
        except FinancialError as e:
            print(f"❌ Failed to order {food_type}: {e}")
            return False
    
    def order_medicine(self, medicine_type: str, quantity: int, cost_per_unit: float) -> bool:
        """
        Order medicine and add to supply.
        
        Args:
            medicine_type: Type of medicine to order
            quantity: Quantity to order
            cost_per_unit: Cost per unit
            
        Returns:
            True if successful
        """
        total_cost = quantity * cost_per_unit
        
        try:
            self.spend_funds(total_cost, f"ordering {quantity} units of {medicine_type}")
            
            if medicine_type in self._medicine_supply:
                self._medicine_supply[medicine_type] += quantity
            else:
                self._medicine_supply[medicine_type] = quantity
            
            print(f"💊 Ordered {quantity} units of {medicine_type}. New supply: {self._medicine_supply[medicine_type]}")
            return True
            
        except FinancialError as e:
            print(f"❌ Failed to order {medicine_type}: {e}")
            return False
    
    def get_resource_status(self) -> Dict:
        """
        Get comprehensive resource status.
        
        Returns:
            Dictionary with resource information
        """
        return {
            'funds': self._funds,
            'daily_costs': self._daily_costs,
            'daily_income': self._daily_income,
            'food_supply': self._food_supply.copy(),
            'medicine_supply': self._medicine_supply.copy()
        }
    
    def reset_daily_stats(self) -> None:
        """Reset daily cost and income tracking."""
        self._daily_costs = 0.0
        self._daily_income = 0.0