# Food Delivery System

A command-line food delivery management system that supports home delivery and takeaway orders, delivery agent management, and restaurant administration.

## Features

- **User Management:** Registration and authentication for customers
- **Order Processing:** Place orders for home delivery or takeaway
- **Menu Management:** Add, update, and delete menu items
- **Delivery Agent System:** Assign and manage delivery agents
- **Order Tracking:** Track order status and estimated delivery time
- **Restaurant Dashboard:** Real-time overview of orders and revenue

## System Requirements

- Python 3.6 or higher
- No external dependencies required

## Installation and Setup

1. Clone this repository or extract the files
2. Navigate to the project directory
3. Run the application:

```bash
python3 src/cli.py
```

## Default Test Accounts
For testing purposes, the application provides the following default accounts:

| User Type       | Username  | Password  |
|----------------|----------|-----------|
| Customer       | customer | password  |
| Delivery Agent | agent    | password  |
| Admin          | admin    | admin123  |

## User Guide
### Main Menu
When you start the application, you'll see the main menu with the following options:
```plaintext
1. Customer Login
2. Register as Customer
3. Delivery Agent Login
4. Admin Login
5. Exit
```

### Customer Interface
#### Registration
- Select `2. Register as Customer`
- Enter your username, password, address, and phone number.

#### Login
- Select `1. Customer Login`
- Enter your registered username and password.
  - **Default test credentials:**
    - Username: `customer`
    - Password: `password`

#### Customer Menu
After successful login, you'll access the customer menu:
```plaintext
1. View Menu
2. Place Order
3. View My Orders
4. Track Order
5. Logout
```

##### Placing an Order
- Select `2. Place Order` from the customer menu.
- Choose items from the menu by entering the item number and quantity.
- Enter `0` when finished selecting items.
- Choose delivery mode:
  - `1` for Home Delivery
  - `2` for Takeaway
- If Home Delivery is selected, use the default address or enter a new one.

##### Tracking an Order
- Select `4. Track Order` from the customer menu.
- Enter the order ID.
- View order status, estimated time remaining, delivery details, and other information.

### Delivery Agent Interface
#### Login
- Select `3. Delivery Agent Login`
- Enter your assigned username and password.
  - **Default test credentials:**
    - Username: `agent`
    - Password: `password`

#### Delivery Agent Menu
After login, you'll see the delivery agent interface:
```plaintext
1. View Assigned Orders
2. Update Order Status
3. Complete Order
4. Logout
```

##### Managing Deliveries
- View assigned orders: Select `1`
- Update the status of an order: Select `2`
  - Example: From "Ready for Pickup" to "Out for Delivery"
- Mark an order as delivered: Select `3`

### Administrator Interface
#### Login
- Select `4. Admin Login`
- Enter admin credentials:
  - **Username:** `admin`
  - **Password:** `admin123`

#### Admin Menu
After login, you'll access the restaurant management interface:
```plaintext
1. Manage Menu
2. View All Orders
3. Update Order Status
4. Manage Delivery Agents
5. Restaurant Dashboard
6. Assign Delivery Agent
7. Logout
```

##### Menu Management
- Select `1. Manage Menu` to:
  - View the current menu
  - Add new menu items with name, price, and preparation time
  - Update existing items
  - Delete menu items

##### Order Management
- View all orders: Select `2`
- Update order status: Select `3`
  - Example: Change status from "Placed" to "Preparing"

##### Delivery Agent Management
- Select `4. Manage Delivery Agents` to:
  - Register new delivery agents
  - View all delivery agents and their status

##### Assigning Delivery Agents
- Select `6. Assign Delivery Agent`
- Choose an order that's ready for delivery.
- Select an available delivery agent to assign the order.

##### Restaurant Dashboard
- Select `5. Restaurant Dashboard` to view:
  - Active orders count
  - Total orders and revenue for the day
  - Order counts by status
  - Recent active orders with time remaining

## Order Lifecycle
Orders progress through the following statuses:

| Status | Description | Next Possible Statuses |
|--------|-------------|------------------------|
| **PLACED** | Order is received by the system | PREPARING, CANCELLED |
| **PREPARING** | Restaurant is preparing the food | READY_FOR_PICKUP, CANCELLED |
| **READY_FOR_PICKUP** | Order is ready for pickup | OUT_FOR_DELIVERY (Home Delivery), PICKED_UP (Takeaway) |
| **OUT_FOR_DELIVERY** | Order is on the way | DELIVERED |
| **DELIVERED** | Order has been delivered | (Final state) |
| **PICKED_UP** | Order has been picked up | (Final state) |
| **CANCELLED** | Order has been cancelled | (Final state) |

## Data Persistence
All data is stored locally in JSON files in the `data` directory:

| File | Content | Description |
|------|---------|-------------|
| `users.json` | Customer information | Stores usernames, passwords (hashed), addresses, and order history |
| `menu_items.json` | Menu items | Stores item IDs, names, prices, and preparation times |
| `orders.json` | Order details | Stores complete order information including items, status, and timestamps |
| `delivery_agents.json` | Delivery agent information | Stores agent credentials, availability, and assigned orders |

## System Architecture
The application follows a layered architecture:

| Layer | Components | Responsibility |
|-------|------------|----------------|
| **Models** | User, MenuItem, OrderItem, Order, DeliveryAgent | Core business entities and logic |
| **Services** | UserService, MenuService, OrderService, DeliveryAgentService | Business logic implementation |
| **Database** | Database class | Data persistence and retrieval |
| **CLI** | CLI class | User interface and interaction handling |

### Class Descriptions

#### Models
| Class | Attributes | Purpose |
|-------|------------|---------|
| **User** | username, password, address, phone, order_history | Represents a customer account |
| **MenuItem** | item_id, name, price, preparation_time | Represents a food item on the menu |
| **OrderItem** | menu_item, quantity | Represents an item in a customer's order |
| **Order** | order_id, customer_username, items, delivery_mode, delivery_address, status, creation_time, estimated_completion_time, assigned_delivery_agent | Represents a customer order |
| **DeliveryAgent** | username, password, phone, available, current_orders | Represents a delivery agent account |

#### Services
| Service | Key Methods | Purpose |
|---------|-------------|---------|
| **UserService** | register_user(), login_user(), get_user_details(), get_user_orders() | Handles user-related operations |
| **MenuService** | add_item(), get_all_items(), update_item(), delete_item() | Handles menu-related operations |
| **OrderService** | create_order(), get_order(), update_order_status(), cancel_order() | Handles order-related operations |
| **DeliveryAgentService** | register_agent(), login_agent(), get_agent_orders(), complete_order(), assign_agent_to_order() | Handles delivery agent operations |

