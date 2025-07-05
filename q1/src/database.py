import os
import json
from typing import Dict, List, Optional
from datetime import datetime

from src.models import User, MenuItem, Order, DeliveryAgent, OrderItem, DeliveryMode, OrderStatus


class Database:
    """Database class for handling data persistence using JSON files"""

    def __init__(self):
        """Initialize database and create data files if needed"""
        # Get data directory from environment or use default
        self.data_dir = os.environ.get('DATA_DIR', 'data')
        
        # Create data directory if it doesn't exist
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Define file paths
        self.users_file = os.path.join(self.data_dir, 'users.json')
        self.menu_items_file = os.path.join(self.data_dir, 'menu_items.json')
        self.orders_file = os.path.join(self.data_dir, 'orders.json')
        self.delivery_agents_file = os.path.join(self.data_dir, 'delivery_agents.json')
        
        # Load initial data
        self.users = self._load_users()
        self.menu_items = self._load_menu_items()
        self.orders = self._load_orders()
        self.delivery_agents = self._load_delivery_agents()

    def _load_users(self) -> Dict[str, User]:
        """Load users from JSON file"""
        try:
            if os.path.exists(self.users_file):
                with open(self.users_file, 'r') as f:
                    data = json.load(f)
                users = {}
                for username, user_data in data.items():
                    user = User(
                        username=username,
                        password=user_data['password'],
                        address=user_data['address'],
                        phone=user_data['phone']
                    )
                    user.order_history = user_data.get('order_history', [])
                    users[username] = user
                return users
            return {}
        except Exception as e:
            print(f"Error loading users: {e}")
            return {}

    def _load_menu_items(self) -> Dict[str, MenuItem]:
        """Load menu items from JSON file"""
        try:
            if os.path.exists(self.menu_items_file):
                with open(self.menu_items_file, 'r') as f:
                    data = json.load(f)
                menu_items = {}
                for item_id, item_data in data.items():
                    item = MenuItem(
                        item_id=item_id,
                        name=item_data['name'],
                        price=item_data['price'],
                        preparation_time=item_data['preparation_time']
                    )
                    menu_items[item_id] = item
                return menu_items
            return {}
        except Exception as e:
            print(f"Error loading menu items: {e}")
            return {}

    def _load_orders(self) -> Dict[str, Order]:
        """Load orders from JSON file"""
        try:
            if os.path.exists(self.orders_file):
                with open(self.orders_file, 'r') as f:
                    data = json.load(f)
                
                orders = {}
                for order_id, order_data in data.items():
                    # First load all menu items needed for this order
                    order_items = []
                    for item_data in order_data.get('items', []):
                        menu_item_id = item_data['menu_item_id']
                        menu_item = self.get_menu_item(menu_item_id)
                        if menu_item:
                            order_item = OrderItem(
                                menu_item=menu_item,
                                quantity=item_data['quantity']
                            )
                            order_items.append(order_item)
                    
                    # Create the order
                    order = Order(
                        order_id=order_id,
                        customer_username=order_data['customer_username'],
                        items=order_items,
                        delivery_mode=DeliveryMode(order_data['delivery_mode']),
                        delivery_address=order_data.get('delivery_address')
                    )
                    
                    # Set additional properties
                    order.status = OrderStatus(order_data['status'])
                    order.creation_time = datetime.fromisoformat(order_data['creation_time'])
                    order.estimated_completion_time = datetime.fromisoformat(order_data['estimated_completion_time'])
                    order.assigned_delivery_agent = order_data.get('assigned_delivery_agent')
                    
                    orders[order_id] = order
                
                return orders
            return {}
        except Exception as e:
            print(f"Error loading orders: {e}")
            return {}

    def _load_delivery_agents(self) -> Dict[str, DeliveryAgent]:
        """Load delivery agents from JSON file"""
        try:
            if os.path.exists(self.delivery_agents_file):
                with open(self.delivery_agents_file, 'r') as f:
                    data = json.load(f)
                agents = {}
                for username, agent_data in data.items():
                    agent = DeliveryAgent(
                        username=username,
                        password=agent_data['password'],
                        phone=agent_data['phone']
                    )
                    agent.available = agent_data.get('available', True)
                    agent.current_orders = agent_data.get('current_orders', [])
                    agents[username] = agent
                return agents
            return {}
        except Exception as e:
            print(f"Error loading delivery agents: {e}")
            return {}

    def _save_users(self) -> bool:
        """Save users to JSON file"""
        try:
            user_data = {}
            for username, user in self.users.items():
                user_data[username] = {
                    'password': user.password,
                    'address': user.address,
                    'phone': user.phone,
                    'order_history': user.order_history
                }
            
            with open(self.users_file, 'w') as f:
                json.dump(user_data, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving users: {e}")
            return False

    def _save_menu_items(self) -> bool:
        """Save menu items to JSON file"""
        try:
            item_data = {}
            for item_id, item in self.menu_items.items():
                item_data[item_id] = {
                    'name': item.name,
                    'price': item.price,
                    'preparation_time': item.preparation_time
                }
            
            with open(self.menu_items_file, 'w') as f:
                json.dump(item_data, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving menu items: {e}")
            return False

    def _save_orders(self) -> bool:
        """Save orders to JSON file"""
        try:
            order_data = {}
            for order_id, order in self.orders.items():
                # Convert items to serializable format
                items = []
                for item in order.items:
                    items.append({
                        'menu_item_id': item.menu_item.item_id,
                        'quantity': item.quantity
                    })
                
                # Create serializable order data
                order_data[order_id] = {
                    'customer_username': order.customer_username,
                    'items': items,
                    'delivery_mode': order.delivery_mode.value,
                    'delivery_address': order.delivery_address,
                    'status': order.status.value,
                    'creation_time': order.creation_time.isoformat(),
                    'estimated_completion_time': order.estimated_completion_time.isoformat(),
                    'assigned_delivery_agent': order.assigned_delivery_agent
                }
            
            with open(self.orders_file, 'w') as f:
                json.dump(order_data, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving orders: {e}")
            return False

    def _save_delivery_agents(self) -> bool:
        """Save delivery agents to JSON file"""
        try:
            agent_data = {}
            for username, agent in self.delivery_agents.items():
                agent_data[username] = {
                    'password': agent.password,
                    'phone': agent.phone,
                    'available': agent.available,
                    'current_orders': agent.current_orders
                }
            
            with open(self.delivery_agents_file, 'w') as f:
                json.dump(agent_data, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving delivery agents: {e}")
            return False

    def save_data(self) -> bool:
        """Save all data to disk"""
        return (self._save_users() and 
                self._save_menu_items() and 
                self._save_orders() and 
                self._save_delivery_agents())

    # User operations
    def add_user(self, user: User) -> bool:
        """Add a new user to the database"""
        if user.username in self.users:
            return False
        
        self.users[user.username] = user
        return self._save_users()

    def get_user(self, username: str) -> Optional[User]:
        """Get a user by username"""
        return self.users.get(username)

    def authenticate_user(self, username: str, password: str) -> bool:
        """Authenticate a user with username and password"""
        user = self.get_user(username)
        return user is not None and user.password == password

    def get_user_orders(self, username: str) -> List[Order]:
        """Get all orders for a specific user"""
        user = self.get_user(username)
        if not user:
            return []
        
        user_orders = []
        for order_id in user.order_history:
            order = self.orders.get(order_id)
            if order:
                user_orders.append(order)
        
        return user_orders

    def update_user(self, user: User) -> bool:
        """Update an existing user"""
        if user.username not in self.users:
            return False
        
        self.users[user.username] = user
        return self._save_users()

    # Menu item operations
    def add_menu_item(self, item: MenuItem) -> bool:
        """Add a new menu item to the database"""
        self.menu_items[item.item_id] = item
        return self._save_menu_items()

    def get_menu_item(self, item_id: str) -> Optional[MenuItem]:
        """Get a menu item by ID"""
        return self.menu_items.get(item_id)

    def get_all_menu_items(self) -> List[MenuItem]:
        """Get all menu items"""
        return list(self.menu_items.values())

    def update_menu_item(self, item: MenuItem) -> bool:
        """Update an existing menu item"""
        if item.item_id not in self.menu_items:
            return False
        
        self.menu_items[item.item_id] = item
        return self._save_menu_items()

    def delete_menu_item(self, item_id: str) -> bool:
        """Delete a menu item"""
        if item_id not in self.menu_items:
            return False
        
        del self.menu_items[item_id]
        return self._save_menu_items()

    # Order operations
    def add_order(self, order: Order) -> bool:
        """Add a new order to the database"""
        # Add the order to the orders dictionary
        self.orders[order.order_id] = order
        
        # Add the order to the user's order history
        user = self.get_user(order.customer_username)
        if user:
            if order.order_id not in user.order_history:
                user.order_history.append(order.order_id)
            
        # Save both orders and users to ensure consistency
        return self._save_orders() and self._save_users()

    def get_order(self, order_id: str) -> Optional[Order]:
        """Get an order by ID"""
        return self.orders.get(order_id)

    def get_all_orders(self) -> List[Order]:
        """Get all orders"""
        return list(self.orders.values())

    def update_order(self, order: Order) -> bool:
        """Update an existing order"""
        if order.order_id not in self.orders:
            return False
        
        self.orders[order.order_id] = order
        return self._save_orders()

    # Delivery agent operations
    def add_delivery_agent(self, agent: DeliveryAgent) -> bool:
        """Add a new delivery agent to the database"""
        if agent.username in self.delivery_agents:
            return False
        
        self.delivery_agents[agent.username] = agent
        return self._save_delivery_agents()

    def get_delivery_agent(self, username: str) -> Optional[DeliveryAgent]:
        """Get a delivery agent by username"""
        return self.delivery_agents.get(username)

    def get_all_delivery_agents(self) -> List[DeliveryAgent]:
        """Get all delivery agents"""
        return list(self.delivery_agents.values())

    def get_available_delivery_agents(self) -> List[DeliveryAgent]:
        """Get available delivery agents"""
        return [agent for agent in self.delivery_agents.values() if agent.available]

    def update_delivery_agent(self, agent: DeliveryAgent) -> bool:
        """Update an existing delivery agent"""
        if agent.username not in self.delivery_agents:
            return False
        
        self.delivery_agents[agent.username] = agent
        return self._save_delivery_agents()
