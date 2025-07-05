import time
import random
import threading
import os
from abc import ABC
from datetime import datetime, timedelta


class User(ABC):
    """
    Abstract base class for all user types in the e-commerce system.

    This class implements the common functionality shared between different
    types of users (individual and retail customers). Using an abstract base class
    allows for polymorphic behavior while enforcing a common interface.
    """

    def __init__(self, username, password, address, user_type):
        """
        Initialize a user with basic information.

        Uses random ID generation to ensure unique identification across the system.
        Orders list is initialized empty and populated as the user makes purchases.

        Args:
            username: User's login identifier
            password: User's authentication credential
            address: User's shipping address
            user_type: Categorizes the user for business logic purposes
        """
        self.userID = random.randint(
            1000, 9999
        )  # Random ID for database-free unique identification
        self.username = username
        self.password = password
        self.address = address
        self.userType = user_type
        self.orders = []  # Track user's order history

    def login(self, entered_password):
        """
        Authenticate a user based on password.

        Simple password comparison is used here for demonstration.

        Args:
            entered_password: The password provided during login attempt

        Returns:
            Boolean indicating whether authentication succeeded
        """
        return self.password == entered_password

    def logout(self):
        """
        Log out the current user.

        Returns:
            Boolean indicating logout success
        """
        return True

    def update_profile(self, field, new_value):
        """
        Update user profile information.

        Selective update approach allows changing specific fields while
        maintaining others, providing flexibility in profile management.

        Args:
            field: The profile attribute to be updated
            new_value: The new value for the specified attribute

        Returns:
            Boolean indicating update success
        """
        if field == "password":
            self.password = new_value
        elif field == "address":
            self.address = new_value
        return True


class IndividualCustomer(User):
    """
    Represents an individual retail customer in the e-commerce system.

    Extends the base User class with individual-specific functionality like
    personal shopping cart management and coupon redemption.
    """

    def __init__(self, username, password, address):
        """
        Initialize an individual customer account.

        Individual customers are distinguished from retail customers by
        type designation and have name capitalized for display purposes.

        Args:
            username: Customer's login identifier
            password: Customer's authentication credential
            address: Customer's shipping address
        """
        # Individual customer type is used for business rules like discounting
        super().__init__(username, password, address, "Individual")
        # For individual customers, username is treated as their personal name
        self.name = username.capitalize()

    def add_to_cart(self, product, quantity, cart):
        """
        Add a product to the customer's shopping cart with stock validation.

        Stock validation prevents orders that exceed available inventory,
        ensuring customers don't place orders that can't be fulfilled.

        Args:
            product: The product to be added
            quantity: How many units of the product to add
            cart: The cart object to update

        Returns:
            Boolean indicating if the product was successfully added
        """
        # Check inventory before adding to cart to prevent overselling
        if product.stockQuantity >= quantity:
            cart.add_item(self.userID, product, quantity)
            return True
        return False

    def check_coupon(self, coupon_code, coupons):
        """
        Validate a coupon code for the customer.

        Checks both existence and validity of the coupon to ensure
        it can be applied to the current order.

        Args:
            coupon_code: The code entered by the customer
            coupons: List of available coupon objects

        Returns:
            Coupon object if valid, None otherwise
        """
        # Linear search through available coupons
        for coupon in coupons:
            if coupon.couponCode == coupon_code:
                # Only return coupons that haven't expired
                if coupon.check_validity():
                    return coupon
        return None


class RetailCustomer(User):
    """
    Represents a business or retail customer in the e-commerce system.

    Retail customers have different purchasing patterns and requirements
    than individual customers, necessitating special business rules like
    minimum order quantities and GST identification.
    """

    def __init__(self, username, password, address):
        """
        Initialize a retail customer account with business-specific attributes.

        Generates a random GST number for tax purposes, which would
        normally be validated against a government database.

        Args:
            username: Business account identifier
            password: Authentication credential
            address: Business shipping address
        """
        super().__init__(username, password, address, "Retail")
        # For retail customers, name is treated as business name
        self.customerName = username.capitalize()
        # Generate a mock GST number for tax documentation
        self.GSTNo = f"GST{random.randint(1000000000, 9999999999)}"

    def add_bulk_order(self, product, quantity, cart):
        """
        Add bulk orders to the cart with minimum quantity validation.

        Ensures retail customers only place orders that meet minimum quantity
        requirements, which helps with inventory planning and wholesale pricing.

        Args:
            product: The product to be ordered in bulk
            quantity: How many units to order
            cart: The cart object to update

        Returns:
            Boolean indicating if the bulk order was successfully added
        """
        min_quantity = 100  # Minimum bulk order quantity
        # Validate both minimum order size and available stock
        if quantity >= min_quantity and product.stockQuantity >= quantity:
            cart.add_item(self.userID, product, quantity)
            return True
        return False

    def check_coupon(self, coupon_code, coupons):
        """
        Validate a coupon code for the retail customer.

        Implementation is identical to individual customers, but kept separate
        to allow for future differentiation in coupon policies.

        Args:
            coupon_code: The code entered by the customer
            coupons: List of available coupon objects

        Returns:
            Coupon object if valid, None otherwise
        """
        for coupon in coupons:
            if coupon.couponCode == coupon_code:
                if coupon.check_validity():
                    return coupon
        return None


