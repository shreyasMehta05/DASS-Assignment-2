import uuid
from typing import List, Optional, Tuple
from datetime import datetime

from src.models import User, MenuItem, Order, DeliveryAgent, OrderItem, DeliveryMode, OrderStatus
from src.database import Database


class UserService:
    def __init__(self):
        self.db = Database()
    
    def register_user(self, username: str, password: str, address: str, phone: str) -> Tuple[bool, str]:
        """Register a new user"""
        if self.db.get_user(username):
            return False, "Username already exists"
        
        user = User(username, password, address, phone)
        if self.db.add_user(user):
            return True, "User registered successfully"
        return False, "Failed to register user"
    
    def login_user(self, username: str, password: str) -> Tuple[bool, str]:
        """Authenticate a user"""
        if self.db.authenticate_user(username, password):
            return True, "Login successful"
        return False, "Invalid username or password"
    
    def get_user_details(self, username: str) -> Tuple[bool, User]:
        """Get user details"""
        user = self.db.get_user(username)
        if user:
            return True, user
        return False, None
    
    def get_user_orders(self, username: str) -> List[Order]:
        """Get all orders for a user"""
        return self.db.get_user_orders(username)


class MenuService:
    def __init__(self):
        self.db = Database()
    
    def add_item(self, name: str, price: float, preparation_time: int) -> Tuple[bool, str]:
        """Add a new menu item"""
        item_id = str(uuid.uuid4())
        item = MenuItem(item_id, name, price, preparation_time)
        
        if self.db.add_menu_item(item):
            return True, f"Item added successfully with ID: {item_id}"
        return False, "Failed to add item"
    
    def get_all_items(self) -> List[MenuItem]:
        """Get all menu items"""
        return self.db.get_all_menu_items()
    
    def get_item(self, item_id: str) -> Optional[MenuItem]:
        """Get a specific menu item"""
        return self.db.get_menu_item(item_id)
    
    def update_item(self, item_id: str, name: str, price: float, preparation_time: int) -> Tuple[bool, str]:
        """Update an existing menu item"""
        item = self.db.get_menu_item(item_id)
        if not item:
            return False, "Item not found"
        
        updated_item = MenuItem(item_id, name, price, preparation_time)
        if self.db.update_menu_item(updated_item):
            return True, "Item updated successfully"
        return False, "Failed to update item"
    
    def delete_item(self, item_id: str) -> Tuple[bool, str]:
        """Delete a menu item"""
        if self.db.delete_menu_item(item_id):
            return True, "Item deleted successfully"
        return False, "Item not found or could not be deleted"


class OrderService:
    def __init__(self):
        self.db = Database()
    
    def create_order(self, username: str, item_quantities: List[Tuple[str, int]], 
                     delivery_mode: DeliveryMode, delivery_address: Optional[str] = None) -> Tuple[bool, str]:
        """Create a new order"""
        # Explicitly reload the database to ensure the latest user data
        self.db = Database()
        
        user = self.db.get_user(username)
        if not user:
            return False, f"User not found"
        
        # Check if delivery address is provided for home delivery
        if delivery_mode == DeliveryMode.HOME_DELIVERY and not delivery_address:
            delivery_address = user.address
        
        # Create order items
        order_items = []
        for item_id, quantity in item_quantities:
            menu_item = self.db.get_menu_item(item_id)
            if not menu_item:
                return False, f"Menu item with ID {item_id} not found"
            
            order_item = OrderItem(menu_item, quantity)
            order_items.append(order_item)
        
        if not order_items:
            return False, "Order must contain at least one item"
        
        # Create order
        order_id = str(uuid.uuid4())
        order = Order(order_id, username, order_items, delivery_mode, delivery_address)
        
        # For home delivery orders, assign a delivery agent if available
        if delivery_mode == DeliveryMode.HOME_DELIVERY:
            self._assign_delivery_agent(order)
        
        # Add order to database first
        if not self.db.add_order(order):
            return False, "Failed to place order"
            
        # Now explicitly update the user's order history
        user = self.db.get_user(username)  # Get fresh user object
        if user:
            if order_id not in user.order_history:
                user.add_order(order_id)
                if not self.db.update_user(user):  # Add this method to Database class
                    print("Warning: Failed to update user order history")
        
        return True, f"Order placed successfully with ID: {order_id}"
    
    def _assign_delivery_agent(self, order: Order) -> bool:
        """Assign a delivery agent to the order"""
        available_agents = self.db.get_available_delivery_agents()
        if not available_agents:
            return False
        
        # Assign to the first available agent
        agent = available_agents[0]
        order.assign_delivery_agent(agent.username)
        agent.assign_order(order.order_id)
        self.db.update_delivery_agent(agent)
        return True
    
    def get_order(self, order_id: str) -> Optional[Order]:
        """Get order details"""
        return self.db.get_order(order_id)
    
    def get_all_orders(self) -> List[Order]:
        """Get all orders"""
        return self.db.get_all_orders()
    
    def update_order_status(self, order_id: str, status: OrderStatus) -> Tuple[bool, str]:
        """Update order status"""
        order = self.db.get_order(order_id)
        if not order:
            return False, "Order not found"
        
        # Check if status transition is valid
        valid_transitions = {
            OrderStatus.PLACED: [OrderStatus.PREPARING, OrderStatus.CANCELLED],
            OrderStatus.PREPARING: [OrderStatus.READY_FOR_PICKUP, OrderStatus.CANCELLED],
            OrderStatus.READY_FOR_PICKUP: [OrderStatus.OUT_FOR_DELIVERY, OrderStatus.PICKED_UP],
            OrderStatus.OUT_FOR_DELIVERY: [OrderStatus.DELIVERED]
        }
        
        if order.status not in valid_transitions or status not in valid_transitions.get(order.status, []):
            return False, f"Invalid status transition from {order.status.value} to {status.value}"
        
        order.update_status(status)
        
        # Handle delivery agent workflow
        if status == OrderStatus.DELIVERED or status == OrderStatus.PICKED_UP:
            if order.assigned_delivery_agent:
                agent = self.db.get_delivery_agent(order.assigned_delivery_agent)
                if agent:
                    agent.complete_order(order_id)
                    self.db.update_delivery_agent(agent)
        
        self.db.update_order(order)
        return True, f"Order status updated to {status.value}"
    
    def cancel_order(self, order_id: str) -> Tuple[bool, str]:
        """Cancel an order"""
        return self.update_order_status(order_id, OrderStatus.CANCELLED)


