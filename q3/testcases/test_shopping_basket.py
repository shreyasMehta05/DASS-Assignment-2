import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.shopping_basket import ShoppingBasket
from src.models.item import Item
from src.models.customer import PersonalClient, BusinessClient

class TestShoppingBasket:
    """Tests for shopping basket functionality"""
    
    @pytest.fixture
    def sample_basket(self):
        """Fixture providing a fresh shopping basket for each test"""
        return ShoppingBasket()
    
    @pytest.fixture
    def sample_customer(self):
        """Fixture providing a sample customer for basket tests"""
        return PersonalClient("test_user", "password", "123 Test St")
    
    @pytest.fixture
    def sample_items(self):
        """Fixture providing sample items for testing"""
        return [
            Item("Item A", "Description A", 10.00, "Test", 100),
            Item("Item B", "Description B", 20.00, "Test", 100),
            Item("Item C", "Description C", 30.00, "Test", 100),
        ]
    
    def test_add_product_new_basket(self, sample_basket, sample_customer, sample_items):
        """Test adding a product to a new basket"""
        customer_id = sample_customer.customer_id
        item = sample_items[0]
        
        # Add product to basket
        assert sample_basket.add_product(customer_id, item, 2) == True
        
        # Check basket contents
        contents = sample_basket.get_basket_contents(customer_id)
        assert len(contents) == 1
        assert contents[0]["item"].item_id == item.item_id
        assert contents[0]["quantity"] == 2
        
        # Check basket value
        assert sample_basket.get_basket_value(customer_id) == item.cost * 2
    
    def test_add_product_existing_item(self, sample_basket, sample_customer, sample_items):
        """Test adding more of an existing product"""
        customer_id = sample_customer.customer_id
        item = sample_items[0]
        
        # Add product to basket twice
        sample_basket.add_product(customer_id, item, 2)
        sample_basket.add_product(customer_id, item, 3)
        
        # Check quantity was combined
        contents = sample_basket.get_basket_contents(customer_id)
        assert len(contents) == 1
        assert contents[0]["quantity"] == 5
        
        # Check basket value was updated correctly
        assert sample_basket.get_basket_value(customer_id) == item.cost * 5
    
    def test_add_multiple_products(self, sample_basket, sample_customer, sample_items):
        """Test adding multiple different products"""
        customer_id = sample_customer.customer_id
        
        # Add multiple items
        for i, item in enumerate(sample_items, 1):
            sample_basket.add_product(customer_id, item, i)
        
        # Check all items were added
        contents = sample_basket.get_basket_contents(customer_id)
        assert len(contents) == len(sample_items)
        
        # Calculate expected total
        expected_total = sum(item.cost * (i+1) for i, item in enumerate(sample_items))
        assert sample_basket.get_basket_value(customer_id) == expected_total
    
    def test_add_zero_quantity(self, sample_basket, sample_customer, sample_items):
        """Test adding a product with zero quantity"""
        customer_id = sample_customer.customer_id
        item = sample_items[0]
        
        # Add product with zero quantity
        sample_basket.add_product(customer_id, item, 0)
        
        # Item should be in basket with zero quantity
        contents = sample_basket.get_basket_contents(customer_id)
        assert len(contents) == 1
        assert contents[0]["quantity"] == 0
        
        # Basket value should be zero
        assert sample_basket.get_basket_value(customer_id) == 0
    
    def test_remove_product(self, sample_basket, sample_customer, sample_items):
        """Test removing a product from the basket"""
        customer_id = sample_customer.customer_id
        item = sample_items[0]
        
        # Add then remove product
        sample_basket.add_product(customer_id, item, 2)
        assert sample_basket.remove_product(customer_id, item.item_id) == True
        
        # Basket should be empty
        assert sample_basket.get_basket_contents(customer_id) == []
        assert sample_basket.get_basket_value(customer_id) == 0
    
    def test_remove_nonexistent_product(self, sample_basket, sample_customer):
        """Test removing a product that doesn't exist in the basket"""
        customer_id = sample_customer.customer_id
        
        # Try to remove a product from an empty basket
        assert sample_basket.remove_product(customer_id, 1234) == False
    
    def test_remove_from_nonexistent_basket(self, sample_basket):
        """Test removing a product from a basket that doesn't exist"""
        assert sample_basket.remove_product(9999, 1234) == False
    
    def test_multiple_customer_baskets(self, sample_basket, sample_items):
        """Test baskets for multiple customers remain separate"""
        customer1 = PersonalClient("user1", "pass1", "Address 1")
        customer2 = PersonalClient("user2", "pass2", "Address 2")
        
        # Add different items to different customer baskets
        sample_basket.add_product(customer1.customer_id, sample_items[0], 1)
        sample_basket.add_product(customer2.customer_id, sample_items[1], 2)
        
        # Check baskets contain the right items
        contents1 = sample_basket.get_basket_contents(customer1.customer_id)
        contents2 = sample_basket.get_basket_contents(customer2.customer_id)
        
        assert len(contents1) == 1
        assert contents1[0]["item"].title == "Item A"
        
        assert len(contents2) == 1
        assert contents2[0]["item"].title == "Item B"
    
    def test_get_empty_basket(self, sample_basket, sample_customer):
        """Test getting contents of empty basket"""
        customer_id = sample_customer.customer_id
        
        assert sample_basket.get_basket_contents(customer_id) == []
        assert sample_basket.get_basket_value(customer_id) == 0
    
    def test_get_nonexistent_basket(self, sample_basket):
        """Test getting a basket that doesn't exist"""
        assert sample_basket.get_basket_contents(9999) == []
        assert sample_basket.get_basket_value(9999) == 0
    
    def test_checkout_empty_basket(self, sample_basket, sample_customer):
        """Test checkout with empty basket returns None"""
        customer_id = sample_customer.customer_id
        
        # Try to checkout with empty basket
        purchase = sample_basket.checkout(sample_customer, "Card")
        
        assert purchase is None
    
    def test_checkout_updates_inventory(self, sample_basket, sample_customer, sample_items):
        """Test checkout reduces item inventory"""
        item = sample_items[0]
        initial_inventory = item.inventory_count
        quantity = 5
        
        # Add to basket and checkout
        sample_basket.add_product(sample_customer.customer_id, item, quantity)
        purchase = sample_basket.checkout(sample_customer, "Card")
        
        # Verify inventory was reduced
        assert item.inventory_count == initial_inventory - quantity
    
    def test_checkout_clears_basket(self, sample_basket, sample_customer, sample_items):
        """Test checkout clears the basket"""
        customer_id = sample_customer.customer_id
        item = sample_items[0]
        
        # Add to basket and checkout
        sample_basket.add_product(customer_id, item, 1)
        sample_basket.checkout(sample_customer, "Card")
        
        # Basket should be reset
        assert sample_basket.get_basket_contents(customer_id) == []
        assert sample_basket.get_basket_value(customer_id) == 0
    
    def test_checkout_creates_purchase(self, sample_basket, sample_customer, sample_items):
        """Test checkout creates a purchase with correct data"""
        item = sample_items[0]
        quantity = 3
        
        # Add to basket and checkout
        sample_basket.add_product(sample_customer.customer_id, item, quantity)
        purchase = sample_basket.checkout(sample_customer, "Card")
        
        # Verify purchase details
        assert purchase is not None
        assert purchase.customer == sample_customer
        assert len(purchase.products_and_quantities) == 1
        assert purchase.products_and_quantities[0]["item"] == item
        assert purchase.products_and_quantities[0]["quantity"] == quantity
        assert purchase.original_cost == item.cost * quantity
        assert purchase.final_cost == item.cost * quantity  # No discount applied
    
    def test_checkout_with_discount(self, sample_basket, sample_customer, sample_items):
        """Test checkout with discount applied"""
        item = sample_items[0]
        quantity = 2
        discount = 5.00
        
        # Add to basket and checkout with discount
        sample_basket.add_product(sample_customer.customer_id, item, quantity)
        purchase = sample_basket.checkout(sample_customer, "Card", discount)
        
        # Verify discount was applied
        assert purchase.original_cost == item.cost * quantity
        assert purchase.final_cost == (item.cost * quantity) - discount
