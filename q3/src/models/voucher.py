from datetime import datetime, timedelta

class Voucher:
    """
    Represents a discount voucher in the system.
    
    Vouchers have a limited validity period and provide percentage-based
    discounts on purchase totals.
    """
    
    def __init__(self, code, discount_percent, valid_days=30):
        """
        Initialize a new voucher with an expiration date.
        
        Args:
            code: Unique voucher identifier
            discount_percent: Discount percentage
            valid_days: Days until voucher expires
        """
        self.code = code
        self.discount_percent = discount_percent
        # Set expiry date relative to creation time
        self.expiry_date = datetime.now() + timedelta(days=valid_days)
    
    def is_valid(self):
        """
        Check if the voucher is still valid based on current date.
        
        Returns:
            Boolean indicating if voucher has not expired
        """
        # Include the entire expiry day by comparing dates, not datetimes
        return datetime.now().date() <= self.expiry_date.date()
    
    def calculate_discount(self, total_cost):
        """
        Calculate the discount amount for a given price.
        
        Args:
            total_cost: Purchase total to apply discount to
            
        Returns:
            Monetary amount to be discounted
        """
        return (total_cost * self.discount_percent) / 100
