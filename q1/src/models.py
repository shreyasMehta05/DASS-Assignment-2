# src/models.py
import datetime
import uuid
from enum import Enum
from typing import Dict, List, Optional


class OrderStatus(Enum):
    PLACED = "Placed"
    PREPARING = "Preparing"
    READY_FOR_PICKUP = "Ready for Pickup"
    OUT_FOR_DELIVERY = "Out for Delivery"
    DELIVERED = "Delivered"
    PICKED_UP = "Picked Up"
    CANCELLED = "Cancelled"


class DeliveryMode(Enum):
    HOME_DELIVERY = "Home Delivery"
    TAKEAWAY = "Takeaway"


class User:
    def __init__(self, username: str, password: str, address: str, phone: str):
        self.username = username
        self.password = password
        self.address = address
        self.phone = phone
        self.order_history: List[str] = []  # List of order IDs

    def add_order(self, order_id: str):
        self.order_history.append(order_id)


class MenuItem:
    def __init__(self, item_id: str, name: str, price: float, preparation_time: int):
        self.item_id = item_id
        self.name = name
        self.price = price
        self.preparation_time = preparation_time  # in minutes


class OrderItem:
    def __init__(self, menu_item: MenuItem, quantity: int):
        self.menu_item = menu_item
        self.quantity = quantity

    @property
    def total_price(self) -> float:
        return self.menu_item.price * self.quantity

    @property
    def preparation_time(self) -> int:
        return self.menu_item.preparation_time


class Order:
    def __init__(self, order_id: str, customer_username: str, items: List[OrderItem], 
                 delivery_mode: DeliveryMode, delivery_address: Optional[str] = None):
        self.order_id = order_id
        self.customer_username = customer_username
        self.items = items
        self.delivery_mode = delivery_mode
        self.delivery_address = delivery_address
        self.status = OrderStatus.PLACED
        self.creation_time = datetime.datetime.now()
        self.estimated_completion_time = self._calculate_estimated_completion_time()
        self.assigned_delivery_agent: Optional[str] = None

    def _calculate_estimated_completion_time(self) -> datetime.datetime:
        # Calculate max preparation time across all items
        max_prep_time = max([item.preparation_time for item in self.items], default=0)
        
        # Add delivery time if it's a home delivery
        if self.delivery_mode == DeliveryMode.HOME_DELIVERY:
            # Assuming 30 minutes for delivery
            total_time = max_prep_time + 30
        else:
            total_time = max_prep_time
        
        return self.creation_time + datetime.timedelta(minutes=total_time)

    @property
    def total_price(self) -> float:
        return sum(item.total_price for item in self.items)

    def update_status(self, new_status: OrderStatus):
        self.status = new_status
        
        # Update estimated time based on status
        if new_status == OrderStatus.PREPARING:
            # No change to estimated time
            pass
        elif new_status == OrderStatus.READY_FOR_PICKUP:
            if self.delivery_mode == DeliveryMode.HOME_DELIVERY:
                # Reset the timer for delivery portion
                self.estimated_completion_time = datetime.datetime.now() + datetime.timedelta(minutes=30)
        elif new_status in [OrderStatus.DELIVERED, OrderStatus.PICKED_UP]:
            # Order is complete
            self.estimated_completion_time = datetime.datetime.now()

    def get_time_remaining(self) -> int:
        """Returns the estimated time remaining in minutes."""
        if self.status in [OrderStatus.DELIVERED, OrderStatus.PICKED_UP, OrderStatus.CANCELLED]:
            return 0
        
        time_remaining = (self.estimated_completion_time - datetime.datetime.now()).total_seconds() / 60
        return max(0, int(time_remaining))

    def assign_delivery_agent(self, agent_username: str):
        if self.delivery_mode == DeliveryMode.HOME_DELIVERY:
            self.assigned_delivery_agent = agent_username


class DeliveryAgent:
    def __init__(self, username: str, password: str, phone: str):
        self.username = username
        self.password = password
        self.phone = phone
        self.available = True
        self.current_orders: List[str] = []  # List of order IDs

    def assign_order(self, order_id: str):
        if order_id not in self.current_orders:
            self.current_orders.append(order_id)
            # Update availability - agent is unavailable when they have 3 or more orders
            self.available = len(self.current_orders) < 3

    def complete_order(self, order_id: str):
        if order_id in self.current_orders:
            self.current_orders.remove(order_id)
            # Always update availability after order changes
            self.available = len(self.current_orders) < 3
            # Ensure agent is available when they have fewer than 3 orders
            if len(self.current_orders) < 3:
                self.available = True