class ShoppingBasket:
    """
    Manages shopping baskets for multiple customers in the system.
    
    Designed as a multi-user service that maintains isolated basket
    state for each customer, enabling concurrent shopping sessions.
    """
    
    def __init__(self):
        """
        Initialize the basket manager with an empty baskets dictionary.
        
        Dictionary-based implementation allows O(1) access to any
        customer's basket by their ID while keeping basket data isolated.
        """
        self.baskets = {}  # Dictionary to store baskets by customer ID
    
    def add_product(self, customer_id, item, quantity):
        """
        Add an item to a customer's basket.
        
        Args:
            customer_id: Identifier for the customer's basket
            item: Item object to add
            quantity: Number of units to add
            
        Returns:
            Boolean indicating successful addition
        """
        # Create basket for new shopper if needed
        if customer_id not in self.baskets:
            self.baskets[customer_id] = {"product_list": [], "basket_value": 0}
        
        # Check if item already exists in basket
        for product in self.baskets[customer_id]["product_list"]:
            if product["item"].item_id == item.item_id:
                product["quantity"] += quantity
                self.baskets[customer_id]["basket_value"] += item.cost * quantity
                return True
        
        # Add new item to basket
        self.baskets[customer_id]["product_list"].append(
            {"item": item, "quantity": quantity}
        )
        self.baskets[customer_id]["basket_value"] += item.cost * quantity
        return True
    
    def remove_product(self, customer_id, item_id):
        """
        Remove an item from a customer's basket.
        
        Args:
            customer_id: Identifier for the customer's basket
            item_id: Item to remove
            
        Returns:
            Boolean indicating if removal was successful
        """
        if customer_id in self.baskets:
            for i, product in enumerate(self.baskets[customer_id]["product_list"]):
                if product["item"].item_id == item_id:
                    # Update total before removing item
                    self.baskets[customer_id]["basket_value"] -= (
                        product["item"].cost * product["quantity"]
                    )
                    self.baskets[customer_id]["product_list"].pop(i)
                    return True
        return False
    
    def checkout(self, customer, payment_method, discount=0):
        """
        Convert a basket to a purchase and clear the basket.
        
        Args:
            customer: Customer placing the order
            payment_method: Payment method used
            discount: Any discount applied
            
        Returns:
            New Purchase object or None if basket is empty
        """
        # Import here to avoid circular imports
        from src.models.purchase import Purchase
        
        # Verify basket exists and has items
        if (customer.customer_id in self.baskets and 
                len(self.baskets[customer.customer_id]["product_list"]) > 0):
            
            # Create purchase with a copy of basket contents
            purchase = Purchase(
                customer,
                self.baskets[customer.customer_id]["product_list"].copy(),
                self.baskets[customer.customer_id]["basket_value"],
                discount,
            )
            
            # Update inventory for purchased items
            for product in self.baskets[customer.customer_id]["product_list"]:
                product["item"].reduce_inventory(product["quantity"])
            
            # Reset the customer's basket
            self.baskets[customer.customer_id] = {"product_list": [], "basket_value": 0}
            
            return purchase
        return None
    
    def get_basket_value(self, customer_id):
        """
        Get the current total value of a customer's basket.
        
        Args:
            customer_id: Identifier for the customer's basket
            
        Returns:
            Total price of items in basket or 0 if basket doesn't exist
        """
        if customer_id in self.baskets:
            return self.baskets[customer_id]["basket_value"]
        return 0
    
    def get_basket_contents(self, customer_id):
        """
        Get the items in a customer's basket.
        
        Args:
            customer_id: Identifier for the customer's basket
            
        Returns:
            List of items in basket or empty list if basket doesn't exist
        """
        if customer_id in self.baskets:
            return self.baskets[customer_id]["product_list"]
        return []
