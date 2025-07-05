# Food Delivery System

## Software Requirements Specifications

### 1. Introduction

This document outlines the software requirements for an online food delivery system that connects customers with local restaurants for food delivery and takeaway services.

### 2. Functional Requirements

#### 2.1 User Management

- 1.1: The system shall allow users to register with username, password, address, and phone number.
- 1.2: The system shall support multiple user roles: Customer, Delivery Agent, and Administrator.
- 1.3: The system shall maintain user profiles and order history.
- 1.4: The system shall allow administrators to manage delivery agent accounts.

#### 2.2 Menu Management

- 2.1: The system shall allow restaurant staff (admin) to add, update, and remove menu items.
- 2.2: Each menu item shall include name, price, and preparation time.
- 2.3: The system shall display menu items to all users.

#### 2.3 Order Management

- 3.1: The system shall allow customers to browse restaurant menus.
- 3.2: The system shall allow customers to add multiple items with quantities to orders.
- 3.3: The system shall allow customers to specify delivery or takeaway preference.
- 3.4: The system shall generate a unique order ID for each order.
- 3.5: The system shall calculate the estimated delivery time based on preparation times.
- 3.6: The system shall update order status in real-time (Placed, Preparing, Ready for Pickup, Out for Delivery, Delivered).
- 3.7: The system shall allow customers to track their order status.
- 3.8: The system shall maintain order history for each user.

#### 2.4 Delivery Management

- 4.1: The system shall support multiple delivery agents.
- 4.2: The system shall allow administrators to manually assign orders to available delivery agents.
- 4.3: The system shall allow delivery agents to update order status (Out for Delivery, Delivered).
- 4.4: The system shall track agent availability based on current order load.

#### 2.5 Administrator Functions

- 5.1: The system shall allow administrators to manage menu items.
- 5.2: The system shall allow administrators to view all orders in the system.
- 5.3: The system shall allow administrators to update order status.
- 5.4: The system shall allow administrators to manage delivery agents.
- 5.5: The system shall provide a restaurant dashboard with order statistics.

### 3. Non-Functional Requirements

#### 3.1 Performance

- 1.1: The system shall load menu pages within 1 second.
- 1.2: The system shall process order placement within 2 seconds.
- 1.3: The system shall update order tracking information at intervals of no more than 20 seconds.

#### 3.2 Security

- 2.1: The system shall protect user data with appropriate access controls.
- 2.2: The system shall use secure authentication mechanisms.

#### 3.3 Reliability

- 3.1: The system shall maintain data consistency across all operations.
- 3.2: The system shall implement data backup through file-based storage.

#### 3.4 Scalability

- 4.1: The database design shall support future expansion of functionality.
- 4.2: The modular architecture shall allow for easy addition of new features.

#### 3.5 Usability

- 5.1: The command-line interface shall be intuitive and easy to navigate.
- 5.2: The system shall provide clear error messages and recovery options.

### 4. System Requirements

#### 4.1 Technical Requirements

- 1.1: The system shall utilize JSON file-based storage for data persistence.
- 1.2: The system shall maintain consistent data across related entities.

#### 4.2 Deployment Requirements

- 3.1: The system shall maintain state across restarts through file persistence.
- 3.2: The system shall be easy to install with minimal dependencies.

### 5. Use Cases

#### 5.1 Customer Use Cases

- 1.1: Place Food Order
  - Actor: Customer
  - Precondition: User is logged in
  - Main Flow:
    1. Customer browses restaurant menu
    2. Customer adds items to order with quantities
    3. Customer selects delivery or takeaway option
    4. Customer provides delivery address (if delivery selected)
    5. Customer confirms order
    6. System confirms order placement
  - Postcondition: Order is placed and available for restaurant staff

- 1.2: Track Order
  - Actor: Customer
  - Precondition: Customer has placed an order
  - Main Flow:
    1. Customer navigates to order history
    2. Customer selects active order
    3. System displays current order status
    4. System displays estimated delivery/pickup time
  - Postcondition: Customer is informed of order progress

