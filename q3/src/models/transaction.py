import random

class Transaction:
    """
    Handles payment processing for purchases.
    
    This is a simplified implementation that would integrate with
    payment gateways in a production system.
    """
    
    def __init__(self, purchase, method, amount):
        """
        Initialize a new payment record.
        
        Args:
            purchase: Purchase this payment is for
            method: Payment method used (e.g., Card, Digital)
            amount: Payment amount
        """
        self.transaction_id = random.randint(100000, 999999)
        self.amount = amount
        self.method = method
        self.status = "Pending"  # Initial status before processing
    
    def create_receipt(self):
        """
        Generate a receipt string for the transaction.
        
        Returns:
            Receipt string with transaction ID and amount
        """
        return f"Receipt #{self.transaction_id} for ${self.amount:.2f}"
    
    def process_payment(self, payment_details):
        """
        Process a payment with the provided details.
        
        Args:
            payment_details: Dictionary with payment-specific information
            
        Returns:
            Boolean indicating payment success
        """
        # In a real system, this would validate payment details
        # and communicate with a payment processor API
        self.status = "Completed"
        return True
