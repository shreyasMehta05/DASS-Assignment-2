import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.item import Item, ItemFinder

class TestItemCreation:
    """Tests for item creation functionality"""
    
    def test_basic_item_creation(self):
        """Test creating an item with proper attributes"""
        item = Item("Smartphone", "Latest model", 999.99, "Electronics", 100)
        
        assert item.title == "Smartphone"
        assert item.details == "Latest model"
        assert item.cost == 999.99
        assert item.classification == "Electronics"
        assert item.inventory_count == 100
        assert 1000 <= item.item_id <= 9999  # ID should be in this range
    
    def test_item_unique_ids(self):
        """Test that multiple items receive unique IDs"""
        items = [Item(f"Item{i}", "Description", 10.0, "Test", 10) for i in range(100)]
        ids = [item.item_id for item in items]
        # Check for uniqueness - should be equal to the length if all are unique
        assert len(set(ids)) == len(ids)
    
    def test_item_with_zero_inventory(self):
        """Test creating an item with zero inventory"""
        item = Item("Out of Stock", "No stock", 15.99, "Test", 0)
        assert item.inventory_count == 0
        assert item.verify_availability(1) == False
    
    def test_item_with_decimal_price(self):
        """Test creating an item with decimal price"""
        item = Item("Precise", "Exact price", 10.33, "Test", 5)
        assert item.cost == 10.33

class TestInventoryManagement:
    """Tests for item inventory management functionality"""
    
    def test_verify_availability(self):
        """Test inventory availability checking"""
        item = Item("Headphones", "Noise cancelling", 199.99, "Electronics", 50)
        
        assert item.verify_availability(25) == True
        assert item.verify_availability(50) == True
        assert item.verify_availability(51) == False
        assert item.verify_availability(0) == True
    
    def test_reduce_inventory(self):
        """Test reducing inventory after purchase"""
        item = Item("Keyboard", "Mechanical gaming keyboard", 129.99, "Electronics", 30)
        
        # Valid reduction
        assert item.reduce_inventory(15) == True
        assert item.inventory_count == 15
        
        # Another valid reduction
        assert item.reduce_inventory(10) == True
        assert item.inventory_count == 5
        
        # Invalid reduction (would go negative)
        assert item.reduce_inventory(10) == False
        assert item.inventory_count == 5  # Inventory unchanged
    
    def test_reduce_zero_quantity(self):
        """Test reducing inventory by zero quantity"""
        item = Item("Keyboard", "Mechanical gaming keyboard", 129.99, "Electronics", 30)
        initial_count = item.inventory_count
        
        assert item.reduce_inventory(0) == True
        assert item.inventory_count == initial_count  # Should remain unchanged
    
    def test_reduce_entire_inventory(self):
        """Test reducing entire inventory to zero"""
        item = Item("Last Item", "Last one in stock", 19.99, "Electronics", 1)
        
        assert item.reduce_inventory(1) == True
        assert item.inventory_count == 0
        
        # Can't reduce further
        assert item.reduce_inventory(1) == False
        assert item.inventory_count == 0

class TestItemSearch:
    """Tests for item search functionality"""
    
    @pytest.fixture
    def sample_items(self):
        """Fixture providing sample items for testing"""
        return [
            Item("Gaming Mouse", "RGB gaming mouse", 59.99, "Electronics", 100),
            Item("Dress Shirt", "Formal cotton shirt", 49.99, "Clothing", 200),
            Item("Gaming Keyboard", "Mechanical keyboard", 129.99, "Electronics", 50),
            Item("Cotton Socks", "Pack of 6 pairs", 9.99, "Clothing", 300),
        ]
    
    def test_text_search_in_title(self, sample_items):
        """Test text-based item search in title"""
        results = ItemFinder.find_by_text(sample_items, "Gaming")
        assert len(results) == 2
        assert "Gaming Mouse" in [item.title for item in results]
        assert "Gaming Keyboard" in [item.title for item in results]
    
    def test_text_search_in_description(self, sample_items):
        """Test text-based item search in description"""
        results = ItemFinder.find_by_text(sample_items, "cotton")
        assert len(results) == 2
        assert "Dress Shirt" in [item.title for item in results]
        assert "Cotton Socks" in [item.title for item in results]
    
    def test_text_search_case_insensitive(self, sample_items):
        """Test case insensitive search"""
        results = ItemFinder.find_by_text(sample_items, "MECHANICAL")
        assert len(results) == 1
        assert results[0].title == "Gaming Keyboard"
    
    def test_text_search_no_results(self, sample_items):
        """Test search with no matching results"""
        results = ItemFinder.find_by_text(sample_items, "nonexistent")
        assert len(results) == 0
    
    def test_text_search_empty_string(self, sample_items):
        """Test search with empty string"""
        results = ItemFinder.find_by_text(sample_items, "")
        # All items should match an empty string
        assert len(results) == len(sample_items)
    
    def test_price_range_exact_match(self, sample_items):
        """Test price range search with exact match"""
        # The socks are exactly 9.99
        results = ItemFinder.find_by_price_range(sample_items, 9.99, 9.99)
        assert len(results) == 1
        assert results[0].title == "Cotton Socks"
    
    def test_price_range_inclusive_bounds(self, sample_items):
        """Test price range search with inclusive bounds"""
        results = ItemFinder.find_by_price_range(sample_items, 40, 60)
        assert len(results) == 2
        assert "Dress Shirt" in [item.title for item in results]
        assert "Gaming Mouse" in [item.title for item in results]
    
    def test_price_range_no_results(self, sample_items):
        """Test price range search with no results"""
        results = ItemFinder.find_by_price_range(sample_items, 200, 300)
        assert len(results) == 0
    
    def test_price_range_inverted_boundaries(self, sample_items):
        """Test price range search with min > max"""
        # When boundaries are inverted, should find nothing
        results = ItemFinder.find_by_price_range(sample_items, 100, 10)
        assert len(results) == 0
    
    def test_classification_search(self, sample_items):
        """Test category-based item search"""
        results = ItemFinder.find_by_classification(sample_items, "Electronics")
        assert len(results) == 2
        assert "Gaming Mouse" in [item.title for item in results]
        assert "Gaming Keyboard" in [item.title for item in results]
    
    def test_classification_search_case_insensitive(self, sample_items):
        """Test case insensitive category search"""
        results = ItemFinder.find_by_classification(sample_items, "electronics")
        assert len(results) == 2
        assert "Gaming Mouse" in [item.title for item in results]
        assert "Gaming Keyboard" in [item.title for item in results]
    
    def test_classification_search_no_results(self, sample_items):
        """Test category search with no results"""
        results = ItemFinder.find_by_classification(sample_items, "Furniture")
        assert len(results) == 0