#### 5.2 Delivery Agent Use Cases

- 2.1: View Assigned Orders
  - Actor: Delivery Agent
  - Precondition: Delivery agent is logged in
  - Main Flow:
    1. Agent views list of orders assigned to them
    2. Agent selects an order to view details
    3. System displays order information including delivery address
  - Postcondition: Agent is informed of orders that need to be delivered

- 2.2: Complete Delivery
  - Actor: Delivery Agent
  - Precondition: Agent has a delivery in progress
  - Main Flow:
    1. Agent selects order that has been delivered
    2. Agent marks order as delivered
    3. System updates order status
    4. System updates agent availability
  - Postcondition: Order is marked as delivered and removed from agent's active orders

#### 5.3 Administrator Use Cases

- 3.1: Manage Menu
  - Actor: System Administrator
  - Precondition: Administrator is logged in
  - Main Flow:
    1. Administrator navigates to menu management
    2. Administrator can add, update, or delete menu items
    3. Administrator provides item details (name, price, preparation time)
    4. System confirms changes to the menu
  - Postcondition: Menu is updated and changes are visible to customers

- 3.2: Assign Delivery Agent
  - Actor: System Administrator
  - Precondition: Administrator is logged in
  - Main Flow:
    1. Administrator views orders ready for delivery
    2. Administrator views available delivery agents
    3. Administrator assigns an agent to an order
    4. System updates order status to Out for Delivery
  - Postcondition: Order is assigned to a delivery agent for completion

## Implementation Overview

The food delivery system manages:
- User accounts (customers)
- Menu items for restaurants
- Order creation and tracking
- Delivery agent assignments
- Order status updates in real-time

The system follows a service-oriented architecture with clear separation of concerns between data models, business services, and the database layer.

## Features

### User Management
- User registration and authentication
- User profile management
- Order history tracking

### Menu Management
- Adding, updating, and removing menu items
- Menu item categorization
- Setting preparation times for accurate delivery estimates

### Order Management
- Browsing restaurant menus
- Adding items to cart
- Specifying delivery or takeaway preference
- Real-time order status tracking
- Estimated delivery time calculations

### Delivery Management
- Multiple delivery agent support
- Order assignment to available agents
- Order status updates by delivery agents

## System Architecture

The food delivery system implements a layered architecture to separate concerns and promote maintainability:

| Layer | Component | Role | Implementation |
|-------|-----------|------|----------------|
| Presentation | Command Line Interface | User interaction | `src/cli.py` provides role-based interfaces for customers, delivery agents and administrators |
| Business Logic | Service Layer | Core application logic | `src/services.py` contains domain-specific services for users, menu, orders and delivery agents |
| Data Model | Domain Models | Data representation | `src/models.py` defines entity classes with appropriate methods and properties |
| Data Access | Database | Data persistence | `src/database.py` handles JSON file storage and retrieval |

The system follows a data flow where:
1. CLI collects user input and invokes appropriate service methods
2. Services apply business logic and perform validations
3. Services interact with the database to retrieve or store data
4. Services return results to the CLI for display

### Classes and Methods

#### Domain Models

| Class | Key Methods | Purpose |
|-------|-------------|---------|
| `User` | `add_order(order_id)` | Stores customer details and manages order history |
| `MenuItem` | Properties only | Represents menu items with price and preparation time |
| `OrderItem` | `total_price`, `preparation_time` properties | Associates menu items with quantities in orders |
| `Order` | `_calculate_estimated_completion_time()`, `update_status(new_status)`, `get_time_remaining()`, `assign_delivery_agent(agent_username)` | Manages order lifecycle with status tracking |
| `DeliveryAgent` | `assign_order(order_id)`, `complete_order(order_id)` | Tracks delivery agent status and assignments |
| `OrderStatus` | Enum values | Defines valid order states (PLACED, PREPARING, etc.) |
| `DeliveryMode` | Enum values | Defines delivery options (HOME_DELIVERY, TAKEAWAY) |