class Product:
    """
    Represents a product available for purchase in the e-commerce system.

    Products encapsulate all information needed for display, inventory
    management, and order processing.
    """

    def __init__(self, name, description, price, category, stock_quantity):
        """
        Initialize a product with its essential attributes.

        Random product ID generation simplifies demonstration without
        requiring database auto-increment functionality.

        Args:
            name: Product display name
            description: Detailed product information
            price: Cost per unit
            category: Product classification for search/filtering
            stock_quantity: Available inventory
        """
        # Random ID for demonstration purposes
        self.productID = random.randint(1000, 9999)
        self.name = name
        self.description = description
        self.price = price
        self.category = category
        self.stockQuantity = stock_quantity

    def check_stock(self, quantity):
        """
        Verify if requested quantity is available in inventory.

        Separated from update_stock to allow stock checking without
        committing to inventory changes.

        Args:
            quantity: Number of units requested

        Returns:
            Boolean indicating if sufficient stock exists
        """
        return self.stockQuantity >= quantity

    def update_stock(self, quantity):
        """
        Reduce available inventory after a purchase.

        Includes validation to prevent negative inventory, which
        could occur with concurrent orders in a multi-user environment.

        Args:
            quantity: Number of units to remove from inventory

        Returns:
            Boolean indicating if the update was successful
        """
        if self.stockQuantity >= quantity:
            self.stockQuantity -= quantity
            return True
        return False


class Search:
    """
    Provides product search functionality using different criteria.

    Implemented as static methods to allow search operations without
    requiring an instance, simplifying the API for clients.
    """

    @staticmethod
    def search_keyword(products, keyword):
        """
        Search products by matching keywords in name or description.

        Case-insensitive search improves user experience by matching
        results regardless of capitalization.

        Args:
            products: List of product objects to search
            keyword: Search term to match

        Returns:
            List of matching product objects
        """
        results = []
        for product in products:
            # Case-insensitive search in both name and description for better results
            if (
                keyword.lower() in product.name.lower()
                or keyword.lower() in product.description.lower()
            ):
                results.append(product)
        return results

    @staticmethod
    def search_price(products, min_price, max_price):
        """
        Search products within a price range.

        Inclusive bounds on both minimum and maximum prices match
        user expectations for range filtering.

        Args:
            products: List of product objects to search
            min_price: Minimum price boundary (inclusive)
            max_price: Maximum price boundary (inclusive)

        Returns:
            List of products within the specified price range
        """
        results = []
        for product in products:
            # Inclusive bounds for intuitive range filtering
            if min_price <= product.price <= max_price:
                results.append(product)
        return results

    @staticmethod
    def search_category(products, category):
        """
        Search products by category.

        Case-insensitive matching improves usability by allowing
        flexible category input from users.

        Args:
            products: List of product objects to search
            category: Category to match

        Returns:
            List of products in the specified category
        """
        results = []
        for product in products:
            # Case-insensitive category matching
            if category.lower() == product.category.lower():
                results.append(product)
        return results


