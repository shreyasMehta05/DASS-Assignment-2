import os
from typing import List, Dict, Optional, Tuple
import time
from datetime import datetime

from src.models import DeliveryMode, OrderStatus
from src.services import UserService, MenuService, OrderService, DeliveryAgentService

class CLI:
    def __init__(self):
        self.user_service = UserService()
        self.menu_service = MenuService()
        self.order_service = OrderService()
        self.delivery_service = DeliveryAgentService()
        
        # Current session
        self.current_user = None
        self.current_agent = None
        self.is_admin = False
    
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self, title):
        """Print a formatted header"""
        self.clear_screen()
        print("=" * 50)
        print(f"{title:^50}")
        print("=" * 50)
        print()
    
    def wait_for_enter(self):
        """Wait for user to press Enter"""
        input("\nPress Enter to continue...")
    
    def main_menu(self):
        """Display the main menu"""
        while True:
            self.print_header("Food Delivery System")
            print("1. Customer Login")
            print("2. Register as Customer")
            print("3. Delivery Agent Login")
            print("4. Admin Login")
            print("5. Exit")
            
            choice = input("\nEnter your choice: ")
            
            if choice == '1':
                self.customer_login()
            elif choice == '2':
                self.register_customer()
            elif choice == '3':
                self.agent_login()
            elif choice == '4':
                self.admin_login()
            elif choice == '5':
                print("\nThank you for using our Food Delivery System!")
                break
            else:
                print("\nInvalid choice. Please try again.")
                self.wait_for_enter()
    
    def customer_login(self):
        """Handle customer login"""
        self.print_header("Customer Login")
        username = input("Enter username: ")
        password = input("Enter password: ")
        
        success, message = self.user_service.login_user(username, password)
        if success:
            self.current_user = username
            print(f"\n{message}")
            self.wait_for_enter()
            self.customer_menu()
        else:
            print(f"\nError: {message}")
            self.wait_for_enter()
    
    def register_customer(self):
        """Handle customer registration"""
        self.print_header("Customer Registration")
        username = input("Enter username: ")
        password = input("Enter password: ")
        address = input("Enter address: ")
        phone = input("Enter phone number: ")
        
        success, message = self.user_service.register_user(username, password, address, phone)
        print(f"\n{message}")
        self.wait_for_enter()
    
    def agent_login(self):
        """Handle delivery agent login"""
        self.print_header("Delivery Agent Login")
        username = input("Enter username: ")
        password = input("Enter password: ")
        
        success, message = self.delivery_service.login_agent(username, password)
        if success:
            self.current_agent = username
            print(f"\n{message}")
            self.wait_for_enter()
            self.delivery_agent_menu()
        else:
            print(f"\nError: {message}")
            self.wait_for_enter()
    
    def admin_login(self):
        """Handle admin login"""
        self.print_header("Admin Login")
        username = input("Enter admin username: ")
        password = input("Enter admin password: ")
        
        # Simple admin check (in a real system, use proper authentication)
        if username == "admin" and password == "admin123":
            self.is_admin = True
            print("\nAdmin login successful!")
            self.wait_for_enter()
            self.admin_menu()
        else:
            print("\nInvalid admin credentials.")
            self.wait_for_enter()
    
    def customer_menu(self):
        """Display customer menu"""
        while True:
            self.print_header(f"Customer Dashboard - Welcome, {self.current_user}")
            print("1. View Menu")
            print("2. Place Order")
            print("3. View My Orders")
            print("4. Track Order")
            print("5. Logout")
            
            choice = input("\nEnter your choice: ")
            
            if choice == '1':
                self.display_menu()
            elif choice == '2':
                self.place_order()
            elif choice == '3':
                self.display_user_orders()
            elif choice == '4':
                self.track_order()
            elif choice == '5':
                self.current_user = None
                print("\nLogged out successfully.")
                self.wait_for_enter()
                break
            else:
                print("\nInvalid choice. Please try again.")
                self.wait_for_enter()
    
    def display_menu(self):
        """Display the restaurant menu"""
        self.print_header("Restaurant Menu")
        
        menu_items = self.menu_service.get_all_items()
        if not menu_items:
            print("No menu items available.")
        else:
            print(f"{'ID':<36} | {'Name':<20} | {'Price':<8} | {'Prep Time':<10}")
            print("-" * 78)
            
            for item in menu_items:
                print(f"{item.item_id:<36} | {item.name:<20} | ${item.price:<7.2f} | {item.preparation_time} mins")
        
        self.wait_for_enter()
    
    def place_order(self):
        """Place a new order"""
        self.print_header("Place New Order")
        
        # Display menu first
        menu_items = self.menu_service.get_all_items()
        if not menu_items:
            print("No menu items available. Cannot place order.")
            self.wait_for_enter()
            return
        
        print(f"{'#':<3} | {'Name':<20} | {'Price':<8} | {'Prep Time':<10}")
        print("-" * 50)
        
        # Create a simpler mapping for item selection
        item_map = {}
        for i, item in enumerate(menu_items, 1):
            item_map[i] = item
            print(f"{i:<3} | {item.name:<20} | ${item.price:<7.2f} | {item.preparation_time} mins")
        
        # Select items for order
        order_items = []
        while True:
            try:
                item_choice = input("\nEnter item number (0 to finish): ")
                if item_choice == "0":
                    break
                
                item_num = int(item_choice)
                if item_num not in item_map:
                    print("Invalid item number. Please try again.")
                    continue
                
                quantity = int(input(f"Enter quantity for {item_map[item_num].name}: "))
                if quantity <= 0:
                    print("Quantity must be positive. Please try again.")
                    continue
                
                order_items.append((item_map[item_num].item_id, quantity))
                print(f"Added {quantity}x {item_map[item_num].name} to your order.")
                
            except ValueError:
                print("Please enter valid numbers.")
        
        if not order_items:
            print("No items selected. Order cancelled.")
            self.wait_for_enter()
            return
        
        # Select delivery mode
        print("\nSelect delivery mode:")
        print("1. Home Delivery")
        print("2. Takeaway")
        
        delivery_choice = input("Enter your choice (1/2): ")
        
        if delivery_choice == "1":
            delivery_mode = DeliveryMode.HOME_DELIVERY
            
            # Ask for custom delivery address or use default
            use_default = input("Use your default address? (y/n): ").lower()
            if use_default == 'y':
                delivery_address = None  # Will use the user's default address
            else:
                delivery_address = input("Enter delivery address: ")
        else:
            delivery_mode = DeliveryMode.TAKEAWAY
            delivery_address = None
        
        # Place the order
        success, message = self.order_service.create_order(
            self.current_user, 
            order_items, 
            delivery_mode, 
            delivery_address
        )
        
        print(f"\n{message}")
        self.wait_for_enter()
    
    def display_user_orders(self):
        """Display all orders for the current user"""
        self.print_header("My Orders")
        
        orders = self.user_service.get_user_orders(self.current_user)
        if not orders:
            print("You have no orders.")
        else:
            print(f"{'Order ID':<36} | {'Date':<19} | {'Status':<15} | {'Total':<8} | {'Delivery Type':<15}")
            print("-" * 100)
            
            for order in orders:
                date = order.creation_time.strftime("%Y-%m-%d %H:%M")
                print(f"{order.order_id:<36} | {date:<19} | {order.status.value:<15} | ${order.total_price:<7.2f} | {order.delivery_mode.value:<15}")
        
        self.wait_for_enter()
    
    def track_order(self):
        """Track a specific order"""
        self.print_header("Track Order")
        
        order_id = input("Enter order ID: ")
        order = self.order_service.get_order(order_id)
        
        if not order:
            print("Order not found.")
            self.wait_for_enter()
            return
        
        # Display order details
        print(f"Order ID: {order.order_id}")
        print(f"Status: {order.status.value}")
        print(f"Estimated Time Remaining: {order.get_time_remaining()} minutes")
        
        # Order items
        print("\nItems:")
        for item in order.items:
            print(f"- {item.quantity}x {item.menu_item.name} (${item.total_price:.2f})")
        
        print(f"\nTotal Price: ${order.total_price:.2f}")
        
        # Show delivery details if applicable
        if order.delivery_mode == DeliveryMode.HOME_DELIVERY:
            print(f"Delivery Address: {order.delivery_address}")
            if order.assigned_delivery_agent:
                agent = self.delivery_service.get_agent_details(order.assigned_delivery_agent)[1]
                if agent:
                    print(f"Delivery Agent: {agent.username}")
                    print(f"Agent Phone: {agent.phone}")
        
        self.wait_for_enter()
    
    def delivery_agent_menu(self):
        """Display delivery agent menu"""
        while True:
            self.print_header(f"Delivery Agent Dashboard - {self.current_agent}")
            print("1. View Assigned Orders")
            print("2. Update Order Status")
            print("3. Complete Order")
            print("4. Logout")
            
            choice = input("\nEnter your choice: ")
            
            if choice == '1':
                self.display_agent_orders()
            elif choice == '2':
                self.update_order_status()
            elif choice == '3':
                self.complete_delivery()
            elif choice == '4':
                self.current_agent = None
                print("\nLogged out successfully.")
                self.wait_for_enter()
                break
            else:
                print("\nInvalid choice. Please try again.")
                self.wait_for_enter()
    
    def display_agent_orders(self):
        """Display orders assigned to the current agent"""
        self.print_header("My Assigned Orders")
        
        orders = self.delivery_service.get_agent_orders(self.current_agent)
        if not orders:
            print("You have no assigned orders.")
        else:
            print(f"{'Order ID':<36} | {'Customer':<15} | {'Status':<20} | {'Delivery Address':<30}")
            print("-" * 105)
            
            for order in orders:
                print(f"{order.order_id:<36} | {order.customer_username:<15} | {order.status.value:<20} | {order.delivery_address:<30}")
        
        self.wait_for_enter()
    
    def update_order_status(self):
        """Update the status of an assigned order"""
        self.print_header("Update Order Status")
        
        orders = self.delivery_service.get_agent_orders(self.current_agent)
        if not orders:
            print("You have no assigned orders.")
            self.wait_for_enter()
            return
        
        print(f"{'#':<3} | {'Order ID':<36} | {'Status':<20}")
        print("-" * 63)
        
        order_map = {}
        for i, order in enumerate(orders, 1):
            order_map[i] = order
            print(f"{i:<3} | {order.order_id:<36} | {order.status.value:<20}")
        
        try:
            order_choice = int(input("\nSelect order number: "))
            if order_choice not in order_map:
                print("Invalid order number.")
                self.wait_for_enter()
                return
            
            selected_order = order_map[order_choice]
            
            # Show available status transitions
            current_status = selected_order.status
            
            if current_status == OrderStatus.READY_FOR_PICKUP:
                print("\nAvailable status updates:")
                print("1. Out for Delivery")
                
                choice = input("\nSelect new status (1): ")
                if choice == "1":
                    result, message = self.order_service.update_order_status(
                        selected_order.order_id, 
                        OrderStatus.OUT_FOR_DELIVERY
                    )
                    print(f"\n{message}")
                else:
                    print("\nInvalid choice.")
                    
            elif current_status == OrderStatus.OUT_FOR_DELIVERY:
                print("\nAvailable status updates:")
                print("1. Delivered")
                
                choice = input("\nSelect new status (1): ")
                if choice == "1":
                    result, message = self.delivery_service.complete_order(
                        self.current_agent,
                        selected_order.order_id
                    )
                    print(f"\n{message}")
                else:
                    print("\nInvalid choice.")
                    
            else:
                print(f"\nCannot update order with status '{current_status.value}' at this time.")
                
        except ValueError:
            print("\nInvalid input. Please enter a number.")
        
        self.wait_for_enter()
    
    def complete_delivery(self):
        """Mark an order as delivered"""
        self.print_header("Complete Order")
        
        orders = self.delivery_service.get_agent_orders(self.current_agent)
        out_for_delivery_orders = [order for order in orders if order.status == OrderStatus.OUT_FOR_DELIVERY]
        
        if not out_for_delivery_orders:
            print("You have no orders that are out for delivery.")
            self.wait_for_enter()
            return
        
        print(f"{'#':<3} | {'Order ID':<36} | {'Customer':<15} | {'Delivery Address':<30}")
        print("-" * 90)
        
        order_map = {}
        for i, order in enumerate(out_for_delivery_orders, 1):
            order_map[i] = order
            print(f"{i:<3} | {order.order_id:<36} | {order.customer_username:<15} | {order.delivery_address:<30}")
        
        try:
            order_choice = int(input("\nSelect order to complete: "))
            if order_choice not in order_map:
                print("Invalid order number.")
                self.wait_for_enter()
                return
            
            selected_order = order_map[order_choice]
            
            # Confirm delivery
            confirm = input(f"Confirm delivery of order {selected_order.order_id}? (y/n): ").lower()
            if confirm == 'y':
                result, message = self.delivery_service.complete_order(
                    self.current_agent,
                    selected_order.order_id
                )
                print(f"\n{message}")
            else:
                print("\nDelivery not confirmed.")
                
        except ValueError:
            print("\nInvalid input. Please enter a number.")
        
        self.wait_for_enter()
    
    def admin_menu(self):
        """Display admin menu"""
        while True:
            self.print_header("Restaurant Management")
            print("1. Manage Menu")
            print("2. View All Orders")
            print("3. Update Order Status")
            print("4. Manage Delivery Agents")
            print("5. Restaurant Dashboard")
            print("6. Assign Delivery Agent")
            print("7. Logout")
            
            choice = input("\nEnter your choice: ")
            
            if choice == '1':
                self.manage_menu()
            elif choice == '2':
                self.view_all_orders()
            elif choice == '3':
                self.admin_update_order_status()
            elif choice == '4':
                self.manage_delivery_agents()
            elif choice == '5':
                self.restaurant_dashboard()
            elif choice == '6':
                self.assign_delivery_agent()
            elif choice == '7':
                self.is_admin = False
                print("\nLogged out successfully.")
                self.wait_for_enter()
                break
            else:
                print("\nInvalid choice. Please try again.")
                self.wait_for_enter()
    
    def manage_menu(self):
        """Admin interface for menu management"""
        while True:
            self.print_header("Menu Management")
            print("1. View Menu")
            print("2. Add Menu Item")
            print("3. Update Menu Item")
            print("4. Delete Menu Item")
            print("5. Back to Admin Menu")
            
            choice = input("\nEnter your choice: ")
            
            if choice == '1':
                self.display_menu()
            elif choice == '2':
                self.add_menu_item()
            elif choice == '3':
                self.update_menu_item()
            elif choice == '4':
                self.delete_menu_item()
            elif choice == '5':
                break
            else:
                print("\nInvalid choice. Please try again.")
                self.wait_for_enter()
    
    def add_menu_item(self):
        """Add a new item to the menu"""
        self.print_header("Add Menu Item")
        
        name = input("Enter item name: ")
        
        try:
            price = float(input("Enter price: $"))
            if price <= 0:
                print("Price must be positive.")
                self.wait_for_enter()
                return
            
            prep_time = int(input("Enter preparation time (minutes): "))
            if prep_time <= 0:
                print("Preparation time must be positive.")
                self.wait_for_enter()
                return
            
            success, message = self.menu_service.add_item(name, price, prep_time)
            print(f"\n{message}")
            
        except ValueError:
            print("\nInvalid input. Please enter numeric values for price and preparation time.")
        
        self.wait_for_enter()
    
    def update_menu_item(self):
        """Update an existing menu item"""
        self.print_header("Update Menu Item")
        
        menu_items = self.menu_service.get_all_items()
        if not menu_items:
            print("No menu items available.")
            self.wait_for_enter()
            return
        
        print(f"{'#':<3} | {'ID':<36} | {'Name':<20} | {'Price':<8} | {'Prep Time':<10}")
        print("-" * 82)
        
        item_map = {}
        for i, item in enumerate(menu_items, 1):
            item_map[i] = item
            print(f"{i:<3} | {item.item_id:<36} | {item.name:<20} | ${item.price:<7.2f} | {item.preparation_time} mins")
        
        try:
            item_choice = int(input("\nSelect item to update: "))
            if item_choice not in item_map:
                print("Invalid item number.")
                self.wait_for_enter()
                return
            
            selected_item = item_map[item_choice]
            
            # Get updated values
            name = input(f"Enter new name (current: {selected_item.name}): ") or selected_item.name
            
            price_input = input(f"Enter new price (current: ${selected_item.price:.2f}): ")
            price = float(price_input) if price_input else selected_item.price
            
            prep_time_input = input(f"Enter new preparation time (current: {selected_item.preparation_time} mins): ")
            prep_time = int(prep_time_input) if prep_time_input else selected_item.preparation_time
            
            if price <= 0 or prep_time <= 0:
                print("Price and preparation time must be positive.")
                self.wait_for_enter()
                return
            
            success, message = self.menu_service.update_item(selected_item.item_id, name, price, prep_time)
            print(f"\n{message}")
            
        except ValueError:
            print("\nInvalid input. Please enter numeric values for price and preparation time.")
        
        self.wait_for_enter()
    
    def delete_menu_item(self):
        """Delete a menu item"""
        self.print_header("Delete Menu Item")
        
        menu_items = self.menu_service.get_all_items()
        if not menu_items:
            print("No menu items available.")
            self.wait_for_enter()
            return
        
        print(f"{'#':<3} | {'ID':<36} | {'Name':<20} | {'Price':<8} | {'Prep Time':<10}")
        print("-" * 82)
        
        item_map = {}
        for i, item in enumerate(menu_items, 1):
            item_map[i] = item
            print(f"{i:<3} | {item.item_id:<36} | {item.name:<20} | ${item.price:<7.2f} | {item.preparation_time} mins")
        
        try:
            item_choice = int(input("\nSelect item to delete: "))
            if item_choice not in item_map:
                print("Invalid item number.")
                self.wait_for_enter()
                return
            
            selected_item = item_map[item_choice]
            
            # Confirm deletion
            confirm = input(f"Are you sure you want to delete '{selected_item.name}'? (y/n): ").lower()
            if confirm == 'y':
                success, message = self.menu_service.delete_item(selected_item.item_id)
                print(f"\n{message}")
            else:
                print("\nDeletion cancelled.")
                
        except ValueError:
            print("\nInvalid input. Please enter a number.")
        
        self.wait_for_enter()
    
    def view_all_orders(self):
        """View all orders in the system"""
        self.print_header("All Orders")
        
        orders = self.order_service.get_all_orders()
        if not orders:
            print("No orders in the system.")
        else:
            print(f"{'Order ID':<36} | {'Customer':<15} | {'Status':<15} | {'Total':<8} | {'Type':<15}")
            print("-" * 95)
            
            for order in orders:
                print(f"{order.order_id:<36} | {order.customer_username:<15} | {order.status.value:<15} | ${order.total_price:<7.2f} | {order.delivery_mode.value:<15}")
        
        self.wait_for_enter()
    
    def admin_update_order_status(self):
        """Admin interface to update order status"""
        self.print_header("Update Order Status")
        
        orders = self.order_service.get_all_orders()
        active_orders = [order for order in orders if order.status not in 
                        [OrderStatus.DELIVERED, OrderStatus.PICKED_UP, OrderStatus.CANCELLED]]
        
        if not active_orders:
            print("No active orders to update.")
            self.wait_for_enter()
            return
        
        print(f"{'#':<3} | {'Order ID':<36} | {'Customer':<15} | {'Status':<15} | {'Type':<15}")
        print("-" * 90)
        
        order_map = {}
        for i, order in enumerate(active_orders, 1):
            order_map[i] = order
            print(f"{i:<3} | {order.order_id:<36} | {order.customer_username:<15} | {order.status.value:<15} | {order.delivery_mode.value:<15}")
        
        try:
            order_choice = int(input("\nSelect order to update: "))
            if order_choice not in order_map:
                print("Invalid order number.")
                self.wait_for_enter()
                return
            
            selected_order = order_map[order_choice]
            
            # Show available status transitions based on current status and delivery mode
            current_status = selected_order.status
            delivery_mode = selected_order.delivery_mode
            
            valid_transitions = {
                OrderStatus.PLACED: [OrderStatus.PREPARING, OrderStatus.CANCELLED],
                OrderStatus.PREPARING: [OrderStatus.READY_FOR_PICKUP, OrderStatus.CANCELLED],
                OrderStatus.READY_FOR_PICKUP: [
                    OrderStatus.OUT_FOR_DELIVERY if delivery_mode == DeliveryMode.HOME_DELIVERY else OrderStatus.PICKED_UP
                ],
                OrderStatus.OUT_FOR_DELIVERY: [OrderStatus.DELIVERED]
            }
            
            if current_status in valid_transitions:
                print("\nAvailable status updates:")
                for i, status in enumerate(valid_transitions[current_status], 1):
                    print(f"{i}. {status.value}")
                
                status_choice = int(input("\nSelect new status: "))
                if 1 <= status_choice <= len(valid_transitions[current_status]):
                    new_status = valid_transitions[current_status][status_choice - 1]
                    result, message = self.order_service.update_order_status(
                        selected_order.order_id, 
                        new_status
                    )
                    print(f"\n{message}")
                else:
                    print("\nInvalid choice.")
            else:
                print(f"\nCannot update order with status '{current_status.value}' at this time.")
                
        except ValueError:
            print("\nInvalid input. Please enter a number.")
        
        self.wait_for_enter()
    
    def manage_delivery_agents(self):
        """Admin interface for delivery agent management"""
        while True:
            self.print_header("Delivery Agent Management")
            print("1. Register New Delivery Agent")
            print("2. View All Delivery Agents")
            print("3. Back to Admin Menu")
            
            choice = input("\nEnter your choice: ")
            
            if choice == '1':
                self.register_delivery_agent()
            elif choice == '2':
                self.view_all_delivery_agents()
            elif choice == '3':
                break
            else:
                print("\nInvalid choice. Please try again.")
                self.wait_for_enter()
    
    def register_delivery_agent(self):
        """Register a new delivery agent"""
        self.print_header("Register Delivery Agent")
        
        username = input("Enter username: ")
        password = input("Enter password: ")
        phone = input("Enter phone number: ")
        
        success, message = self.delivery_service.register_agent(username, password, phone)
        print(f"\n{message}")
        self.wait_for_enter()
    
    def view_all_delivery_agents(self):
        """View all delivery agents in the system"""
        self.print_header("All Delivery Agents")
        
        # Get all delivery agents from service
        agents = self.delivery_service.get_all_agents()
        
        if not agents:
            print("No delivery agents registered in the system.")
            self.wait_for_enter()
            return
            
        print(f"{'Username':<20} | {'Phone':<15} | {'Available':<10} | {'Current Orders':<15}")
        print("-" * 65)
        
        for agent in agents:
            status = "Available" if agent.available else "Busy"
            order_count = len(agent.current_orders)
            print(f"{agent.username:<20} | {agent.phone:<15} | {status:<10} | {order_count:<15}")
        
        self.wait_for_enter()
    
    def restaurant_dashboard(self):
        """Show restaurant dashboard with real-time data"""
        self.print_header("Restaurant Dashboard")
        
        orders = self.order_service.get_all_orders()
        active_orders = [order for order in orders if order.status not in 
                        [OrderStatus.DELIVERED, OrderStatus.PICKED_UP, OrderStatus.CANCELLED]]
        
        # Order counts by status
        status_counts = {}
        for order in orders:
            status = order.status.value
            status_counts[status] = status_counts.get(status, 0) + 1
        
        # Daily order total
        today_orders = [order for order in orders if 
                       order.creation_time.date() == datetime.now().date()]
        today_revenue = sum(order.total_price for order in today_orders)
        
        # Display dashboard
        print(f"Active Orders: {len(active_orders)}")
        print(f"Total Orders Today: {len(today_orders)}")
        print(f"Total Revenue Today: ${today_revenue:.2f}")
        
        print("\nOrders by Status:")
        for status, count in status_counts.items():
            print(f"- {status}: {count}")
        
        print("\nRecent Active Orders:")
        if active_orders:
            print(f"{'Order ID':<36} | {'Customer':<15} | {'Status':<15} | {'Time Left':<10}")
            print("-" * 80)
            
            for order in sorted(active_orders, key=lambda o: o.get_time_remaining())[:5]:  # Show 5 most urgent orders
                print(f"{order.order_id:<36} | {order.customer_username:<15} | {order.status.value:<15} | {order.get_time_remaining()} mins")
        else:
            print("No active orders.")
        
        self.wait_for_enter()

    def assign_delivery_agent(self):
        """Assign a delivery agent to an order"""
        self.print_header("Assign Delivery Agent")
        
        # Get orders that need a delivery agent
        orders = self.order_service.get_all_orders()
        ready_orders = [order for order in orders 
                       if order.status == OrderStatus.READY_FOR_PICKUP 
                       and order.delivery_mode == DeliveryMode.HOME_DELIVERY 
                       and not order.assigned_delivery_agent]
        
        if not ready_orders:
            print("No orders require a delivery agent at this time.")
            self.wait_for_enter()
            return
            
        print("Orders ready for delivery:")
        print(f"{'#':<3} | {'Order ID':<36} | {'Customer':<15} | {'Delivery Address':<30}")
        print("-" * 90)
        
        order_map = {}
        for i, order in enumerate(ready_orders, 1):
            order_map[i] = order
            print(f"{i:<3} | {order.order_id:<36} | {order.customer_username:<15} | {order.delivery_address or 'N/A':<30}")
        
        try:
            order_choice = int(input("\nSelect order number: "))
            if order_choice not in order_map:
                print("Invalid order number.")
                self.wait_for_enter()
                return
                
            selected_order = order_map[order_choice]
            
            # Get available delivery agents
            available_agents = self.delivery_service.get_available_agents()
            
            if not available_agents:
                print("No delivery agents available at this time.")
                self.wait_for_enter()
                return
                
            print("\nAvailable delivery agents:")
            print(f"{'#':<3} | {'Username':<20} | {'Phone':<15} | {'Order Count':<12}")
            print("-" * 55)
            
            agent_map = {}
            for i, agent in enumerate(available_agents, 1):
                agent_map[i] = agent
                print(f"{i:<3} | {agent.username:<20} | {agent.phone:<15} | {len(agent.current_orders):<12}")
            
            agent_choice = int(input("\nSelect agent number: "))
            if agent_choice not in agent_map:
                print("Invalid agent number.")
                self.wait_for_enter()
                return
                
            selected_agent = agent_map[agent_choice]
            
            # Assign the agent to the order
            result, message = self.delivery_service.assign_agent_to_order(
                selected_order.order_id, 
                selected_agent.username
            )
            
            print(f"\n{message}")
            
        except ValueError:
            print("\nInvalid input. Please enter a number.")
        
        self.wait_for_enter()



