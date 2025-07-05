import unittest
import os
import sys
import shutil
import uuid
from datetime import datetime

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models import User, MenuItem, Order, OrderItem, DeliveryAgent, DeliveryMode, OrderStatus
from src.services import UserService, MenuService, OrderService, DeliveryAgentService
from src.database import Database

class TestFoodDeliveryBasics(unittest.TestCase):
    """Basic test cases for the food delivery system"""
    
    def setUp(self):
        """Set up test environment"""
        # Use a temporary directory for test data
        self.test_data_dir = "test_data"
        os.environ['DATA_DIR'] = self.test_data_dir
        os.makedirs(self.test_data_dir, exist_ok=True)
        
        # Initialize services
        self.user_service = UserService()
        self.menu_service = MenuService()
        self.order_service = OrderService()
        self.delivery_service = DeliveryAgentService()
        
        # Add test data
        self._create_test_data()
    
    def tearDown(self):
        """Clean up after tests"""
        # Remove test data directory
        if os.path.exists(self.test_data_dir):
            shutil.rmtree(self.test_data_dir)
        
        # Reset environment variable
        if 'DATA_DIR' in os.environ:
            del os.environ['DATA_DIR']
    
    def _create_test_data(self):
        """Create initial test data"""
        # Add sample menu items
        self.menu_service.add_item("Test Pizza", 10.99, 15)
        self.menu_service.add_item("Test Burger", 8.99, 12)
        self.menu_service.add_item("Test Salad", 6.99, 5)
        
        # Add sample users
        self.user_service.register_user("testuser", "testpass", "123 Test St", "555-1234")
        
        # Add sample delivery agent
        self.delivery_service.register_agent("testagent", "testpass", "555-5678")
        
        # Save to ensure data is committed to files
        db = Database()
        db.save_data()
        
        # Reload services to ensure data is loaded
        self.user_service = UserService()
        self.menu_service = MenuService()
        self.order_service = OrderService()
        self.delivery_service = DeliveryAgentService()
    
    # 1. Basic User Tests
    
    def test_01_register_user(self):
        """Test registering a user"""
        success, message = self.user_service.register_user(
            "newuser", "password", "456 Test Ave", "555-9876")
        self.assertTrue(success)
        self.assertEqual(message, "User registered successfully")
    
    def test_02_duplicate_user_registration(self):
        """Test registering a duplicate user"""
        success, message = self.user_service.register_user(
            "testuser", "password", "789 Test Blvd", "555-1111")
        self.assertFalse(success)
        self.assertEqual(message, "Username already exists")
    
    def test_03_valid_user_login(self):
        """Test logging in with valid credentials"""
        success, message = self.user_service.login_user("testuser", "testpass")
        self.assertTrue(success)
        self.assertEqual(message, "Login successful")
    
    def test_04_invalid_user_login(self):
        """Test logging in with invalid credentials"""
        success, message = self.user_service.login_user("testuser", "wrongpass")
        self.assertFalse(success)
    
    def test_05_get_user_details(self):
        """Test getting user details"""
        success, user = self.user_service.get_user_details("testuser")
        self.assertTrue(success)
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.address, "123 Test St")
    
    # 2. Basic Menu Tests
    
    def test_06_add_menu_item(self):
        """Test adding a menu item"""
        success, message = self.menu_service.add_item("New Dish", 12.99, 20)
        self.assertTrue(success)
        self.assertIn("Item added successfully", message)
    
    def test_07_get_all_menu_items(self):
        """Test getting all menu items"""
        menu_items = self.menu_service.get_all_items()
        self.assertGreaterEqual(len(menu_items), 3)
    
    def test_08_get_specific_menu_item(self):
        """Test getting a specific menu item"""
        # First add a menu item to get its ID
        success, message = self.menu_service.add_item("Special Item", 15.99, 25)
        item_id = message.split(": ")[1]
        
        # Retrieve the item
        item = self.menu_service.get_item(item_id)
        self.assertIsNotNone(item)
        self.assertEqual(item.name, "Special Item")
    
    def test_09_update_menu_item(self):
        """Test updating a menu item"""
        # First add a menu item to update
        success, message = self.menu_service.add_item("Update Me", 9.99, 10)
        item_id = message.split(": ")[1]
        
        # Update the item
        success, message = self.menu_service.update_item(item_id, "Updated Item", 14.99, 15)
        self.assertTrue(success)
        
        # Verify update
        item = self.menu_service.get_item(item_id)
        self.assertEqual(item.name, "Updated Item")
    
    def test_10_delete_menu_item(self):
        """Test deleting a menu item"""
        # First add a menu item to delete
        success, message = self.menu_service.add_item("Delete Me", 7.99, 8)
        item_id = message.split(": ")[1]
        
        # Delete the item
        success, message = self.menu_service.delete_item(item_id)
        self.assertTrue(success)
        
        # Verify deletion
        item = self.menu_service.get_item(item_id)
        self.assertIsNone(item)
    
    # 3. Basic Order Tests
    
    def test_11_create_takeaway_order(self):
        """Test creating a takeaway order"""
        menu_items = self.menu_service.get_all_items()
        item_quantities = [(menu_items[0].item_id, 1)]
        
        success, message = self.order_service.create_order(
            "testuser", item_quantities, DeliveryMode.TAKEAWAY)
        
        self.assertTrue(success)
        self.assertIn("Order placed successfully", message)
    
    def test_12_create_home_delivery_order(self):
        """Test creating a home delivery order"""
        menu_items = self.menu_service.get_all_items()
        item_quantities = [(menu_items[0].item_id, 1)]
        
        success, message = self.order_service.create_order(
            "testuser", item_quantities, DeliveryMode.HOME_DELIVERY, "456 Delivery St")
        
        self.assertTrue(success)
        self.assertIn("Order placed successfully", message)
    
    def test_13_get_order_details(self):
        """Test getting order details"""
        # First create an order
        menu_items = self.menu_service.get_all_items()
        success, message = self.order_service.create_order(
            "testuser", [(menu_items[0].item_id, 1)], DeliveryMode.TAKEAWAY)
        
        order_id = message.split(": ")[1]
        
        # Get the order
        order = self.order_service.get_order(order_id)
        
        self.assertIsNotNone(order)
        self.assertEqual(order.customer_username, "testuser")
        self.assertEqual(order.status, OrderStatus.PLACED)
    
    def test_14_order_initial_status(self):
        """Test initial order status"""
        # Create order
        menu_items = self.menu_service.get_all_items()
        success, message = self.order_service.create_order(
            "testuser", [(menu_items[0].item_id, 1)], DeliveryMode.TAKEAWAY)
        order_id = message.split(": ")[1]
        
        # Check status
        order = self.order_service.get_order(order_id)
        self.assertEqual(order.status, OrderStatus.PLACED)
    
    def test_15_update_order_status(self):
        """Test updating order status"""
        # Create order
        menu_items = self.menu_service.get_all_items()
        success, message = self.order_service.create_order(
            "testuser", [(menu_items[0].item_id, 1)], DeliveryMode.TAKEAWAY)
        order_id = message.split(": ")[1]
        
        # Update status
        success, message = self.order_service.update_order_status(
            order_id, OrderStatus.PREPARING)
        
        self.assertTrue(success)
        
        # Verify status change
        order = self.order_service.get_order(order_id)
        self.assertEqual(order.status, OrderStatus.PREPARING)
    
    def test_16_cancel_order(self):
        """Test cancelling an order"""
        # Create order
        menu_items = self.menu_service.get_all_items()
        success, message = self.order_service.create_order(
            "testuser", [(menu_items[0].item_id, 1)], DeliveryMode.TAKEAWAY)
        order_id = message.split(": ")[1]
        
        # Cancel order
        success, message = self.order_service.cancel_order(order_id)
        self.assertTrue(success)
        
        # Verify cancellation
        order = self.order_service.get_order(order_id)
        self.assertEqual(order.status, OrderStatus.CANCELLED)
    
    # 4. Basic Delivery Agent Tests
    
    def test_17_register_delivery_agent(self):
        """Test registering a delivery agent"""
        success, message = self.delivery_service.register_agent(
            "newagent", "password", "555-9876")
        self.assertTrue(success)
        self.assertEqual(message, "Delivery agent registered successfully")
    
    def test_18_duplicate_agent_registration(self):
        """Test registering a duplicate delivery agent"""
        success, message = self.delivery_service.register_agent(
            "testagent", "password", "555-1111")
        self.assertFalse(success)
        self.assertEqual(message, "Username already exists")
    
    def test_19_valid_agent_login(self):
        """Test logging in with valid agent credentials"""
        success, message = self.delivery_service.login_agent("testagent", "testpass")
        self.assertTrue(success)
        self.assertEqual(message, "Login successful")
    
    def test_20_invalid_agent_login(self):
        """Test logging in with invalid agent credentials"""
        success, message = self.delivery_service.login_agent("testagent", "wrongpass")
        self.assertFalse(success)
    
    def test_21_get_agent_details(self):
        """Test getting agent details"""
        success, agent = self.delivery_service.get_agent_details("testagent")
        self.assertTrue(success)
        self.assertEqual(agent.username, "testagent")
        self.assertEqual(agent.phone, "555-5678")
    
    # 5. Additional Basic Tests
    
    def test_22_get_nonexistent_user(self):
        """Test getting details of nonexistent user"""
        success, user = self.user_service.get_user_details("nonexistent")
        self.assertFalse(success)
    
    def test_23_get_nonexistent_agent(self):
        """Test getting details of nonexistent agent"""
        success, agent = self.delivery_service.get_agent_details("nonexistent")
        self.assertFalse(success)
    
    def test_24_get_nonexistent_menu_item(self):
        """Test getting a nonexistent menu item"""
        item = self.menu_service.get_item("nonexistent-id")
        self.assertIsNone(item)
    
    def test_25_get_nonexistent_order(self):
        """Test getting a nonexistent order"""
        order = self.order_service.get_order("nonexistent-id")
        self.assertIsNone(order)
    
    def test_26_create_order_nonexistent_user(self):
        """Test creating order with nonexistent user"""
        menu_items = self.menu_service.get_all_items()
        success, message = self.order_service.create_order(
            "nonexistent", [(menu_items[0].item_id, 1)], DeliveryMode.TAKEAWAY)
        self.assertFalse(success)
    
    def test_27_create_order_nonexistent_item(self):
        """Test creating order with nonexistent menu item"""
        success, message = self.order_service.create_order(
            "testuser", [("nonexistent-id", 1)], DeliveryMode.TAKEAWAY)
        self.assertFalse(success)
    
    def test_28_create_order_empty_items(self):
        """Test creating order with no items"""
        success, message = self.order_service.create_order(
            "testuser", [], DeliveryMode.TAKEAWAY)
        self.assertFalse(success)
    
    def test_29_order_total_price(self):
        """Test order total price calculation"""
        # Create menu items with known prices
        success, message1 = self.menu_service.add_item("Item1", 10.00, 15)
        item1_id = message1.split(": ")[1]
        
        success, message2 = self.menu_service.add_item("Item2", 5.00, 10)
        item2_id = message2.split(": ")[1]
        
        # Create order with multiple items
        success, message = self.order_service.create_order(
            "testuser", [(item1_id, 2), (item2_id, 1)], DeliveryMode.TAKEAWAY)
        order_id = message.split(": ")[1]
        
        # Check total price (2*10 + 1*5 = 25)
        order = self.order_service.get_order(order_id)
        self.assertEqual(order.total_price, 25.00)
    
    def test_30_update_nonexistent_order(self):
        """Test updating status of nonexistent order"""
        success, message = self.order_service.update_order_status(
            "nonexistent-id", OrderStatus.PREPARING)
        self.assertFalse(success)
    
    def test_31_invalid_status_transition(self):
        """Test invalid order status transition"""
        # Create order
        menu_items = self.menu_service.get_all_items()
        success, message = self.order_service.create_order(
            "testuser", [(menu_items[0].item_id, 1)], DeliveryMode.TAKEAWAY)
        order_id = message.split(": ")[1]
        
        # Try to skip from PLACED directly to PICKED_UP
        success, message = self.order_service.update_order_status(
            order_id, OrderStatus.PICKED_UP)
        self.assertFalse(success)
    
    def test_32_get_all_delivery_agents(self):
        """Test getting all delivery agents"""
        agents = self.delivery_service.get_all_agents()
        self.assertGreaterEqual(len(agents), 1)
        self.assertEqual(agents[0].username, "testagent")
    
    def test_33_create_multiple_orders(self):
        """Test creating multiple orders"""
        menu_items = self.menu_service.get_all_items()
        
        # Create first order
        success1, _ = self.order_service.create_order(
            "testuser", [(menu_items[0].item_id, 1)], DeliveryMode.TAKEAWAY)
        
        # Create second order
        success2, _ = self.order_service.create_order(
            "testuser", [(menu_items[1].item_id, 1)], DeliveryMode.TAKEAWAY)
        
        self.assertTrue(success1)
        self.assertTrue(success2)
        
        # Get all orders
        orders = self.order_service.get_all_orders()
        self.assertEqual(len(orders), 2)
    
    def test_34_update_nonexistent_menu_item(self):
        """Test updating a nonexistent menu item"""
        success, message = self.menu_service.update_item(
            "nonexistent-id", "New Name", 10.99, 15)
        self.assertFalse(success)
    
    def test_35_delete_nonexistent_menu_item(self):
        """Test deleting a nonexistent menu item"""
        success, message = self.menu_service.delete_item("nonexistent-id")
        self.assertFalse(success)

    def test_36_order_with_default_address(self):
        """Test ordering delivery with default address"""
        menu_items = self.menu_service.get_all_items()
        success, message = self.order_service.create_order(
            "testuser", [(menu_items[0].item_id, 1)], DeliveryMode.HOME_DELIVERY)
        
        order_id = message.split(": ")[1]
        order = self.order_service.get_order(order_id)
        
        self.assertEqual(order.delivery_address, "123 Test St")

    def test_37_create_order_multiple_items(self):
        """Test creating an order with multiple items"""
        menu_items = self.menu_service.get_all_items()
        success, message = self.order_service.create_order(
            "testuser", 
            [(menu_items[0].item_id, 2), (menu_items[1].item_id, 3)], 
            DeliveryMode.TAKEAWAY
        )
        
        order_id = message.split(": ")[1]
        order = self.order_service.get_order(order_id)
        
        self.assertEqual(len(order.items), 2)
        # Check items have correct quantities
        item_quantities = {item.menu_item.item_id: item.quantity for item in order.items}
        self.assertEqual(item_quantities[menu_items[0].item_id], 2)
        self.assertEqual(item_quantities[menu_items[1].item_id], 3)

    def test_38_order_status_after_update(self):
        """Test order status after update"""
        menu_items = self.menu_service.get_all_items()
        success, message = self.order_service.create_order(
            "testuser", [(menu_items[0].item_id, 1)], DeliveryMode.TAKEAWAY)
        order_id = message.split(": ")[1]
        
        # Sequence of updates
        self.order_service.update_order_status(order_id, OrderStatus.PREPARING)
        self.order_service.update_order_status(order_id, OrderStatus.READY_FOR_PICKUP)
        
        # Verify final status
        order = self.order_service.get_order(order_id)
        self.assertEqual(order.status, OrderStatus.READY_FOR_PICKUP)

    def test_39_database_save_and_reload(self):
        """Test database save and reload functionality"""
        # Create a new user
        self.user_service.register_user("dbuser", "dbpass", "DB St", "555-1234")
        
        # Force save
        db = Database()
        db.save_data()
        
        # Create new service instance to reload data
        new_user_service = UserService()
        
        # Check if user exists in new service instance
        success, user = new_user_service.get_user_details("dbuser")
        self.assertTrue(success)
        self.assertEqual(user.address, "DB St")

    def test_40_get_menu_item_by_id(self):
        """Test retrieving a menu item by ID"""
        # Add item
        success, message = self.menu_service.add_item("Test Item", 11.99, 10)
        item_id = message.split(": ")[1]
        
        # Retrieve item
        item = self.menu_service.get_item(item_id)
        
        self.assertIsNotNone(item)
        self.assertEqual(item.name, "Test Item")
        self.assertEqual(item.price, 11.99)
        self.assertEqual(item.preparation_time, 10)

    def test_41_multiple_agents_registration(self):
        """Test registering multiple agents"""
        success1, _ = self.delivery_service.register_agent("agent1", "pass1", "111-1111")
        success2, _ = self.delivery_service.register_agent("agent2", "pass2", "222-2222")
        
        self.assertTrue(success1)
        self.assertTrue(success2)
        
        agents = self.delivery_service.get_all_agents()
        agent_usernames = [agent.username for agent in agents]
        
        self.assertIn("agent1", agent_usernames)
        self.assertIn("agent2", agent_usernames)

    def test_42_multiple_users_registration(self):
        """Test registering multiple users"""
        success1, _ = self.user_service.register_user("user1", "pass1", "Address1", "111-1111")
        success2, _ = self.user_service.register_user("user2", "pass2", "Address2", "222-2222")
        
        self.assertTrue(success1)
        self.assertTrue(success2)
        
        # Verify both users exist
        success1, user1 = self.user_service.get_user_details("user1")
        success2, user2 = self.user_service.get_user_details("user2")
        
        self.assertTrue(success1)
        self.assertTrue(success2)
        self.assertEqual(user1.address, "Address1")
        self.assertEqual(user2.address, "Address2")

    def test_43_order_creation_time(self):
        """Test order creation time is set"""
        menu_items = self.menu_service.get_all_items()
        success, message = self.order_service.create_order(
            "testuser", [(menu_items[0].item_id, 1)], DeliveryMode.TAKEAWAY)
        order_id = message.split(": ")[1]
        
        order = self.order_service.get_order(order_id)
        
        # Check that creation time is set
        self.assertIsNotNone(order.creation_time)
        self.assertIsInstance(order.creation_time, datetime)

    def test_44_order_estimated_completion_time(self):
        """Test order estimated completion time is set"""
        menu_items = self.menu_service.get_all_items()
        success, message = self.order_service.create_order(
            "testuser", [(menu_items[0].item_id, 1)], DeliveryMode.TAKEAWAY)
        order_id = message.split(": ")[1]
        
        order = self.order_service.get_order(order_id)
        
        # Check that estimated time is set
        self.assertIsNotNone(order.estimated_completion_time)
        self.assertIsInstance(order.estimated_completion_time, datetime)

    def test_45_time_remaining_calculation(self):
        """Test basic time remaining calculation"""
        menu_items = self.menu_service.get_all_items()
        
        # Find a menu item with preparation time 15
        test_item = None
        for item in menu_items:
            if item.preparation_time == 15:
                test_item = item
                break
        
        if not test_item:
            # Create one if not found
            success, message = self.menu_service.add_item("Time Test", 10.99, 15)
            item_id = message.split(": ")[1]
            test_item = self.menu_service.get_item(item_id)
        
        # Create order with this item
        success, message = self.order_service.create_order(
            "testuser", [(test_item.item_id, 1)], DeliveryMode.TAKEAWAY)
        order_id = message.split(": ")[1]
        
        # Check time remaining is approximately the preparation time
        order = self.order_service.get_order(order_id)
        time_remaining = order.get_time_remaining()
        
        # Time should be around 15 minutes (could be 14 if a second has passed)
        self.assertIn(time_remaining, [14, 15, 16])

    def test_46_get_all_orders_empty(self):
        """Test getting all orders when none exist"""
        # Create fresh database
        shutil.rmtree(self.test_data_dir)
        os.makedirs(self.test_data_dir, exist_ok=True)
        
        # Reload services
        self.user_service = UserService()
        self.menu_service = MenuService()
        self.order_service = OrderService()
        
        # Check no orders exist
        orders = self.order_service.get_all_orders()
        self.assertEqual(len(orders), 0)

    def test_47_get_available_agents(self):
        """Test getting available delivery agents"""
        # Register a new agent
        self.delivery_service.register_agent("availagent", "pass", "333-3333")
        
        # Get available agents
        available_agents = self.delivery_service.get_available_agents()
        
        # Check agent is in available list
        agent_usernames = [agent.username for agent in available_agents]
        self.assertIn("availagent", agent_usernames)

    def test_48_order_item_properties(self):
        """Test order item properties"""
        # Create menu item
        success, message = self.menu_service.add_item("Property Test", 10.00, 15)
        item_id = message.split(": ")[1]
        menu_item = self.menu_service.get_item(item_id)
        
        # Create order item
        order_item = OrderItem(menu_item, 3)
        
        # Check properties
        self.assertEqual(order_item.quantity, 3)
        self.assertEqual(order_item.total_price, 30.00)  # 3 * 10.00
        self.assertEqual(order_item.preparation_time, 15)

    def test_49_get_user_orders_empty(self):
        """Test getting orders for a user with no orders"""
        # Register a new user
        self.user_service.register_user("noorderuser", "pass", "No Order St", "444-4444")
        
        # Get orders
        orders = self.user_service.get_user_orders("noorderuser")
        
        # Should have no orders
        self.assertEqual(len(orders), 0)

    def test_50_update_user_details(self):
        """Test user's order history is updated after ordering"""
        # Register user
        self.user_service.register_user("orderuser", "pass", "Order St", "555-5555")
        
        # Place an order
        menu_items = self.menu_service.get_all_items()
        self.order_service.create_order(
            "orderuser", [(menu_items[0].item_id, 1)], DeliveryMode.TAKEAWAY)
        
        # Force reload services
        self.user_service = UserService()
        
        # Get user and check order history
        success, user = self.user_service.get_user_details("orderuser")
        self.assertTrue(success)
        self.assertEqual(len(user.order_history), 1)


if __name__ == '__main__':
    unittest.main()
