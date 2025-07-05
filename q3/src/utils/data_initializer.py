import random
from models.item import Item
from models.voucher import Voucher

def initialize_store_data():
    """
    Create initial product catalog and promotion vouchers.
    
    Generates a diverse set of items across multiple categories,
    and random vouchers with varying discounts to populate the system.
    
    Returns:
        Tuple containing items list and voucher list
    """
    # Create items with realistic data
    items = [
        # Electronics
        Item(
            "Wireless Earbuds",
            "Premium noise-cancelling wireless earbuds",
            159.99,
            "Electronics",
            150,
        ),
        Item(
            "Mobile Phone",
            "Latest model with high-resolution camera",
            899.99,
            "Electronics",
            120,
        ),
        Item(
            "HD Camera",
            "1080p high-definition camera with tripod",
            79.99,
            "Electronics",
            200,
        ),
        # Apparel
        Item(
            "Premium T-Shirt", "Soft cotton blend t-shirt", 24.99, "Apparel", 500
        ),
        Item("Designer Jeans", "Stylish slim fit denim", 79.99, "Apparel", 300),
        Item(
            "Business Shirt",
            "Wrinkle-resistant button-up shirt",
            49.99,
            "Apparel",
            250,
        ),
        Item(
            "Insulated Jacket",
            "Water-resistant winter jacket",
            149.99,
            "Apparel",
            100,
        ),
        Item(
            "Floral Dress",
            "Lightweight summer dress with floral pattern",
            39.99,
            "Apparel",
            200,
        ),
        Item(
            "Pullover",
            "Warm cotton-blend pullover hoodie",
            34.99,
            "Apparel",
            350,
        ),
        # Footwear
        Item(
            "Running Shoes", "Athletic shoes with arch support", 89.99, "Footwear", 200
        ),
        Item(
            "Hiking Boots",
            "Waterproof leather hiking boots",
            149.99,
            "Footwear",
            150,
        ),
        Item(
            "Canvas Sneakers",
            "Everyday casual sneakers",
            59.99,
            "Footwear",
            250,
        ),
        Item(
            "Dress Shoes",
            "Classic leather formal shoes",
            129.99,
            "Footwear",
            100,
        ),
        # Wellness
        Item("Whey Protein", "Pure whey protein supplement, 2kg", 39.99, "Wellness", 150),
        Item("Exercise Mat", "Non-slip exercise and yoga mat", 29.99, "Wellness", 200),
        Item(
            "Adjustable Weights",
            "Set of adjustable dumbbells, 5-25kg",
            199.99,
            "Wellness",
            75,
        ),
        Item(
            "Activity Monitor",
            "Waterproof fitness and activity tracker",
            79.99,
            "Wellness",
            180,
        ),
        # Home & Kitchen
        Item(
            "Coffee Machine",
            "Programmable espresso maker with milk frother",
            149.99,
            "Kitchen",
            90,
        ),
        Item(
            "Food Processor",
            "Multi-function food processor with attachments",
            129.99,
            "Kitchen",
            100,
        ),
        Item(
            "Cookware Set",
            "Non-stick cookware, 10-piece set",
            199.99,
            "Kitchen",
            75,
        ),
        Item(
            "Bedding Set",
            "Premium cotton queen size bedding set",
            89.99,
            "Home",
            120,
        ),
        Item(
            "Smart Lamp",
            "Voice-controlled, color-adjustable lamp",
            59.99,
            "Home",
            150,
        ),
    ]

    # Generate voucher codes with varied discounts and expiry dates
    voucher_prefixes = ["WELCOME", "SAVE", "HOLIDAY", "SPECIAL", "DEAL"]
    discount_options = [10, 15, 20, 25, 30]
    
    vouchers = []
    
    # Create 5 different vouchers
    for i in range(5):
        code = f"{random.choice(voucher_prefixes)}{random.randint(10, 99)}"
        discount = random.choice(discount_options)
        # Valid days between 7 and 60
        valid_days = random.randint(7, 60)
        vouchers.append(Voucher(code, discount, valid_days))
    
    # Add one expired voucher for testing
    expired_code = f"EXPIRED{random.randint(10, 99)}"
    vouchers.append(Voucher(expired_code, 50, -5))  # Expired 5 days ago
    
    return items, vouchers
