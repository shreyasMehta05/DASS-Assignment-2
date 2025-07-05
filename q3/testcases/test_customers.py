import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.customer import PersonalClient, BusinessClient
from src.models.shopping_basket import ShoppingBasket
from src.models.item import Item
from src.models.voucher import Voucher
from datetime import datetime, timedelta

class TestCustomerCreation:
    """Tests for customer creation functionality"""
    
    def test_personal_client_creation(self):
        """Test basic personal client creation with valid parameters"""
        client = PersonalClient("john", "pass123", "123 Main St")
        
        assert client.login_id == "john"
        assert client.display_name == "John"
        assert client.secret_key == "pass123"
        assert client.shipping_location == "123 Main St"
        assert client.client_category == "Personal"
        assert client.purchase_history == []
        assert 1000 <= client.customer_id <= 9999  # Should be in this range
    
    def test_business_client_creation(self):
        """Test basic business client creation with valid parameters"""
        client = BusinessClient("acme", "business123", "456 Corp Ave")
        
        assert client.login_id == "acme"
        assert client.business_name == "Acme"
        assert client.secret_key == "business123"
        assert client.shipping_location == "456 Corp Ave"
        assert client.client_category == "Business"
        assert client.purchase_history == []
        assert 1000 <= client.customer_id <= 9999
        assert client.tax_id.startswith("TAX")
    
    def test_unique_customer_ids(self):
        """Test that multiple customers receive unique IDs"""
        customers = [PersonalClient(f"user{i}", "pass", "Address") for i in range(100)]
        ids = [c.customer_id for c in customers]
        # Check for uniqueness - should be equal to the length if all are unique
        assert len(set(ids)) == len(ids)
    
    def test_business_unique_tax_ids(self):
        """Test that business clients receive unique tax IDs"""
        businesses = [BusinessClient(f"business{i}", "pass", "Address") for i in range(100)]
        tax_ids = [b.tax_id for b in businesses]
        # All tax IDs should be unique
        assert len(set(tax_ids)) == len(tax_ids)

class TestCustomerAuthentication:
    """Tests for customer authentication functionality"""
    
    def test_successful_authentication(self):
        """Test successful authentication with correct credentials"""
        client = PersonalClient("alice", "secure123", "789 Oak Dr")
        assert client.authenticate("secure123") == True
    
    def test_failed_authentication(self):
        """Test failed authentication with incorrect credentials"""
        client = PersonalClient("alice", "secure123", "789 Oak Dr")
        assert client.authenticate("wrong_pass") == False
        assert client.authenticate("Secure123") == False  # Case-sensitive check
    
    def test_empty_password_authentication(self):
        """Test authentication with empty password"""
        client = PersonalClient("alice", "", "789 Oak Dr")
        assert client.authenticate("") == True
        assert client.authenticate("anypass") == False
    
    def test_end_session(self):
        """Test session termination"""
        client = PersonalClient("bob", "bob123", "101 Pine St")
        assert client.end_session() == True

class TestProfileModification:
    """Tests for profile modification functionality"""
    
    def test_update_password(self):
        """Test updating customer password"""
        client = PersonalClient("bob", "bob123", "101 Pine St")
        
        # Update password
        assert client.modify_profile("secret_key", "newpass123") == True
        assert client.secret_key == "newpass123"
        # Verify new password works for authentication
        assert client.authenticate("newpass123") == True
    
    def test_update_address(self):
        """Test updating customer address"""
        client = PersonalClient("bob", "bob123", "101 Pine St")
        
        # Update address
        assert client.modify_profile("shipping_location", "202 Elm St") == True
        assert client.shipping_location == "202 Elm St"
    
    def test_unknown_attribute_modification(self):
        """Test modifying an unknown attribute doesn't change anything"""
        client = PersonalClient("bob", "bob123", "101 Pine St")
        original_id = client.customer_id
        
        # Try to modify a non-modifiable field
        result = client.modify_profile("customer_id", 12345)
        
        # Should return True as the method doesn't raise an error
        assert result == True
        # But ID shouldn't change
        assert client.customer_id == original_id