class Cart:
    """
    Manages shopping carts for multiple users in the system.

    Designed as a multi-user service that maintains isolated cart
    state for each customer, enabling concurrent shopping sessions.
    """

    def __init__(self):
        """
        Initialize the cart manager with an empty carts dictionary.

        Dictionary-based implementation allows O(1) access to any
        user's cart by their ID while keeping cart data isolated.
        """
        self.carts = {}  # Dictionary to store carts for different users

    def add_item(self, customer_id, product, quantity):
        """
        Add a product to a customer's cart.

        Handles both new cart creation and updates to existing items,
        automatically creating a new cart for first-time shoppers.

        Args:
            customer_id: Identifier for the customer's cart
            product: Product object to add
            quantity: Number of units to add

        Returns:
            Boolean indicating successful addition
        """
        # Create cart for new shopper if needed
        if customer_id not in self.carts:
            self.carts[customer_id] = {"itemsList": [], "total": 0}

        # Check if product already in cart for quantity aggregation
        for item in self.carts[customer_id]["itemsList"]:
            if item["product"].productID == product.productID:
                item["quantity"] += quantity
                self.carts[customer_id]["total"] += product.price * quantity
                return True

        # Add new product to cart if not found
        self.carts[customer_id]["itemsList"].append(
            {"product": product, "quantity": quantity}
        )
        self.carts[customer_id]["total"] += product.price * quantity
        return True

    def remove_item(self, customer_id, product_id):
        """
        Remove an item from a customer's cart.

        Updates the cart total to maintain consistency between
        item list and total price.

        Args:
            customer_id: Identifier for the customer's cart
            product_id: Product to remove

        Returns:
            Boolean indicating if removal was successful
        """
        if customer_id in self.carts:
            for i, item in enumerate(self.carts[customer_id]["itemsList"]):
                if item["product"].productID == product_id:
                    # Update cart total before removing item
                    self.carts[customer_id]["total"] -= (
                        item["product"].price * item["quantity"]
                    )
                    self.carts[customer_id]["itemsList"].pop(i)
                    return True
        return False

    def place_order(self, customer, payment_method, discount=0):
        """
        Convert a cart to an order and clear the cart.

        Creates an order record, updates inventory, and resets
        the customer's cart in a single transaction-like operation.

        Args:
            customer: Customer placing the order
            payment_method: Payment method used
            discount: Any discount applied to the order

        Returns:
            New Order object or None if cart is empty
        """
        # Verify cart exists and has items before proceeding
        if (
            customer.userID in self.carts
            and len(self.carts[customer.userID]["itemsList"]) > 0
        ):
            # Create a new order with a copy of cart contents
            order = Order(
                customer,
                self.carts[customer.userID]["itemsList"].copy(),
                self.carts[customer.userID]["total"],
                discount,
            )

            # Update product stock to reflect purchased quantities
            for item in self.carts[customer.userID]["itemsList"]:
                item["product"].update_stock(item["quantity"])

            # Clear the cart after successful order creation
            self.carts[customer.userID] = {"itemsList": [], "total": 0}

            return order
        return None

    def get_total(self, customer_id):
        """
        Get the current total value of a customer's cart.

        Provides a safe way to access cart totals without
        direct manipulation of the carts dictionary.

        Args:
            customer_id: Identifier for the customer's cart

        Returns:
            Total price of items in cart or 0 if cart doesn't exist
        """
        if customer_id in self.carts:
            return self.carts[customer_id]["total"]
        return 0

    def get_items(self, customer_id):
        """
        Get the items in a customer's cart.

        Provides read access to cart contents without exposing
        the underlying cart structure for modification.

        Args:
            customer_id: Identifier for the customer's cart

        Returns:
            List of items in cart or empty list if cart doesn't exist
        """
        if customer_id in self.carts:
            return self.carts[customer_id]["itemsList"]
        return []


class Order:
    """
    Represents a finalized customer order in the system.

    Orders are immutable records of purchases that include delivery
    tracking, payment details, and item information.
    """

    # Class variable to auto-increment order IDs across all orders
    order_count = 0

    def __init__(self, customer, items_list, total_amount, discount=0):
        """
        Create a new order from cart contents.

        Automatically creates a delivery record and adds the order
        to the customer's order history for tracking.

        Args:
            customer: Customer who placed the order
            items_list: Products and quantities ordered
            total_amount: Pre-discount total
            discount: Amount to subtract from total
        """
        Order.order_count += 1  # Auto-increment for sequential order IDs
        self.orderID = Order.order_count
        self.customer = customer
        self.itemsAndQuantitiesList = items_list
        self.totalAmount = total_amount
        self.discountedAmount = total_amount - discount
        self.status = "Pending"
        self.orderDate = datetime.now()

        # Create delivery for this order automatically
        self.delivery = Delivery(self.orderID, self)

        # Add this order to customer's order history
        customer.orders.append(self)

    def get_total(self):
        """
        Get the original total amount of the order.

        Separate from discounted amount to allow order analysis
        and discount impact tracking.

        Returns:
            Original total price before discounts
        """
        return self.totalAmount

    def apply_discount(self, discount):
        """
        Apply a discount to the order after creation.

        Allows for post-order discount adjustments such as
        customer service goodwill discounts.

        Args:
            discount: Amount to subtract from total

        Returns:
            New discounted total
        """
        self.discountedAmount = self.totalAmount - discount
        return self.discountedAmount


