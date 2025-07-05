import random

class Item:
    """
    Represents a product available for purchase in the Dollmart system.
    
    Items encapsulate all information needed for display, inventory
    management, and purchase processing.
    """
    
    # Track used IDs to ensure uniqueness
    _used_ids = set()
    
    def __init__(self, title, details, cost, classification, inventory_count):
        """
        Initialize an item with its essential attributes.
        
        Args:
            title: Item display name
            details: Detailed product description
            cost: Price per unit
            classification: Item category for search/filtering
            inventory_count: Available inventory
        """
        # Generate a unique ID
        while True:
            potential_id = random.randint(1000, 9999)
            if potential_id not in Item._used_ids:
                self.item_id = potential_id
                Item._used_ids.add(potential_id)
                break
                
        self.title = title
        self.details = details
        self.cost = cost
        self.classification = classification
        self.inventory_count = inventory_count
    
    def verify_availability(self, quantity):
        """
        Check if requested quantity is available in inventory.
        
        Args:
            quantity: Number of units requested
            
        Returns:
            Boolean indicating if sufficient inventory exists
        """
        return self.inventory_count >= quantity
    
    def reduce_inventory(self, quantity):
        """
        Reduce available inventory after a purchase.
        
        Args:
            quantity: Number of units to remove from inventory
            
        Returns:
            Boolean indicating if the update was successful
        """
        if self.inventory_count >= quantity:
            self.inventory_count -= quantity
            return True
        return False


class ItemFinder:
    """
    Provides item search functionality using different criteria.
    
    Implemented as a class with static methods to provide a clean
    interface for different search approaches.
    """
    
    @staticmethod
    def find_by_text(items, query):
        """
        Search items by matching text in name or description.
        
        Args:
            items: List of item objects to search
            query: Search term to match
            
        Returns:
            List of matching item objects
        """
        matches = []
        for item in items:
            if (query.lower() in item.title.lower() or
                    query.lower() in item.details.lower()):
                matches.append(item)
        return matches
    
    @staticmethod
    def find_by_price_range(items, min_cost, max_cost):
        """
        Find items within a specific price range.
        
        Args:
            items: List of item objects to search
            min_cost: Minimum price boundary (inclusive)
            max_cost: Maximum price boundary (inclusive)
            
        Returns:
            List of items within the specified price range
        """
        matches = []
        for item in items:
            if min_cost <= item.cost <= max_cost:
                matches.append(item)
        return matches
    
    @staticmethod
    def find_by_classification(items, classification):
        """
        Find items by their category/classification.
        
        Args:
            items: List of item objects to search
            classification: Category to match
            
        Returns:
            List of items in the specified category
        """
        matches = []
        for item in items:
            if classification.lower() == item.classification.lower():
                matches.append(item)
        return matches
