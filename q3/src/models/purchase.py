from datetime import datetime
from src.models.shipment import Shipment

class Purchase:
    """
    Represents a finalized customer order in the system.
    
    Purchases are immutable records of transactions that include
    delivery tracking, payment details, and item information.
    """
    
    # Class variable to auto-increment purchase IDs
    purchase_count = 0
    
    def __init__(self, customer, products_list, total_cost, discount=0):
        """
        Create a new purchase from basket contents.
        
        Args:
            customer: Customer who placed the order
            products_list: Items and quantities ordered
            total_cost: Pre-discount total
            discount: Amount to subtract from total
        """
        Purchase.purchase_count += 1
        self.purchase_id = Purchase.purchase_count
        self.customer = customer
        self.products_and_quantities = products_list
        self.original_cost = total_cost
        self.final_cost = total_cost - discount
        self.status = "Pending"
        self.purchase_date = datetime.now()
        
        # Create shipment for this purchase automatically
        self.shipment = Shipment(self.purchase_id, self)
        
        # Add this purchase to customer's history
        customer.purchase_history.append(self)
    
    def get_original_cost(self):
        """
        Get the pre-discount total cost of the purchase.
        
        Returns:
            Original total price before discounts
        """
        return self.original_cost
    
    def apply_additional_discount(self, discount_amount):
        """
        Apply an additional discount to the purchase.
        
        Args:
            discount_amount: Amount to subtract from total
            
        Returns:
            New discounted total
        """
        self.final_cost = self.original_cost - discount_amount
        return self.final_cost