class DeliveryAgentService:
    def __init__(self):
        self.db = Database()
    
    def register_agent(self, username: str, password: str, phone: str) -> Tuple[bool, str]:
        """Register a new delivery agent"""
        if self.db.get_delivery_agent(username):
            return False, "Username already exists"
        
        agent = DeliveryAgent(username, password, phone)
        if self.db.add_delivery_agent(agent):
            return True, "Delivery agent registered successfully"
        return False, "Failed to register delivery agent"
    
    def login_agent(self, username: str, password: str) -> Tuple[bool, str]:
        """Authenticate a delivery agent"""
        agent = self.db.get_delivery_agent(username)
        if agent and agent.password == password:
            return True, "Login successful"
        return False, "Invalid username or password"
    
    def get_agent_details(self, username: str) -> Tuple[bool, DeliveryAgent]:
        """Get agent details"""
        agent = self.db.get_delivery_agent(username)
        if agent:
            return True, agent
        return False, None
    
    def get_agent_orders(self, username: str) -> List[Order]:
        """Get all assigned orders for an agent"""
        agent = self.db.get_delivery_agent(username)
        if not agent:
            return []
        
        orders = []
        for order_id in agent.current_orders:
            order = self.db.get_order(order_id)
            if order:
                orders.append(order)
        
        return orders
    
    def complete_order(self, agent_username: str, order_id: str) -> Tuple[bool, str]:
        """Mark an order as completed by the agent"""
        agent = self.db.get_delivery_agent(agent_username)
        if not agent:
            return False, "Agent not found"
        
        order = self.db.get_order(order_id)
        if not order:
            return False, "Order not found"
        
        if order_id not in agent.current_orders:
            return False, "Order not assigned to this agent"
        
        # Update order status
        order_service = OrderService()
        result, message = order_service.update_order_status(order_id, OrderStatus.DELIVERED)
        return result, message
    
    def get_all_agents(self) -> List[DeliveryAgent]:
        """Get all delivery agents"""
        return self.db.get_all_delivery_agents()
    
    def get_available_agents(self) -> List[DeliveryAgent]:
        """Get all available delivery agents"""
        return self.db.get_available_delivery_agents()
    
    def assign_agent_to_order(self, order_id: str, agent_username: str) -> Tuple[bool, str]:
        """Assign a delivery agent to an order"""
        agent = self.db.get_delivery_agent(agent_username)
        if not agent:
            return False, "Agent not found"
        
        if not agent.available:
            return False, "Agent is not available"
        
        order = self.db.get_order(order_id)
        if not order:
            return False, "Order not found"
        
        if order.status != OrderStatus.READY_FOR_PICKUP:
            return False, "Order is not ready for pickup"
        
        if order.delivery_mode != DeliveryMode.HOME_DELIVERY:
            return False, "Order is not for home delivery"
        
        if order.assigned_delivery_agent:
            return False, "Order already has an assigned agent"
        
        # Assign the agent
        order.assign_delivery_agent(agent_username)
        agent.assign_order(order_id)
        
        # Update order status to out for delivery
        order.update_status(OrderStatus.OUT_FOR_DELIVERY)
        
        # Save changes
        self.db.save_data()
        
        return True, f"Agent {agent_username} assigned to order {order_id}"