class Delivery:
    """
    Manages the delivery process for an order.

    Includes status tracking, estimated delivery dates, and
    automated status updates to simulate real delivery progression.
    """

    def __init__(self, order_id, order=None):
        """
        Initialize delivery tracking for an order.

        Creates a unique tracking ID and starts an automated status
        update process to simulate real-world delivery progression.

        Args:
            order_id: The order this delivery is associated with
            order: Reference to the Order object
        """
        self.deliveryID = random.randint(10000, 99999)
        self.orderID = order_id
        self.order = order  # Store reference to the order object
        self.status = "Processing"
        # Set estimated delivery 3 days from now
        self.deliveryDate = datetime.now() + timedelta(days=3)
        # Generate tracking number for customer reference
        self.trackingNumber = f"TRK{random.randint(1000000, 9999999)}"

        # Start background thread to automatically update delivery status
        self.status_thread = threading.Thread(target=self.auto_update_status)
        self.status_thread.daemon = True  # Don't block program exit
        self.status_thread.start()

    def track_delivery(self):
        """
        Get current delivery status information.

        Returns structured data rather than raw attributes to
        provide a clean interface for UI display.

        Returns:
            Dictionary with status, estimated delivery date, and tracking number
        """
        return {
            "status": self.status,
            "estimated_delivery": self.deliveryDate.strftime("%Y-%m-%d"),
            "tracking_number": self.trackingNumber,
        }

    def update_status(self, status):
        """
        Manually update the delivery status.

        Allows for manual status adjustments by system operators
        in case of exceptions or special circumstances.

        Args:
            status: New delivery status

        Returns:
            Boolean indicating update success
        """
        self.status = status
        return True

    def auto_update_status(self):
        """
        Automatically progress delivery through status stages.

        Background thread that simulates the natural progression
        of a delivery through various logistics stages.
        """
        statuses = ["Processing", "Packed", "Shipped", "Out for delivery", "Delivered"]
        current_index = 0

        # Progress through each status with a delay between changes
        while current_index < len(statuses):
            self.status = statuses[current_index]
            
            # Update order status to "Completed" when delivery is "Delivered"
            if self.status == "Delivered" and self.order is not None:
                self.order.status = "Completed"
                
            time.sleep(5)  # Update every 5 seconds for demo purposes
            current_index += 1


class Payment:
    """
    Handles payment processing for orders.

    Simplified implementation for demonstration purposes that would
    integrate with real payment gateways in a production system.
    """

    def __init__(self, order, method, amount):
        """
        Initialize a new payment record.

        Args:
            order: Order this payment is for
            method: Payment method used (e.g., Card, UPI)
            amount: Payment amount
        """
        self.paymentID = random.randint(100000, 999999)
        self.amount = amount
        self.method = method
        self.status = "Pending"  # Initial status before processing

    def generate_invoice(self):
        """
        Generate an invoice string for the payment.

        Simple implementation for demonstration that would create
        a formal invoice document in a production system.

        Returns:
            Invoice string with payment ID and amount
        """
        return f"Invoice #{self.paymentID} for ${self.amount:.2f}"

    def make_payment(self, payment_details):
        """
        Process a payment with the provided details.

        Simplified implementation that always succeeds, but would
        include gateway integration and validation in production.

        Args:
            payment_details: Dictionary with payment-specific information

        Returns:
            Boolean indicating payment success
        """
        self.status = "Paid"
        return True


class Coupon:
    """
    Represents a discount coupon in the system.

    Coupons have a limited validity period and provide percentage-based
    discounts on order totals.
    """

    def __init__(self, code, percentage, expiry_days=30):
        """
        Initialize a new coupon with an expiration date.

        Args:
            code: Unique coupon identifier
            percentage: Discount percentage
            expiry_days: Days until coupon expires
        """
        self.couponCode = code
        self.percentage = percentage
        # Set expiry date relative to creation time
        self.expiryDate = datetime.now() + timedelta(days=expiry_days)

    def check_validity(self):
        """
        Check if the coupon is still valid based on current date.

        Returns:
            Boolean indicating if coupon has not expired
        """
        return datetime.now() < self.expiryDate

    def calculate_amount(self, price):
        """
        Calculate the discount amount for a given price.

        Args:
            price: Order total to apply discount to

        Returns:
            Monetary amount to be discounted
        """
        return (price * self.percentage) / 100


