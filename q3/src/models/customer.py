import random
from abc import ABC

class Customer(ABC):
    """
    Abstract base class for all customer types in Dollmart e-commerce system.
    
    This class defines the common interface and functionality shared by
    different types of customers (personal and business clients).
    """
    
    # Track used customer IDs to ensure uniqueness
    _used_ids = set()
    
    def __init__(self, login_id, secret_key, shipping_location, client_category):
        """
        Initialize a customer with basic information.
        
        Args:
            login_id: Customer's username for login
            secret_key: Customer's password
            shipping_location: Customer's delivery address
            client_category: Type of customer account
        """
        # Generate a unique customer ID
        while True:
            potential_id = random.randint(1000, 9999)
            if potential_id not in Customer._used_ids:
                self.customer_id = potential_id
                Customer._used_ids.add(potential_id)
                break
                
        self.login_id = login_id
        self.secret_key = secret_key
        self.shipping_location = shipping_location
        self.client_category = client_category
        self.purchase_history = []
    
    def authenticate(self, provided_key):
        """
        Verify customer credentials for login.
        
        Args:
            provided_key: Password entered during login attempt
            
        Returns:
            Boolean indicating authentication success
        """
        return self.secret_key == provided_key
    
    def end_session(self):
        """
        End the current customer session.
        
        Returns:
            Boolean indicating logout success
        """
        return True
    
    def modify_profile(self, attribute, updated_value):
        """
        Update customer profile information.
        
        Args:
            attribute: Profile field to update
            updated_value: New value for the field
            
        Returns:
            Boolean indicating update success
        """
        if attribute == "secret_key":
            self.secret_key = updated_value
        elif attribute == "shipping_location":
            self.shipping_location = updated_value
        return True


class PersonalClient(Customer):
    """
    Represents an individual shopper in the Dollmart system.
    
    Personal clients have different shopping patterns and discount
    options compared to business clients.
    """
    
    def __init__(self, login_id, secret_key, shipping_location):
        """
        Initialize a personal client account.
        
        Args:
            login_id: Customer's username 
            secret_key: Customer's password
            shipping_location: Customer's delivery address
        """
        super().__init__(login_id, secret_key, shipping_location, "Personal")
        self.display_name = login_id.capitalize()
    
    def place_in_basket(self, item, quantity, basket):
        """
        Add an item to the customer's shopping basket.
        
        Args:
            item: The item to be added
            quantity: How many units to add
            basket: The shopping basket to update
            
        Returns:
            Boolean indicating if the item was successfully added
        """
        if item.inventory_count >= quantity:
            basket.add_product(self.customer_id, item, quantity)
            return True
        return False
    
    def validate_voucher(self, voucher_code, vouchers):
        """
        Check if a voucher code is valid for this customer.
        
        Args:
            voucher_code: Code entered by the customer
            vouchers: List of available vouchers
            
        Returns:
            Voucher object if valid, None otherwise
        """
        for voucher in vouchers:
            if voucher.code == voucher_code and voucher.is_valid():
                return voucher
        return None


class BusinessClient(Customer):
    """
    Represents a business or retail customer in the Dollmart system.
    
    Business clients can place bulk orders with special pricing
    and have tax identification for reporting purposes.
    """
    
    def __init__(self, login_id, secret_key, shipping_location):
        """
        Initialize a business client account.
        
        Args:
            login_id: Business account identifier
            secret_key: Authentication credential
            shipping_location: Business delivery address
        """
        super().__init__(login_id, secret_key, shipping_location, "Business")
        self.business_name = login_id.capitalize()
        # Generate tax ID for business accounting
        self.tax_id = f"TAX{random.randint(1000000000, 9999999999)}"
    
    def place_bulk_order(self, item, quantity, basket):
        """
        Add bulk orders to the basket with minimum quantity validation.
        
        Args:
            item: The item to be ordered
            quantity: Units to order
            basket: The basket object to update
            
        Returns:
            Boolean indicating if the bulk order was successfully added
        """
        min_bulk_quantity = 100  # Minimum bulk order size
        if quantity >= min_bulk_quantity and item.inventory_count >= quantity:
            basket.add_product(self.customer_id, item, quantity)
            return True
        return False
    
    def validate_voucher(self, voucher_code, vouchers):
        """
        Validate a voucher code for the business customer.
        
        Args:
            voucher_code: The code entered by the customer
            vouchers: List of available voucher objects
            
        Returns:
            Voucher object if valid, None otherwise
        """
        for voucher in vouchers:
            if voucher.code == voucher_code and voucher.is_valid():
                return voucher
        return None