class TestShoppingBasketInteractions:
    """Tests for customer interactions with shopping basket"""
    
    def test_personal_client_add_to_basket(self):
        """Test personal client adding items to basket"""
        client = PersonalClient("emma", "emma456", "303 Maple Ave")
        basket = ShoppingBasket()
        item = Item("Test Item", "A test item", 19.99, "Test", 10)
        
        # Test adding available item
        assert client.place_in_basket(item, 5, basket) == True
        
        # Check basket contents
        contents = basket.get_basket_contents(client.customer_id)
        assert len(contents) == 1
        assert contents[0]["item"].title == "Test Item"
        assert contents[0]["quantity"] == 5
    
    def test_personal_client_add_insufficient_inventory(self):
        """Test adding item with insufficient inventory"""
        client = PersonalClient("emma", "emma456", "303 Maple Ave")
        basket = ShoppingBasket()
        item = Item("Test Item", "A test item", 19.99, "Test", 10)
        
        # Try to add more than available
        assert client.place_in_basket(item, 15, basket) == False
        
        # Basket should be empty
        contents = basket.get_basket_contents(client.customer_id)
        assert len(contents) == 0
    
    def test_business_client_bulk_order(self):
        """Test business client placing bulk order"""
        client = BusinessClient("company", "corp789", "404 Business Blvd")
        basket = ShoppingBasket()
        item = Item("Bulk Item", "For business use", 9.99, "Bulk", 200)
        
        # Test adding valid bulk order
        assert client.place_bulk_order(item, 150, basket) == True
        
        # Check basket contents
        contents = basket.get_basket_contents(client.customer_id)
        assert len(contents) == 1
        assert contents[0]["item"].title == "Bulk Item"
        assert contents[0]["quantity"] == 150
    
    def test_business_client_below_minimum_quantity(self):
        """Test business client order below minimum quantity"""
        client = BusinessClient("company", "corp789", "404 Business Blvd")
        basket = ShoppingBasket()
        item = Item("Bulk Item", "For business use", 9.99, "Bulk", 200)
        
        # Try to add below minimum bulk quantity
        assert client.place_bulk_order(item, 50, basket) == False
        
        # Basket should be empty
        contents = basket.get_basket_contents(client.customer_id)
        assert len(contents) == 0
    
    def test_business_client_insufficient_inventory(self):
        """Test business client order with insufficient inventory"""
        client = BusinessClient("company", "corp789", "404 Business Blvd")
        basket = ShoppingBasket()
        item = Item("Bulk Item", "For business use", 9.99, "Bulk", 50)
        
        # Try to add more than available (even if above minimum quantity)
        assert client.place_bulk_order(item, 100, basket) == False
        
        # Basket should be empty
        contents = basket.get_basket_contents(client.customer_id)
        assert len(contents) == 0

class TestVoucherValidation:
    """Tests for voucher validation functionality"""
    
    def test_valid_voucher(self):
        """Test validating a valid voucher"""
        personal_client = PersonalClient("sam", "sam555", "505 Cedar St")
        business_client = BusinessClient("corp", "corp555", "606 Industry Way")
        
        # Create valid voucher
        valid_voucher = Voucher("VALID10", 10, 30)
        vouchers = [valid_voucher]
        
        # Both client types should be able to validate
        assert personal_client.validate_voucher("VALID10", vouchers) == valid_voucher
        assert business_client.validate_voucher("VALID10", vouchers) == valid_voucher
    
    def test_expired_voucher(self):
        """Test validating an expired voucher"""
        client = PersonalClient("sam", "sam555", "505 Cedar St")
        
        # Create expired voucher
        expired_voucher = Voucher("EXPIRED20", 20, -1)  # Expired yesterday
        vouchers = [expired_voucher]
        
        # Should return None for expired voucher
        assert client.validate_voucher("EXPIRED20", vouchers) is None
    
    def test_nonexistent_voucher(self):
        """Test validating a voucher that doesn't exist"""
        client = PersonalClient("sam", "sam555", "505 Cedar St")
        
        valid_voucher = Voucher("VALID10", 10, 30)
        vouchers = [valid_voucher]
        
        # Should return None for nonexistent voucher
        assert client.validate_voucher("NONEXISTENT", vouchers) is None
    
    def test_case_sensitive_voucher_code(self):
        """Test that voucher validation is case-sensitive"""
        client = PersonalClient("sam", "sam555", "505 Cedar St")
        
        valid_voucher = Voucher("UPPERCASE", 10, 30)
        vouchers = [valid_voucher]
        
        # Should return None for incorrect case
        assert client.validate_voucher("uppercase", vouchers) is None