# Initialize data
def initialize_data():
    """
    Create initial product catalog and promotion coupons.

    Generates a set of products across multiple categories,
    and random coupons with varying discounts to populate the system
    for demonstration purposes.

    Returns:
        Tuple containing product list and coupon list
    """
    # Create products with realistic data
    products = [
        # Electronics
        Product(
            "Bluetooth Headphones",
            "Noise-cancelling wireless headphones",
            179.99,
            "Electronics",
            150,
        ),
        Product(
            "Smartphone",
            "Latest model with 5G capabilities and dual camera",
            899.99,
            "Electronics",
            120,
        ),
        Product(
            "Webcam",
            "1080p HD webcam with built-in microphone",
            69.99,
            "Electronics",
            200,
        ),
        # Clothing
        Product(
            "Cotton T-Shirt", "Premium quality cotton t-shirt", 19.99, "Clothing", 500
        ),
        Product("Denim Jeans", "Slim fit denim jeans", 59.99, "Clothing", 300),
        Product(
            "Formal Shirt",
            "Business casual button-up shirt",
            45.99,
            "Clothing",
            250,
        ),
        Product(
            "Winter Jacket",
            "Waterproof insulated winter coat",
            129.99,
            "Clothing",
            100,
        ),
        Product(
            "Summer Dress",
            "Light floral pattern dress",
            39.99,
            "Clothing",
            200,
        ),
        Product(
            "Hoodie",
            "Comfortable cotton-blend hoodie",
            34.99,
            "Clothing",
            350,
        ),
        # Footwear
        Product(
            "Sports Shoes", "Running shoes with cushioned sole", 89.99, "Footwear", 200
        ),
        Product(
            "Leather Boots",
            "Waterproof leather hiking boots",
            149.99,
            "Footwear",
            150,
        ),
        Product(
            "Casual Sneakers",
            "Everyday comfortable sneakers",
            59.99,
            "Footwear",
            250,
        ),
        Product(
            "Formal Shoes",
            "Classic leather dress shoes",
            129.99,
            "Footwear",
            100,
        ),
        # Health & Fitness
        Product("Protein Powder", "Whey protein supplement, 2kg", 39.99, "Health", 150),
        Product("Yoga Mat", "Non-slip yoga mat", 29.99, "Sports", 200),
        Product(
            "Dumbbells Set",
            "Adjustable weights from 5-25kg",
            199.99,
            "Sports",
            75,
        ),
        Product(
            "Fitness Tracker",
            "Water-resistant activity tracker",
            79.99,
            "Health",
            180,
        ),
        # Home & Kitchen
        Product(
            "Coffee Maker",
            "Programmable drip coffee machine",
            79.99,
            "Kitchen",
            100,
        ),
        Product(
            "Blender",
            "High-speed blender for smoothies",
            59.99,
            "Kitchen",
            120,
        ),
        Product(
            "Cutlery Set",
            "24-piece stainless steel cutlery set",
            49.99,
            "Kitchen",
            150,
        ),
        Product(
            "Bedding Set",
            "Cotton queen size bedding with 4 pillowcases",
            89.99,
            "Home",
            100,
        ),
        Product(
            "Table Lamp",
            "Modern design with adjustable brightness",
            39.99,
            "Home",
            200,
        ),
        # Books
        Product(
            "Programming Book",
            "Learn Python the Hard Way",
            34.99,
            "Books",
            150,
        ),
        Product(
            "Fiction Novel",
            "Bestselling thriller paperback",
            14.99,
            "Books",
            250,
        ),
        # Beauty & Personal Care
        Product(
            "Face Cream",
            "Anti-aging moisturizer, 50ml",
            24.99,
            "Beauty",
            200,
        ),
        Product(
            "Shampoo",
            "Organic hair care product, 250ml",
            12.99,
            "Beauty",
            300,
        ),
        Product(
            "Electric Toothbrush",
            "Rechargeable with 5 cleaning modes",
            49.99,
            "Personal Care",
            120,
        ),
        # Toys & Games
        Product(
            "Board Game",
            "Strategic family board game",
            29.99,
            "Toys",
            100,
        ),
        Product(
            "Action Figure",
            "Collectible movie character figure",
            19.99,
            "Toys",
            150,
        ),
        Product(
            "Puzzle",
            "1000-piece landscape jigsaw puzzle",
            14.99,
            "Toys",
            200,
        ),
        # Outdoor & Garden
        Product(
            "Garden Tools Set",
            "5-piece gardening tools with storage bag",
            34.99,
            "Garden",
            80,
        ),
        Product(
            "Camping Tent",
            "4-person waterproof tent",
            129.99,
            "Outdoor",
            50,
        ),
    ]

    # Generate random coupon codes and discounts each time the program runs
    # to demonstrate dynamic promotion capabilities
    coupon_prefixes = [
        "WELCOME",
        "SAVE",
        "MISSEDYOU",
        "SUPER",
        "DEAL",
        "SALE",
        "DISCOUNT",
    ]
    coupon_discounts = [7, 10, 17, 24, 31, 42, 50, 100]  # Possible discount percentages

    coupons = []
    # Generate 4 unique random coupons for demonstration
    for _ in range(4):
        prefix = random.choice(coupon_prefixes)
        discount = random.choice(coupon_discounts)
        suffix = random.randint(10, 99)
        code = f"{prefix}{suffix}"
        # Set random expiry days between 10 and 45 days for variety
        expiry_days = random.randint(10, 45)
        coupons.append(Coupon(code, discount, expiry_days))

    return products, coupons