#### Service Layer

| Service | Key Methods | Purpose |
|---------|-------------|---------|
| `UserService` | `register_user()`, `login_user()`, `get_user_details()`, `get_user_orders()` | Handles user operations and authentication |
| `MenuService` | `add_item()`, `get_all_items()`, `get_item()`, `update_item()`, `delete_item()` | Manages the restaurant menu |
| `OrderService` | `create_order()`, `get_order()`, `get_all_orders()`, `update_order_status()`, `cancel_order()` | Processes order operations with status transition validations |
| `DeliveryAgentService` | `register_agent()`, `login_agent()`, `get_agent_details()`, `get_agent_orders()`, `complete_order()`, `assign_agent_to_order()` | Manages delivery agent workflow |

#### Data Persistence

| Database Method Groups | Key Methods | Purpose |
|-----------------------|-------------|---------|
| User Operations | `add_user()`, `get_user()`, `authenticate_user()`, `get_user_orders()` | Store and retrieve user data |
| Menu Operations | `add_menu_item()`, `get_menu_item()`, `get_all_menu_items()`, `update_menu_item()`, `delete_menu_item()` | Manage menu data |
| Order Operations | `add_order()`, `get_order()`, `get_all_orders()`, `update_order()` | Handle order persistence |
| Delivery Agent Operations | `add_delivery_agent()`, `get_delivery_agent()`, `get_all_delivery_agents()`, `get_available_delivery_agents()` | Maintain delivery agent data |
| File Operations | `_load_users()`, `_save_users()`, etc. | Handle JSON serialization and file I/O |

#### CLI Interface Components

| Menu | Key Functions | Available Actions |
|------|--------------|-------------------|
| Main Menu | `main_menu()` | Customer login/registration, Agent login, Admin login |
| Customer Interface | `customer_menu()` | View menu, Place order, View orders, Track order |
| Delivery Agent Interface | `delivery_agent_menu()` | View assigned orders, Update order status, Complete delivery |
| Admin Interface | `admin_menu()` | Manage menu, View all orders, Update order status, Manage agents, Restaurant dashboard, Assign delivery agents |

### Implementation Details

The application uses:
- UUID generation for unique IDs for menu items and orders
- JSON files for persistent storage without requiring a database server
- Datetime objects for temporal tracking of orders
- A state machine approach for handling valid order status transitions

## Installation and Setup

### Prerequisites
- Python 3.6 or higher

### Setup
1. Clone the repository:
```bash
cd q1
```

2. Create data directory (optional, will be created automatically on first run):
```bash
mkdir data
```

## Running the Application

Run the main application with:
```bash
python src/cli.py
```

### Default Accounts
- **Customer**: username: `customer`, password: `password`
- **Delivery Agent**: username: `agent`, password: `password`
- **Admin**: username: `admin`, password: `admin123`

## Testing

### Instructions to Run Tests

Run the tests with:
```bash
python3 -m unittest testcases.test_food_delivery_system
```

### Test Cases and Coverage

The test suite contains comprehensive tests covering all major components of the system:

#### 1. Database Tests
- Test database connection establishment
- Test database initialization (table creation)
- Test sample data addition to verify database population

#### 2. User Model Tests
- Test user registration with valid information
- Test duplicate phone number rejection during registration
- Test successful user login with correct credentials
- Test login failure with incorrect password
- Test login failure with non-existent phone number
- Test retrieving user orders from the database

#### 3. Restaurant Model Tests
- Test adding new restaurants to the system
- Test retrieving all restaurants from the database
- Test fetching restaurant details by ID

#### 4. Order Model Tests
- Test order creation with delivery estimation
- Test order status updating functionality
- Test retrieving orders by user ID
- Test retrieving orders by restaurant ID
- Test formatting delivery time into human-readable format

