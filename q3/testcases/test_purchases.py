import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.customer import PersonalClient, BusinessClient
from src.models.item import Item
from src.models.purchase import Purchase
from src.models.shopping_basket import ShoppingBasket
from datetime import datetime, timedelta

class TestPurchaseCreation:
    """Tests for purchase creation functionality"""
    
    @pytest.fixture
    def sample_customer(self):
        """Fixture providing a sample customer for testing"""
        return PersonalClient("testuser", "password", "123 Test St")
    
    @pytest.fixture
    def sample_business_customer(self):
        """Fixture providing a sample business customer for testing"""
        return BusinessClient("business", "password", "456 Commerce Ave")
    
    @pytest.fixture
    def sample_items(self):
        """Fixture providing sample items for testing"""
        return [
            Item("Item A", "Description A", 10.00, "Test", 50),
            Item("Item B", "Description B", 20.00, "Test", 40)
        ]
    
    def test_direct_purchase_creation(self, sample_customer, sample_items):
        """Test creating a purchase directly without a basket"""
        items_list = [
            {"item": sample_items[0], "quantity": 2},
            {"item": sample_items[1], "quantity": 3}
        ]
        total_cost = (2 * 10.00) + (3 * 20.00)
        
        purchase = Purchase(sample_customer, items_list, total_cost)
        
        assert purchase.purchase_id > 0
        assert purchase.customer == sample_customer
        assert purchase.products_and_quantities == items_list
        assert purchase.original_cost == total_cost
        assert purchase.final_cost == total_cost
        assert purchase.status == "Pending"
        assert isinstance(purchase.purchase_date, datetime)
        assert purchase.shipment is not None
    
    def test_purchase_with_different_customers(self, sample_customer, sample_business_customer, sample_items):
        """Test creating purchases for different customer types"""
        # Personal customer purchase
        purchase1 = Purchase(sample_customer, [{"item": sample_items[0], "quantity": 1}], 10.00)
        
        # Business customer purchase
        purchase2 = Purchase(sample_business_customer, [{"item": sample_items[1], "quantity": 1}], 20.00)
        
        # Verify purchases are added to the correct customer histories
        assert purchase1 in sample_customer.purchase_history
        assert purchase2 in sample_business_customer.purchase_history
        assert purchase1 not in sample_business_customer.purchase_history
        assert purchase2 not in sample_customer.purchase_history
    
    def test_purchase_id_increments(self):
        """Test that purchase IDs auto-increment"""
        customer = PersonalClient("testuser", "password", "123 Test St")
        item = Item("Test Item", "Description", 10.00, "Test", 10)
        
        # Store the current purchase count
        initial_count = Purchase.purchase_count
        
        # Create purchases and check ID incrementation
        purchase1 = Purchase(customer, [{"item": item, "quantity": 1}], 10.00)
        purchase2 = Purchase(customer, [{"item": item, "quantity": 1}], 10.00)
        purchase3 = Purchase(customer, [{"item": item, "quantity": 1}], 10.00)
        
        assert purchase1.purchase_id == initial_count + 1
        assert purchase2.purchase_id == initial_count + 2
        assert purchase3.purchase_id == initial_count + 3
    
    def test_purchase_with_zero_items(self, sample_customer):
        """Test creating a purchase with empty item list"""
        # This is an edge case that might not be common but should be handled
        purchase = Purchase(sample_customer, [], 0.00)
        
        assert purchase.products_and_quantities == []
        assert purchase.original_cost == 0.00
        assert purchase.final_cost == 0.00
    
    def test_purchase_with_negative_discount(self, sample_customer, sample_items):
        """Test handling negative discount (should increase final price)"""
        # Another edge case - a negative discount is technically a surcharge
        purchase = Purchase(
            sample_customer, 
            [{"item": sample_items[0], "quantity": 1}], 
            10.00, 
            discount=-5.00
        )
        
        assert purchase.original_cost == 10.00
        assert purchase.final_cost == 15.00  # 10.00 - (-5.00) = 15.00
    
    def test_additional_discount_application(self, sample_customer, sample_items):
        """Test applying additional discounts after purchase creation"""
        purchase = Purchase(
            sample_customer, 
            [{"item": sample_items[0], "quantity": 1}], 
            100.00, 
            discount=10.00
        )
        
        assert purchase.original_cost == 100.00
        assert purchase.final_cost == 90.00  # After initial discount
        
        # Apply additional discount
        purchase.apply_additional_discount(20.00)
        assert purchase.final_cost == 80.00
        
        # Apply another discount
        purchase.apply_additional_discount(30.00)
        assert purchase.final_cost == 70.00
        
        # Apply discount that exceeds original price
        purchase.apply_additional_discount(150.00)
        assert purchase.final_cost == -50.00  # Negative price is possible in the current implementation


class TestPurchaseShipmentIntegration:
    """Tests for purchase and shipment integration"""
    
    def test_shipment_creation(self):
        """Test that a shipment is created with each purchase"""
        customer = PersonalClient("testuser", "password", "123 Test St")
        item = Item("Test Item", "Description", 10.00, "Test", 10)
        
        purchase = Purchase(customer, [{"item": item, "quantity": 1}], 10.00)
        
        assert purchase.shipment is not None
        assert purchase.shipment.purchase_id == purchase.purchase_id
        assert purchase.shipment.purchase == purchase  # Should reference back to purchase
    
    def test_purchase_status_updates(self):
        """Test that purchase status can be updated"""
        customer = PersonalClient("testuser", "password", "123 Test St")
        item = Item("Test Item", "Description", 10.00, "Test", 10)
        
        purchase = Purchase(customer, [{"item": item, "quantity": 1}], 10.00)
        
        # Default status should be "Pending"
        assert purchase.status == "Pending"
        
        # Manually update status
        purchase.status = "Processing"
        assert purchase.status == "Processing"
        
        purchase.status = "Completed"
        assert purchase.status == "Completed"
    
    def test_purchase_in_customer_history(self):
        """Test that purchases are added to customer history"""
        customer = PersonalClient("testuser", "password", "123 Test St")
        item = Item("Test Item", "Description", 10.00, "Test", 10)
        
        initial_history_count = len(customer.purchase_history)
        
        # Create multiple purchases
        purchase1 = Purchase(customer, [{"item": item, "quantity": 1}], 10.00)
        purchase2 = Purchase(customer, [{"item": item, "quantity": 2}], 20.00)
        
        # Check that both purchases were added to history
        assert len(customer.purchase_history) == initial_history_count + 2
        assert purchase1 in customer.purchase_history
        assert purchase2 in customer.purchase_history
