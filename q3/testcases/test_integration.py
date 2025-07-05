import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.customer import PersonalClient, BusinessClient
from src.models.item import Item, ItemFinder
from src.models.shopping_basket import ShoppingBasket
from src.models.purchase import Purchase
from src.models.shipment import Shipment
from src.models.transaction import Transaction
from src.models.voucher import Voucher
from datetime import datetime, timedelta

class TestEndToEndFlow:
    """Integration tests for the complete shopping flow"""
    
    def test_personal_customer_shopping_flow(self):
        """Test complete shopping flow for personal customer"""
        # 1. Create a customer
        customer = PersonalClient("john", "pass123", "123 Main St")
        
        # 2. Create some products
        product1 = Item("Laptop", "High-end laptop", 1200.00, "Electronics", 10)
        product2 = Item("Mouse", "Wireless mouse", 50.00, "Electronics", 20)
        
        # 3. Create a shopping basket
        basket = ShoppingBasket()
        
        # 4. Add products to the basket
        customer.place_in_basket(product1, 1, basket)
        customer.place_in_basket(product2, 2, basket)
        
        # Check basket contents
        contents = basket.get_basket_contents(customer.customer_id)
        assert len(contents) == 2
        assert contents[0]["item"].title == "Laptop"
        assert contents[0]["quantity"] == 1
        assert contents[1]["item"].title == "Mouse"
        assert contents[1]["quantity"] == 2
        
        # Calculate expected total
        expected_total = 1200.00 + (2 * 50.00)  # Fixed syntax error here
        assert basket.get_basket_value(customer.customer_id) == expected_total
        
        # 5. Apply a voucher discount
        voucher = Voucher("SAVE100", 10, 30)  # 10% discount
        discount = voucher.calculate_discount(expected_total)
        assert discount == 130.00  # 10% of 1300
        
        # 6. Checkout
        purchase = basket.checkout(customer, "Card", discount)
        
        # 7. Verify purchase details
        assert purchase is not None
        assert purchase.customer == customer
        assert purchase.original_cost == expected_total
        assert purchase.final_cost == expected_total - discount
        assert purchase.status == "Pending"
        
        # 8. Verify shipment creation
        assert purchase.shipment is not None
        assert purchase.shipment.status == "Processing"
        
        # 9. Verify inventory was updated
        assert product1.inventory_count == 9  # 10 - 1
        assert product2.inventory_count == 18  # 20 - 2
        
        # 10. Verify purchase is in customer history
        assert purchase in customer.purchase_history
    
    def test_business_customer_shopping_flow(self):
        """Test complete shopping flow for business customer with bulk orders"""
        # 1. Create a business customer
        business = BusinessClient("acme", "biz123", "456 Corp Ave")
        
        # 2. Create a product with enough inventory for bulk order
        product = Item("Office Chair", "Ergonomic chair", 200.00, "Furniture", 200)
        
        # 3. Create a shopping basket
        basket = ShoppingBasket()
        
        # 4. Place a bulk order (minimum 100 units)
        business.place_bulk_order(product, 150, basket)
        
        # Check basket contents
        contents = basket.get_basket_contents(business.customer_id)
        assert len(contents) == 1
        assert contents[0]["item"].title == "Office Chair"
        assert contents[0]["quantity"] == 150
        
        # Calculate expected total
        expected_total = 150 * 200.00
        assert basket.get_basket_value(business.customer_id) == expected_total
        
        # 5. Checkout (with special business discount)
        business_discount = expected_total * 0.05  # 5% business discount
        purchase = basket.checkout(business, "Bank Transfer", business_discount)
        
        # 6. Verify purchase details
        assert purchase is not None
        assert purchase.customer == business
        assert purchase.original_cost == expected_total
        assert purchase.final_cost == expected_total - business_discount
        
        # 7. Verify inventory was updated
        assert product.inventory_count == 50  # 200 - 150
        
        # 8. Create payment transaction
        transaction = Transaction(purchase, "Bank Transfer", purchase.final_cost)
        transaction.process_payment({"account": "123456789"})
        
        assert transaction.status == "Completed"
    
    def test_search_and_purchase_flow(self):
        """Test searching for products and purchasing them"""
        # 1. Create a customer
        customer = PersonalClient("alice", "alice123", "789 Oak Dr")
        
        # 2. Create a variety of products
        products = [
            Item("Gaming Laptop", "High-performance gaming laptop", 1500.00, "Electronics", 5),
            Item("Work Laptop", "Business laptop", 1000.00, "Electronics", 10),
            Item("Gaming Mouse", "RGB gaming mouse", 80.00, "Electronics", 20),
            Item("Office Chair", "Ergonomic chair", 250.00, "Furniture", 15)
        ]
        
        # 3. Search for products using different criteria
        # Search by text
        laptop_results = ItemFinder.find_by_text(products, "laptop")
        assert len(laptop_results) == 2
        
        # Search by price range
        expensive_results = ItemFinder.find_by_price_range(products, 1000, 2000)
        assert len(expensive_results) == 2
        
        # Search by category
        furniture_results = ItemFinder.find_by_classification(products, "Furniture")
        assert len(furniture_results) == 1
        assert furniture_results[0].title == "Office Chair"
        
        # 4. Add a searched product to basket
        basket = ShoppingBasket()
        mouse = ItemFinder.find_by_text(products, "Mouse")[0]
        customer.place_in_basket(mouse, 1, basket)
        
        # 5. Complete purchase
        purchase = basket.checkout(customer, "Digital")
        
        # 6. Verify purchase was successful
        assert purchase is not None
        assert purchase in customer.purchase_history
        assert mouse.inventory_count == 19  # 20 - 1