#### 5. User Controller Tests
- Test user registration process through the controller
- Test user login with authentication
- Test failed login handling
- Test order placement through user interface
- Test viewing user order history

#### 6. Restaurant Controller Tests
- Test restaurant staff login authentication
- Test viewing restaurant-specific orders

#### 7. Admin Controller Tests
- Test admin login with correct credentials
- Test admin login failure with incorrect password
- Test restaurant addition through admin interface
- Test viewing all restaurants in the system
- Test viewing orders for specific restaurants

The tests use an in-memory database to allow for isolated testing without affecting persistent data.

### Detailed Test Documentation

The test suite includes 50 individual test cases organized by functionality:

| Category | Tests |
|----------|-------|
| User Management | Registration, login, profile retrieval |
| Menu Management | CRUD operations for menu items |
| Order Placement | Takeaway and delivery orders creation |
| Order Tracking | Status updates and time estimation |
| Delivery Agent | Registration, assignment, order completion |
| System Persistence | Data storage and retrieval |

Example test:
```python
def test_order_creation(self):
    """Test order creation functionality"""
    menu_items = self.menu_service.get_all_items()
    item_quantities = [(menu_items[0].item_id, 2), (menu_items[1].item_id, 1)]
    
    success, message = self.order_service.create_order(
        "testuser", item_quantities, DeliveryMode.TAKEAWAY)
    
    # Assertions to verify order creation
    self.assertTrue(success)
    self.assertTrue("Order placed successfully" in message)
```

## Project Structure

```
food-delivery-system/
├── data/               # Data storage directory
├── src/                # Source code
│   ├── __init__.py
│   ├── models.py       # Data models
│   ├── services.py     # Business logic
│   ├── database.py     # Data persistence
│   └── cli.py          # Command-line interface
├── testcases/          # Unit tests
│   ├── __init__.py
│   └── test_food_delivery_system.py
└── README.md           # This file
```

## Design Choices

### Service-Layer Architecture

The food delivery system follows a service-layer architecture rather than a strict MVC pattern:

1. Models (`models.py`): Handle data representation with entities like User, MenuItem, Order, etc.
2. Services (`services.py`): Provide business logic and operations for each domain
3. Database (`database.py`): Manages data persistence independent of business logic
4. CLI Interface (`cli.py`): Handles both display and user input processing

This layered approach provides clear separation of concerns without enforcing a rigid MVC structure.

### Service-Oriented Design
The system separates core functionality into domain-specific services (UserService, MenuService, OrderService, DeliveryAgentService), making the code modular and easier to maintain.

### JSON-Based Storage
The system uses JSON file-based storage for persistence, creating separate files for users, menu items, orders, and delivery agents. This approach requires no database server while ensuring data consistency through managed transactions.

### Order Status Workflow
The implementation defines a clear order status workflow with valid transitions:
- Placed → Preparing → Ready for Pickup → Out for Delivery/Picked Up → Delivered
- Placed/Preparing → Cancelled

These transitions are enforced through validation in the OrderService to maintain business logic integrity.

### Delivery Agent Availability
Delivery agents have an availability status determined by their current order load - an agent is marked as "unavailable" when handling three or more orders. This status updates automatically when orders are assigned or completed.

### Time Estimation System
The system calculates estimated completion times based on:
- Maximum preparation time among ordered items
- Additional delivery time (30 minutes) for home delivery orders
- Status updates that dynamically adjust the estimated completion time

### Role-Based Interface
The CLI provides distinct interfaces for three user roles:
- Customers: Browse menu, place orders, track orders
- Delivery Agents: View assignments, update delivery status
- Administrators: Manage menu, view orders, assign delivery agents

### Explicit Data Serialization
The system implements explicit serialization/deserialization between object models and JSON storage, ensuring proper data type preservation and consistency.