# Helper functions for UI
def clear_screen():
    """
    Clear the terminal screen for better UI experience.

    Cross-platform implementation that works on both Windows and Unix-based systems.
    """
    os.system("cls" if os.name == "nt" else "clear")


def display_ascii_art():
    """
    Display application logo in ASCII art.

    Provides a visual identity for the application and enhances
    user experience with a branded interface.
    """
    print(
        r"""
$$$$$$$\   $$$$$$\  $$\       $$\       $$\      $$\  $$$$$$\  $$$$$$$\ $$$$$$$$\ 
$$  __$$\ $$  __$$\ $$ |      $$ |      $$$\    $$$ |$$  __$$\ $$  __$$\\__$$  __|
$$ |  $$ |$$ /  $$ |$$ |      $$ |      $$$$\  $$$$ |$$ /  $$ |$$ |  $$ |  $$ |   
$$ |  $$ |$$ |  $$ |$$ |      $$ |      $$\$$\$$ $$ |$$$$$$$$ |$$$$$$$  |  $$ |   
$$ |  $$ |$$ |  $$ |$$ |      $$ |      $$ \$$$  $$ |$$  __$$ |$$  __$$<   $$ |   
$$ |  $$ |$$ |  $$ |$$ |      $$ |      $$ |\$  /$$ |$$ |  $$ |$$ |  $$ |  $$ |   
$$$$$$$  | $$$$$$  |$$$$$$$$\ $$$$$$$$\ $$ | \_/ $$ |$$ |  $$ |$$ |  $$ |  $$ |   
\_______/  \______/ \________|\________|\__|     \__|\__|  \__|\__|  \__|  \__|   
"""
    )