def main():
    """Main entry point for the application"""
    # Create data directory if it doesn't exist
    import os
    os.makedirs("data", exist_ok=True)
    
    # Add sample data for demonstration if needed
    menu_service = MenuService()
    user_service = UserService()
    delivery_service = DeliveryAgentService()
    
    # Add sample menu items if no menu exists
    if len(menu_service.get_all_items()) == 0:
        menu_service.add_item("Margherita Pizza", 9.99, 15)
        menu_service.add_item("Pepperoni Pizza", 11.99, 18)
        menu_service.add_item("Veggie Burger", 8.50, 12)
        menu_service.add_item("Chicken Wings", 7.99, 20)
        menu_service.add_item("French Fries", 3.99, 8)
        menu_service.add_item("Chocolate Cake", 5.99, 5)
        menu_service.add_item("Caesar Salad", 6.99, 10)
        menu_service.add_item("Iced Tea", 2.50, 2)
    
    # Add a test customer if none exists
    success, _ = user_service.get_user_details("customer")
    if not success:
        user_service.register_user("customer", "password", "123 Main St", "555-1234")
    
    # Add a test delivery agent if none exists
    if not delivery_service.get_agent_details("agent")[0]:
        delivery_service.register_agent("agent", "password", "555-5678")
    
    # Start the CLI
    cli = CLI()
    cli.main_menu()

if __name__ == "__main__":
    main()