# Main Application
def main():
    """
    Entry point for the e-commerce application.

    Implements the main application loop and user interface flow,
    handling user authentication, product browsing, cart management,
    checkout processes, and account management.
    """
    # Initialize system with products and promotions
    products, coupons = initialize_data()
    users = []  # In-memory user database
    cart = Cart()  # Centralized cart manager
    current_user = None  # Track logged-in user

    # Main application loop
    while True:
        clear_screen()
        display_ascii_art()

        # Authentication flow when no user is logged in
        if current_user is None:
            print("\n1. Login")
            print("2. Register")
            print("3. Exit")

            choice = input("\nEnter your choice: ")

            if choice == "1":
                username = input("\nEnter your username: ")
                password = input("Enter your password: ")

                user_found = False
                for user in users:
                    if user.username == username:
                        if user.login(password):
                            current_user = user
                            user_found = True
                            print(f"\nWelcome {current_user.username.capitalize()}!")
                            time.sleep(1)
                            break

                if not user_found:
                    print("\nInvalid username or password!")
                    time.sleep(2)

            elif choice == "2":
                username = input("\nEnter your username: ")
                # Check if username already exists
                if any(user.username == username for user in users):
                    print("\nUsername already exists!")
                    time.sleep(2)
                    continue

                password = input("Enter your password: ")
                address = input("Enter your address: ")
                user_type = input("Enter 0 for Individual Customer, else 1: ")

                if user_type == "0":
                    new_user = IndividualCustomer(username, password, address)
                elif user_type == "1":
                    new_user = RetailCustomer(username, password, address)
                else:
                    print("\nInvalid user type!")
                    time.sleep(2)
                    continue

                users.append(new_user)
                print("\nAccount created successfully!")
                time.sleep(1)

            elif choice == "3":
                print("\nGoodbye!")
                break

            else:
                print("\nInvalid choice!")
                time.sleep(1)

        else:  # User is logged in
            print(f"\n1. View Products")
            print("2. Search Products")
            print("3. View Cart")
            print("4. Track Orders")
            print("5. Update Profile")
            print("6. Logout")
            print("7. Delete Account")

            choice = input("\nEnter your choice: ")

            if choice == "1":  # View Products
                while True:
                    clear_screen()
                    print("\n=== PRODUCTS ===\n")
                    for i, product in enumerate(products, 1):
                        print(
                            f"{i}. {product.name} - ${product.price:.2f} - {product.stockQuantity} units"
                        )
                        print(f"   Description: {product.description}")
                        print(f"   Category: {product.category}\n")

                    choice = input(
                        "\nEnter product number to add to cart (0 to return to menu): "
                    )

                    if choice == "0":
                        break

                    try:
                        product_index = int(choice) - 1
                        if 0 <= product_index < len(products):
                            if current_user.userType == "Individual":
                                quantity = int(input("Enter the quantity: "))
                                if current_user.add_to_cart(
                                    products[product_index], quantity, cart
                                ):
                                    print(
                                        f"\n{quantity} units of {products[product_index].name} added to cart!"
                                    )
                                else:
                                    print("\nNot enough stock available!")
                            else:  # Retail customer
                                quantity = int(
                                    input(f"Enter the quantity (minimum 100): ")
                                )
                                if current_user.add_bulk_order(
                                    products[product_index], quantity, cart
                                ):
                                    print(
                                        f"\n{quantity} units of {products[product_index].name} added to cart!"
                                    )
                                else:
                                    print(
                                        "\nNot enough stock or below minimum bulk order quantity!"
                                    )
                        else:
                            print("\nInvalid product number!")
                    except ValueError:
                        print("\nPlease enter a valid number!")

                    time.sleep(2)

            elif choice == "2":  # Search Products
                clear_screen()
                print("\n=== SEARCH PRODUCTS ===\n")
                print("1. Search by keyword")
                print("2. Search by price range")
                print("3. Search by category")

                search_choice = input("\nEnter your choice: ")

                if search_choice == "1":
                    keyword = input("\nEnter keyword to search: ")
                    results = Search.search_keyword(products, keyword)
                elif search_choice == "2":
                    min_price = float(input("\nEnter minimum price: "))
                    max_price = float(input("Enter maximum price: "))
                    results = Search.search_price(products, min_price, max_price)
                elif search_choice == "3":
                    # Show available categories
                    categories = set(product.category for product in products)
                    print("\nAvailable Categories:")
                    for i, cat in enumerate(categories, 1):
                        print(f"{i}. {cat}")

                    category = input("\nEnter category: ")
                    results = Search.search_category(products, category)
                else:
                    print("\nInvalid choice!")
                    time.sleep(2)
                    continue

                if results:
                    print("\nSearch Results:")
                    for i, product in enumerate(results, 1):
                        print(
                            f"{i}. {product.name} - ${product.price:.2f} - {product.stockQuantity} units"
                        )
                        print(f"   Description: {product.description}")
                        print(f"   Category: {product.category}\n")

                    choice = input(
                        "\nEnter product number to add to cart (0 to return to menu): "
                    )

                    if choice != "0":
                        try:
                            product_index = int(choice) - 1
                            if 0 <= product_index < len(results):
                                if current_user.userType == "Individual":
                                    quantity = int(input("Enter the quantity: "))
                                    if current_user.add_to_cart(
                                        results[product_index], quantity, cart
                                    ):
                                        print(
                                            f"\n{quantity} units of {results[product_index].name} added to cart!"
                                        )
                                    else:
                                        print("\nNot enough stock available!")
                                else:  # Retail customer
                                    quantity = int(
                                        input(f"Enter the quantity (minimum 100): ")
                                    )
                                    if current_user.add_bulk_order(
                                        results[product_index], quantity, cart
                                    ):
                                        print(
                                            f"\n{quantity} units of {results[product_index].name} added to cart!"
                                        )
                                    else:
                                        print(
                                            "\nNot enough stock or below minimum bulk order quantity!"
                                        )
                            else:
                                print("\nInvalid product number!")
                        except ValueError:
                            print("\nPlease enter a valid number!")
                else:
                    print("\nNo results found!")

                time.sleep(2)

            elif choice == "3":  # View Cart
                clear_screen()
                print("\n=== YOUR CART ===\n")

                cart_items = cart.get_items(current_user.userID)

                if not cart_items:
                    print("Your cart is empty. Add some items first!")
                    time.sleep(2)
                    continue

                total = 0
                for i, item in enumerate(cart_items, 1):
                    product = item["product"]
                    quantity = item["quantity"]
                    item_total = product.price * quantity
                    total += item_total
                    print(
                        f"{i}. {product.name} - ${product.price:.2f} x {quantity} = ${item_total:.2f}"
                    )

                print(f"\nTotal: ${total:.2f}")

                print("\n1. Checkout")
                print("2. Remove item")
                print("3. Return to menu")

                cart_choice = input("\nEnter your choice: ")

                if cart_choice == "1":  # Checkout
                    if cart_items:
                        # Apply discount for retail customers
                        discount = 0
                        if current_user.userType == "Retail":
                            discount = total * 0.05  # 5% discount for bulk purchase
                            print(f"\nTotal: ${total:.2f}")
                            print(
                                f"Discount for bulk purchase: ${discount:.2f} (5% off)"
                            )
                            total -= discount
                        else:
                            # Ask for coupon for individual customers only
                            has_coupon = input(
                                "\nEnter 0 if you have a coupon, else 1: "
                            )

                            if has_coupon == "0":
                                print("\nAvailable Coupons:")
                                for i, coupon in enumerate(coupons, 1):
                                    print(
                                        f"{i}. {coupon.couponCode} - {coupon.percentage}% off - Valid until {coupon.expiryDate.strftime('%Y-%m-%d')}"
                                    )

                                coupon_code = input(
                                    "\nEnter Coupon code (0 to cancel): "
                                )

                                if coupon_code != "0":
                                    coupon = current_user.check_coupon(
                                        coupon_code, coupons
                                    )
                                    if coupon:
                                        discount = coupon.calculate_amount(total)
                                        print("\nCoupon code applied successfully!")
                                        print(f"\nTotal: ${total:.2f}")
                                        print(f"Discount: ${discount:.2f}")
                                        print(
                                            f"\nTotal after discount: ${total - discount:.2f}"
                                        )
                                    else:
                                        print("\nInvalid or expired coupon code!")
                                        time.sleep(2)

                        print("\nChoose a payment method:")
                        print("\n1. Card")
                        print("2. UPI")

                        payment_choice = input("\nEnter your choice: ")

                        if payment_choice == "1":
                            # Card payment details
                            card_number = input("\nEnter your card number: ")
                            expiry_date = input("Enter your expiry date: ")
                            cvv = input("Enter your CVV: ")

                            # Process payment
                            payment = Payment(None, "Card", total - discount)
                            if payment.make_payment(
                                {
                                    "card_number": card_number,
                                    "expiry_date": expiry_date,
                                    "cvv": cvv,
                                }
                            ):
                                order = cart.place_order(current_user, "Card", discount)
                                print("\nPayment successful!")
                                print("\nThank you for shopping with us!")
                                print(f"Your order number is {order.orderID}")

                        elif payment_choice == "2":
                            # UPI payment details
                            upi_id = input("\nEnter your UPI ID: ")

                            # Process payment
                            payment = Payment(None, "UPI", total - discount)
                            if payment.make_payment({"upi_id": upi_id}):
                                order = cart.place_order(current_user, "UPI", discount)
                                print("\nPayment successful!")
                                print("\nThank you for shopping with us!")
                                print(f"Your order number is {order.orderID}")

                        else:
                            print("\nInvalid choice!")

                    else:
                        print("\nAdd items to the cart first!")

                elif cart_choice == "2":  # Remove item
                    item_index = int(input("\nEnter item number to remove: "))
                    if 1 <= item_index <= len(cart_items):
                        product_id = cart_items[item_index - 1]["product"].productID
                        if cart.remove_item(current_user.userID, product_id):
                            print("\nItem removed successfully!")
                        else:
                            print("\nFailed to remove item!")
                    else:
                        print("\nInvalid item number!")

                time.sleep(2)

            elif choice == "4":  # Track Orders
                clear_screen()
                print("\n=== YOUR ORDERS ===\n")

                if not current_user.orders:
                    print("You have no orders yet!")
                else:
                    for order in current_user.orders:
                        print(
                            f"Order {order.orderID} - ${order.discountedAmount:.2f} - {order.status}"
                        )
                        delivery_info = order.delivery.track_delivery()
                        print(
                            f"Delivery Status: {delivery_info['status']} (ETA: {delivery_info['estimated_delivery']})"
                        )
                        print(f"Tracking Number: {delivery_info['tracking_number']}\n")

                        # Show items in this order
                        print("Items:")
                        for item in order.itemsAndQuantitiesList:
                            product = item["product"]
                            quantity = item["quantity"]
                            print(
                                f"- {product.name} x {quantity} = ${product.price * quantity:.2f}"
                            )

                        print("--------------------")

                input("\nPress Enter to continue...")

            elif choice == "5":  # Update Profile
                clear_screen()
                print("\n=== UPDATE PROFILE ===\n")
                print("Choose what to update:")
                print("\n1. Password")
                print("2. Address")

                update_choice = input("\nEnter your choice: ")

                if update_choice == "1":
                    new_password = input("\nEnter your new password: ")
                    current_user.update_profile("password", new_password)
                    print("\nPassword updated successfully!")

                elif update_choice == "2":
                    new_address = input("\nEnter your new address: ")
                    current_user.update_profile("address", new_address)
                    print("\nAddress updated successfully!")

                else:
                    print("\nInvalid choice!")

                time.sleep(2)

            elif choice == "6":  # Logout
                current_user.logout()
                current_user = None
                print("\nLogged out successfully!")
                time.sleep(1)

            elif choice == "7":  # Delete Account
                confirm = input(
                    "\nAre you sure you want to delete your account? (y/n): "
                )
                if confirm.lower() == "y":
                    users.remove(current_user)
                    current_user = None
                    print("\nAccount deleted successfully!")
                    time.sleep(1)

            else:
                print("\nInvalid choice!")
                time.sleep(1)


if __name__ == "__main__":
    main()
