# Design and Analysis of Software Systems (DASS) - Assignment 2
## Student Information
- **Name:** Shreyas Mehta
- **Roll No:** 2023101059
- **Semester:** 4th Semester
- **Course:** Design and Analysis of Software Systems

## Assignment Overview
This assignment implements three different software systems to demonstrate various software engineering concepts and practices:

1. **Food Delivery System (Q1):** A command-line application that models a food delivery service with multiple user roles and order tracking
2. **Gobblet of Fire Game (Q2):** A Pygame implementation with progressive code quality improvements through linting
3. **Dollmart E-commerce System (Q3):** An object-oriented e-commerce application with comprehensive class design and test coverage

### Complete Directory Structure
```
.
├── Commands.md         # Quick reference guide
├── Readme.md           # Main project documentation
├── q1/                 # Food Delivery System
│   ├── data/           # Data storage directory
│   ├── src/            # Source code
│   │   ├── __init__.py
│   │   ├── models.py   # Data models
│   │   ├── services.py # Business logic
│   │   ├── database.py # Data persistence
│   │   └── cli.py      # Command-line interface
│   └── testcases/      # Unit tests
│       ├── __init__.py
│       └── test_food_delivery_system.py
├── q2/                 # Gobblet of Fire Game
│   ├── AllLint/
│   │   ├── gobbletfinal.py     # Final version with best lint score
│   │   ├── gobblet_v2.py       # Progressive improvements
│   │   ├── gobblet_v3.py
│   │   ├── gobblet_v4.py
│   │   ├── gobblet_v5.py
│   │   ├── lintfinal.txt       # Final lint report
│   │   └── lintScore.txt       # Lint scores summary
│   ├── InitialLint/
│   │   └── initialLint.txt     # Initial lint report
│   ├── OriginalGame/
│   │   └── gobblet.py          # Original implementation
│   └── pic/
│       └── game-background.jpg # Game asset
└── q3/                 # Dollmart E-Commerce System
    ├── src/            # Source code
    │   ├── app.py      # Application logic
    │   ├── __init__.py
    │   ├── main.py     # Main application entry point
    │   ├── models/     # Domain models
    │   │   ├── customer.py
    │   │   ├── item.py
    │   │   ├── purchase.py
    │   │   ├── shipment.py
    │   │   ├── shopping_basket.py
    │   │   ├── transaction.py
    │   │   └── voucher.py
    │   └── utils/      # Utility functions
    ├── testcases/      # Test suites
    │   ├── test_customers.py
    │   ├── test_integration.py
    │   ├── test_items.py
    │   ├── test_purchases.py
    │   ├── test_shipments.py
    │   ├── test_shopping_basket.py
    │   ├── test_transactions.py
    │   └── test_vouchers.py
    ├── uml/            # UML diagrams
    │   ├── mermaid.txt # UML class diagram in Mermaid format
    │   └── uml.png     # UML diagram image
    ├── Report.md       # Design documentation
    ├── Test.md         # Test documentation
    └── run_tests.py    # Test runner script
```

## Assignment Tasks and Implementation

### Q1: Food Delivery System
A command-line food delivery application demonstrating service-oriented architecture and multi-user roles.

#### Learning Objectives Demonstrated
- Service-oriented architecture
- Domain modeling
- Persistence with JSON file storage
- Command-line interface design
- Role-based access control

## Overview

This project contains the implementation of three different software systems for DASS Assignment-2:

1. A Food Delivery System with multi-user roles and order tracking (Q1)
2. A Gobblet of Fire board game implementation with improved code quality through linting (Q2)
3. A Dollmart E-commerce System with comprehensive object-oriented design and test coverage (Q3)

## Index

1. **Food Delivery System (Q1)**
   - [Software Requirements Specifications](#software-requirements-specifications)
   - [Implementation Overview](#implementation-overview)
   - [Features](#features)
   - [System Architecture](#system-architecture)
   - [Running the Application](#running-the-application)
   - [Testing](#testing)
   - [Project Structure](#project-structure)
   - [Design Choices](#design-choices)

2. **Gobblet of Fire: Ignite the Battle (Q2)**
   - [Game Overview](#q2-gobblet-of-fire-ignite-the-battle)
   - [Assumptions](#assumptions)
   - [Directory Structure](#directory-structure)
   - [Running the Game](#running-the-game)
   - [Lint Results and Version Changes](#lint-results-and-version-changes)
   - [Conclusion](#conclusion)

3. **Dollmart E-Commerce System (Q3)**
   - [UML Diagram](#uml-diagram)
   - [UML Class Diagram and Multiplicity](#uml-class-diagram-multiplicity)
   - [Class Purpose & Responsibility](#class-purpose--responsibility)
   - [Design Decisions & Rationale](#design-decisions--rationale)
   - [Software Tools & Technologies](#software-tools--technologies)
   - [Test Documentation](#test-documentation)
   - [Testing Philosophy and Coverage](#testing-philosophy-and-coverage)
   - [Running the Tests](#running-the-tests)
  
4. **Quick Commands**
   - [Q1: Food Delivery System](#q1-food-delivery-system-commands)
   - [Q2: Gobblet of Fire Game](#q2-gobblet-of-fire-game-commands)
   - [Q3: Dollmart E-Commerce System](#q3-dollmart-e-commerce-system-commands)
   - [General Commands](#general-commands)

---
# Q1: Food Delivery System

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
  - Alternative Flow:
    - Order not confirmed: System displays error message
  - Postcondition: Order is placed and available for restaurant staff

- 1.2: Track Order
  - Actor: Customer
  - Precondition: Customer has placed an order
  - Main Flow:
    1. Customer navigates to order history
    2. Customer selects active order
    3. System displays current order status
    4. System displays estimated delivery/pickup time
  - Alternative Flow:
    - Order not found: System displays message to try again later
  - Postcondition: Customer is informed of order progress

#### 5.2 Delivery Agent Use Cases

- 2.1: View Assigned Orders
  - Actor: Delivery Agent
  - Precondition: Delivery agent is logged in
  - Main Flow:
    1. Agent views list of orders assigned to them
    2. Agent selects an order to view details
    3. System displays order information including delivery address
  - Alternative Flow:
    - No orders assigned: System displays message to try again later
  - Postcondition: Agent is informed of orders that need to be delivered

- 2.2: Complete Delivery
  - Actor: Delivery Agent
  - Precondition: Agent has a delivery in progress
  - Main Flow:
    1. Agent selects order that has been delivered
    2. Agent marks order as delivered
    3. System updates order status
    4. System updates agent availability
  - Alternative Flow:
    - Agent cannot complete delivery: System displays error message
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
  - Alternative Flow:
    - Invalid item details: System displays error message
  - Postcondition: Menu is updated and changes are visible to customers

- 3.2: Assign Delivery Agent
  - Actor: System Administrator
  - Precondition: Administrator is logged in
  - Main Flow:
    1. Administrator views orders ready for delivery
    2. Administrator views available delivery agents
    3. Administrator assigns an agent to an order
    4. System updates order status to Out for Delivery
  - Alternative Flow:
    - No available agents: System displays message to try again later
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


## Running the Application

Run the main application with:
```bash
python3 src/cli.py
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


## Q2 Gobblet of Fire: Ignite the Battle


---


This project implements the board game **Gobblet of Fire: Ignite the Battle** using Pygame. The game logic and rendering are defined in multiple Python modules that were iteratively improved through various linting passes.

## Assumptions


- **Fixed Board and Pieces:**  
  The game is built on a fixed 3x3 board, and each player has pieces of three sizes (small, medium, large). The dimensions (e.g., screen size of 800x800 pixels, cell size of 100 pixels) are fixed within the code.

- **User Input:**  
  The game is designed for desktop environments with mouse input.

- **Game Rules:**  
  The game follows the rules of Gobblet, where players can place pieces on the board, move pieces within the board, and gobble up smaller pieces. The game ends when a player has four pieces in a row or when the board is full.

- **No Bot or AI:**  
  The game does not include a bot or AI opponent. It is designed for two human players to take turns.

- **Single Device:**  
  The game is intended to be played on a single device, with players alternating turns on the same screen.

- **No Network Play:**  
  The game does not support network play or multiplayer modes. It is a local two-player game.

- **No undo/redo:**  
  The game does not include undo/redo functionality. Players must be careful with their moves.



- **Pygame Library:**
  The game uses the Pygame library for rendering graphics and handling user input.

## Directory Structure

The project directory is organized as follows:

```
q2/
├── AllLint/
│   ├── gobbletfinal.py
│   ├── gobblet_v2.py
│   ├── gobblet_v3.py
│   ├── gobblet_v4.py
│   ├── gobblet_v5.py
│   ├── lintfinal.txt
│   └── lintScore.txt
├── InitialLint/
│   └── initialLint.txt
├── OriginalGame/
│   └── gobblet.py
└── pic/
    └── game-background.jpg
```


- **OriginalGame/** contains the initial version of the game code.
- **InitialLint/** includes the lint results for the original version.
- **AllLint/** holds several iterations of the game code (from v2 through gobbletfinal.py) along with updated lint scores and reports.
- **pic/** stores the background image asset used by the game.
- **NOTE:** The final version of the game is `gobbletfinal.py` and is same as `gobblet_v5.py`.

## Running the Game
- To run the game first navigate to q2 folder:
    ```bash
    cd q2
    ```
- Run the final version of the game:
    ```bash
    python3 AllLint/gobbletfinal.py
    ```
- Run the original version of the game:
    ```bash
    python3 OriginalGame/gobblet.py
    ```
- Store the linting results in a text file:
    ```bash
    pylint AllLint/gobbletfinal.py > AllLint/lintfinal.txt
    ```
- View the linting score:
    ```bash
    cat AllLint/lintScore.txt
    ```
- Store the initial linting results in a text file:
    ```bash
    pylint OriginalGame/gobblet.py > InitialLint/initialLint.txt
    ```
- View the initial linting score:
    ```bash
    cat InitialLint/initialLint.txt
    ```
- Note: The game is designed for desktop environments with mouse input.
## Lint Results and Version Changes

### OriginalGame/gobblet.py
- **Lint Score:** 5.10/10  
- **Issues Identified:**
  - Trailing whitespace on many lines.
  - Several lines exceeding the 100-character limit.
  - Missing module and function docstrings.
  - Unused imports (e.g., `os`, `random`, and unused types from `typing`).
  - Variable redefinitions (e.g., reusing the name `screen`).
  - Warnings related to PyGame (e.g., missing members like `pygame.init`, `pygame.error`, `pygame.SRCALPHA`, etc.).

- **Changes Made:**  
  Removed some trailing whitespace, split some long lines.

---

### AllLint/gobblet_v2.py
- **Lint Score:** 5.31/10  
- **Issues Identified:**  
  Similar to the original version with trailing whitespace and line-length issues.

- **Changes Made:**  
  Further cleanup of trailing whitespace and adjustment of long lines to enhance readability and added some docstrings to functions.

---

### AllLint/gobblet_v3.py
- **Lint Score:** 7.99/10  
- **Issues Identified:**
  - Unnecessary "elif" after a return statement.
  - Redefined variable names (e.g., shadowing the global `screen`).
  - Unused variables.
  - Too few public methods in some classes.

- **Changes Made:**  
  Removed unnecessary `elif` statements, fixed variable redefinitions, and cleaned up unused variables. These changes helped improve code clarity and reduced redundancy. And also checked import order and added docstrings to classes.

---

### AllLint/gobblet_v4.py
- **Lint Score:** 8.45/10  
- **Issues Identified:**
  - Minor line-length issues.
  - Persistent PyGame member warnings.

- **Changes Made:**  
  Renamed parameters (e.g., using `surface` instead of `screen` in drawing methods) to avoid shadowing global variables. Inline pylint disables were added to handle known PyGame false‐positives (e.g., for `pygame.init`, `pygame.error`, `pygame.SRCALPHA`, etc.). Additionally, long function calls were split to satisfy the line-length requirement, and local variable counts were reduced.

---

### AllLint/gobblet_v5.py and gobbletfinal.py
- **Lint Score:** 9.91/10  
- **Issues Identified:**  
  A few remaining minor issues with line lengths and local variable counts in certain functions.

- **Changes Made:**  
    None
---

## Conclusion

The project has undergone a series of improvements based on linting feedback—from the original version (5.10/10) to the final version (9.91/10). Each version addressed specific issues ranging from trailing whitespace and long lines to more intricate concerns like variable shadowing and unnecessary code constructs. The final code is clean, well-documented, and structured for maintainability and readability.

---


# Q3: Dollmart E-Commerce System: Design & Implementation Report

## Assumptions

The Dollmart E-commerce System was implemented with the following assumptions:

1. **In-Memory Data Storage**: The system uses in-memory data structures rather than persistent database storage. All data exists only for the duration of the program execution.

2. **Simulated Shipping Process**: The delivery process is simulated using background threads that automatically progress shipments through various status stages.

3. **Single Session Operation**: While the system is designed to handle multiple users with separate shopping baskets, it assumes sequential access rather than truly concurrent operations.

4. **Simplified Authentication**: User authentication is implemented as a simple username/password match without encryption or advanced security features.

5. **Limited Payment Processing**: Payment processing is simulated and always succeeds. No actual payment gateway integration is implemented.

6. **Fixed Currency**: All monetary values are assumed to be in a single currency with no support for currency conversion or international pricing.

7. **No Tax Calculation**: The system doesn't implement tax calculations that would be required in a real-world application.

8. **Simplified Business Rules**: Business client bulk ordering has simplified validation logic compared to real-world requirements.

9. **Thread Safety Limitations**: While multiple threads are used for background operations like shipment status updates, not all operations are fully thread-safe.

10. **No Data Validation**: Input validation is minimal and doesn't cover all possible edge cases that would be handled in a production system.

## UML Diagram
[![UML Diagram](/q3/uml/uml.png)](/q3/uml/uml.png)

## UML Class Diagram Multiplicity

The UML diagram for the Dollmart system uses multiplicity indicators to show the relationships between classes. Multiplicity defines how many instances of one class can be associated with instances of another class.

| Relationship | Multiplicity | Explanation |
|--------------|--------------|-------------|
| Customer -- Purchase | 1 to 0..* | One customer can have zero or many purchases |
| Purchase -- Item | 1 to 1..* | One purchase contains one or many items |
| Purchase -- Shipment | 1 to 1 | One purchase creates exactly one shipment |
| ShoppingBasket -- Purchase | 1 to 0..* | One shopping basket can create multiple purchases |
| Customer -- Voucher | 1 to 0..* | One customer can validate multiple vouchers |
| ShoppingBasket -- Item | 1 to 0..* | One shopping basket can contain multiple items |
| Purchase -- Transaction | 1 to 1 | One purchase is processed by one transaction |

## Class Purpose & Responsibility

| Class | Primary Responsibility | Explanation |
|-------|--------------------------|-------------|
| Customer (Abstract) | User management | Abstract base class implementing common functionality for different user types including authentication, profile management, and order history tracking |
| PersonalClient | Individual shopping | Extends Customer with personal shopping capabilities and standard discount validation |
| BusinessClient | Bulk purchasing | Extends Customer with wholesale/bulk order functionality and tax identification |
| Item | Product management | Encapsulates product data, inventory tracking, and stock management |
| ItemFinder | Search functionality | Provides static search methods for finding products by different criteria |
| ShoppingBasket | Cart management | Maintains shopping carts for multiple users with isolation between sessions |
| Purchase | Order processing | Records finalized orders with payment, shipping, and item details |
| Shipment | Delivery tracking | Manages the delivery process with automated status updates |
| Transaction | Payment processing | Handles payment operations and receipt generation |
| Voucher | Discount management | Implements time-limited discount codes with validation |

## Design Decisions & Rationale

### 1. System Architecture

The Dollmart system uses an object-oriented design pattern with clear separation of concerns. This approach was chosen for several reasons:

- **Modularity**: Each class has a well-defined responsibility, making the system easier to maintain and extend
- **Encapsulation**: Implementation details are hidden behind clean interfaces
- **Polymorphism**: The abstract Customer class allows treating different customer types uniformly
- **Reusability**: Components can be reused across the application

### 2. Class Division Strategy

The system's functionality is divided into distinct classes based on domain concepts:

#### User Management
- **Abstract Customer Class**: Provides a common interface for all customer types
- **Customer Type Specializations**: Different implementations for personal and business clients with specific business rules
- **Rationale**: This approach allows adding new customer types without modifying existing code, following the Open-Closed Principle

#### Product & Inventory Management
- **Item Class**: Manages product information and inventory
- **ItemFinder**: Separates search logic from item data
- **Rationale**: This separation allows complex search algorithms to be implemented without modifying the core Item class

#### Order Processing
- **ShoppingBasket**: Multi-user basket management
- **Purchase**: Immutable record of completed orders
- **Rationale**: Keeping basket (mutable) separate from purchase (immutable) supports the principle of command-query separation

#### Delivery & Fulfillment
- **Shipment Class**: Dedicated to delivery tracking with background status updates
- **Rationale**: Using a background thread for status updates provides real-time simulation without blocking the main thread

### 3. Design Patterns Used

Several design patterns were incorporated to solve specific challenges:

- **Factory Method**: Used in shopping basket checkout to create purchase objects
- **Strategy Pattern**: Applied in payment processing to handle different payment methods
- **Observer Pattern**: Used between purchase and shipment for status updates
- **Singleton (avoided)**: Multiple instances allowed for better testability and less coupling

### 4. Data Management

Unlike traditional e-commerce systems that might use external databases, Dollmart uses in-memory data structures:

- **In-Memory Collections**: Lists and dictionaries store application state
- **Rationale**: Simplifies the implementation for demonstration purposes while maintaining appropriate data structures

If this were a production system, we would instead use:
- **Database**: PostgreSQL for transactional data with proper schema design
- **Redis**: For session management and caching frequently accessed data
- **Search Engine**: Elasticsearch for efficient product search functionality

### 5. Concurrency Management

The system handles concurrent operations through:

- **Dictionary-Based Isolation**: Each user's basket is kept separate by using customer IDs as keys
- **Thread Safety**: Background processes like shipment updates run in separate threads
- **Rationale**: This approach balances simplicity with the ability to handle multiple users

### 6. Error Handling Strategy

The system implements defensive programming through:

- **Input Validation**: Methods validate parameters before processing
- **Graceful Degradation**: Returning sensible defaults (empty lists, zero values) when resources don't exist
- **Rationale**: Makes the system more robust against unexpected inputs without excessive error handling

### 7. Testing Approach

A comprehensive test suite was developed with:

- **Unit Tests**: Testing individual components in isolation
- **Integration Tests**: Testing interactions between components
- **Edge Case Coverage**: Explicitly testing boundary conditions and unexpected inputs
- **Rationale**: Ensures system reliability and simplifies future maintenance

## Software Tools & Technologies

| Tool/Technology | Purpose | Rationale |
|----------------|---------|-----------|
| Python 3.10 | Implementation language | Chosen for readability, strong OOP support, and extensive standard library |
| Pytest | Testing framework | Selected for its simple syntax, fixture support, and parameterized testing capabilities |
| Threading module | Concurrent operations | Used for background processes like delivery status updates |
| Mermaid.js | UML diagram generation | Provides version-controllable diagrams that can be maintained alongside code |
| Git | Version control | Enables collaborative development and history tracking |

## Conclusion

The Dollmart e-commerce system demonstrates a well-structured object-oriented design that balances simplicity and functionality. The design decisions prioritize:

1. **Maintainability**: Through clear separation of concerns and encapsulation
2. **Extensibility**: Via appropriate abstractions and inheritance
3. **Testability**: With dependency injection and modular components
4. **Reliability**: Through comprehensive test coverage

These priorities reflect industry best practices for developing maintainable software systems, especially for domains like e-commerce where requirements frequently evolve and reliability is critical.


# Dollmart E-Commerce System Test Documentation

This document provides an overview of the comprehensive test suite created for the Dollmart e-commerce system. The test suite follows the principles of thorough unit testing and integration testing to ensure the system functions correctly in both normal operation and edge cases.

## Test Suite Overview

The test suite consists of over 90 test cases divided into several modules corresponding to the main components of the system. Each test has been designed to validate specific functionality and handle potential edge cases.

## Test Cases by Module

### 1. Customer Tests (20 tests)

| Test Case | Purpose | Functionality Tested | Edge Cases |
|-----------|---------|---------------------|------------|
| `test_personal_client_creation` | Verify personal customer accounts can be created | Account creation | ✓ |
| `test_business_client_creation` | Verify business customer accounts can be created | Account creation | ✓ |
| `test_unique_customer_ids` | Ensure each customer gets a unique ID | ID generation | ✓ |
| `test_business_unique_tax_ids` | Ensure business customers get unique tax IDs | Tax ID generation | ✓ |
| `test_successful_authentication` | Verify login works with correct credentials | Authentication | ✓ |
| `test_failed_authentication` | Verify login fails with incorrect credentials | Authentication | ✓ |
| `test_empty_password_authentication` | Test authentication with empty password | Authentication | ✓ |
| `test_end_session` | Test user logout functionality | Session management | ✓ |
| `test_update_password` | Test password change functionality | Profile modification | ✓ |
| `test_update_address` | Test address change functionality | Profile modification | ✓ |
| `test_unknown_attribute_modification` | Test behavior when modifying unknown attributes | Error handling | ✓ |
| `test_personal_client_add_to_basket` | Test adding items to basket as personal client | Shopping | ✓ |
| `test_personal_client_add_insufficient_inventory` | Test behavior when insufficient stock | Inventory validation | ✓ |
| `test_business_client_bulk_order` | Test bulk ordering for business clients | Bulk purchasing | ✓ |
| `test_business_client_below_minimum_quantity` | Test bulk order below minimum quantity | Business rules | ✓ |
| `test_business_client_insufficient_inventory` | Test bulk order with insufficient stock | Inventory validation | ✓ |
| `test_valid_voucher` | Test using valid discount vouchers | Discount application | ✓ |
| `test_expired_voucher` | Test behavior with expired vouchers | Voucher validation | ✓ |
| `test_nonexistent_voucher` | Test using voucher codes that don't exist | Error handling | ✓ |
| `test_case_sensitive_voucher_code` | Test voucher code case sensitivity | Input validation | ✓ |

### 2. Item Tests (19 tests)

| Test Case | Purpose | Functionality Tested | Edge Cases |
|-----------|---------|---------------------|------------|
| `test_basic_item_creation` | Test creating items with valid attributes | Item management | ✓ |
| `test_item_unique_ids` | Ensure each item gets a unique ID | ID generation | ✓ |
| `test_item_with_zero_inventory` | Test creating items with zero inventory | Inventory edge case | ✓ |
| `test_item_with_decimal_price` | Test items with non-integer prices | Price handling | ✓ |
| `test_verify_availability` | Test stock availability checking | Inventory management | ✓ |
| `test_reduce_inventory` | Test reducing inventory after purchase | Inventory management | ✓ |
| `test_reduce_zero_quantity` | Test reducing inventory by zero | Zero quantity edge case | ✓ |
| `test_reduce_entire_inventory` | Test reducing inventory to zero | Inventory depletion | ✓ |
| `test_text_search_in_title` | Test searching items by title text | Search functionality | ✓ |
| `test_text_search_in_description` | Test searching items by description | Search functionality | ✓ |
| `test_text_search_case_insensitive` | Test case-insensitive search | Search flexibility | ✓ |
| `test_text_search_no_results` | Test searching with no matches | Empty results handling | ✓ |
| `test_text_search_empty_string` | Test searching with empty string | Empty input edge case | ✓ |
| `test_price_range_exact_match` | Test price search with exact match | Price filtering | ✓ |
| `test_price_range_inclusive_bounds` | Test price range with inclusive bounds | Range filtering | ✓ |
| `test_price_range_no_results` | Test price range with no matches | Empty results handling | ✓ |
| `test_price_range_inverted_boundaries` | Test price range with min > max | Input validation | ✓ |
| `test_classification_search` | Test category-based search | Category filtering | ✓ |
| `test_classification_search_case_insensitive` | Test case-insensitive category search | Search flexibility | ✓ |

### 3. Shopping Basket Tests (16 tests)

| Test Case | Purpose | Functionality Tested | Edge Cases |
|-----------|---------|---------------------|------------|
| `test_add_product_new_basket` | Test adding products to new basket | Basket creation | ✓ |
| `test_add_product_existing_item` | Test adding more of existing product | Quantity aggregation | ✓ |
| `test_add_multiple_products` | Test adding different products | Multi-item baskets | ✓ |
| `test_add_zero_quantity` | Test adding zero quantity of an item | Zero quantity edge case | ✓ |
| `test_remove_product` | Test removing products from basket | Item removal | ✓ |
| `test_remove_nonexistent_product` | Test removing items not in basket | Error handling | ✓ |
| `test_remove_from_nonexistent_basket` | Test removing from invalid basket | Error handling | ✓ |
| `test_multiple_customer_baskets` | Test basket isolation between users | Multi-user support | ✓ |
| `test_get_empty_basket` | Test fetching empty basket contents | Empty basket handling | ✓ |
| `test_get_nonexistent_basket` | Test fetching invalid basket | Error handling | ✓ |
| `test_checkout_empty_basket` | Test checkout with empty basket | Empty basket handling | ✓ |
| `test_checkout_updates_inventory` | Test inventory updates after checkout | Inventory management | ✓ |
| `test_checkout_clears_basket` | Test basket clearing after checkout | Basket management | ✓ |
| `test_checkout_creates_purchase` | Test purchase creation on checkout | Order creation | ✓ |
| `test_checkout_with_discount` | Test checkout with applied discount | Discount application | ✓ |

### 4. Purchase Tests (13 tests)

| Test Case | Purpose | Functionality Tested | Edge Cases |
|-----------|---------|---------------------|------------|
| `test_direct_purchase_creation` | Test creating purchase without basket | Order creation | ✓ |
| `test_purchase_with_different_customers` | Test purchases for different customers | Multi-user support | ✓ |
| `test_purchase_id_increments` | Test auto-incrementing purchase IDs | ID generation | ✓ |
| `test_purchase_with_zero_items` | Test purchase with no items | Empty order edge case | ✓ |
| `test_purchase_with_negative_discount` | Test purchase with negative discount | Negative value edge case | ✓ |
| `test_additional_discount_application` | Test applying discounts after creation | Discount modification | ✓ |
| `test_shipment_creation` | Test shipment creation with purchase | Order fulfillment | ✓ |
| `test_purchase_status_updates` | Test purchase status changes | Order tracking | ✓ |
| `test_purchase_in_customer_history` | Test purchases added to customer history | Order history | ✓ |

### 5. Shipment Tests (9 tests)

| Test Case | Purpose | Functionality Tested | Edge Cases |
|-----------|---------|---------------------|------------|
| `test_basic_shipment_creation` | Test creating shipments | Shipment creation | ✓ |
| `test_shipment_with_purchase_reference` | Test shipment-purchase association | Order tracking | ✓ |
| `test_shipment_unique_ids` | Test uniqueness of shipment IDs | ID generation | ✓ |
| `test_tracking_code_format` | Test tracking code format | Data validation | ✓ |
| `test_arrival_date_calculation` | Test delivery date calculation | Date handling | ✓ |
| `test_get_status` | Test getting shipment status info | Status tracking | ✓ |
| `test_manual_status_update` | Test manually updating shipment status | Status management | ✓ |
| `test_auto_status_update` | Test automatic status progression | Background processing | ✓ |
| `test_purchase_status_update_on_delivery` | Test purchase status updates on delivery | Status synchronization | ✓ |

### 6. Transaction Tests (9 tests)

| Test Case | Purpose | Functionality Tested | Edge Cases |
|-----------|---------|---------------------|------------|
| `test_basic_transaction_creation` | Test creating payment transactions | Payment processing | ✓ |
| `test_zero_amount_transaction` | Test payments with zero amount | Zero value edge case | ✓ |
| `test_negative_amount_transaction` | Test payments with negative amount | Refund scenario | ✓ |
| `test_different_payment_methods` | Test various payment methods | Payment options | ✓ |
| `test_transaction_unique_ids` | Test uniqueness of transaction IDs | ID generation | ✓ |
| `test_receipt_creation` | Test generating payment receipts | Document generation | ✓ |
| `test_payment_processing_success` | Test successful payment processing | Payment acceptance | ✓ |
| `test_different_payment_details` | Test various payment detail formats | Payment flexibility | ✓ |
| `test_transaction_with_purchase` | Test transactions linked to purchases | Purchase-payment linkage | ✓ |

### 7. Voucher Tests (11 tests)

| Test Case | Purpose | Functionality Tested | Edge Cases |
|-----------|---------|---------------------|------------|
| `test_voucher_creation` | Test creating discount vouchers | Voucher creation | ✓ |
| `test_voucher_with_custom_validity` | Test creating vouchers with custom validity | Expiration handling | ✓ |
| `test_expired_voucher_creation` | Test creating already expired vouchers | Past expiry edge case | ✓ |
| `test_zero_validity_voucher` | Test vouchers that expire today | Same-day expiry | ✓ |
| `test_valid_voucher` | Test voucher validity checking | Validity verification | ✓ |
| `test_expired_voucher` | Test expired voucher validation | Expiration handling | ✓ |
| `test_expiring_today_voucher` | Test vouchers expiring today | Edge case handling | ✓ |
| `test_about_to_expire_voucher` | Test vouchers about to expire | Near-expiry edge case | ✓ |
| `test_basic_discount_calculation` | Test discount calculation | Discount computation | ✓ |
| `test_discount_with_decimal_price` | Test discounts on decimal prices | Precision handling | ✓ |
| `test_discount_with_zero_price` | Test discounts on zero price | Zero value edge case | ✓ |

### 8. Integration Tests (3 tests)

| Test Case | Purpose | Functionality Tested | Edge Cases |
|-----------|---------|---------------------|------------|
| `test_personal_customer_shopping_flow` | Test complete shopping flow for individuals | End-to-end process | ✓ |
| `test_business_customer_shopping_flow` | Test bulk ordering flow for businesses | End-to-end process | ✓ |
| `test_search_and_purchase_flow` | Test product search and purchase flow | Multi-step process | ✓ |

## Testing Philosophy and Coverage

The test suite was designed with these key principles in mind:

1. **Comprehensive Coverage**: Tests cover all major system components and their interactions.

2. **Edge Case Testing**: Special attention given to boundary conditions, zero values, and unexpected inputs.

3. **Isolation**: Each unit test focuses on testing a single functionality without dependencies.

4. **Integration**: Integration tests verify that components work correctly together.

5. **Regression Prevention**: Tests help ensure that code changes don't break existing functionality.

## Why This Level of Testing Is Important

- **Quality Assurance**: Ensures the system behaves as expected in all situations
- **Maintainability**: Makes future changes safer by catching regressions early
- **Documentation**: Tests serve as executable documentation of expected behavior
- **Robustness**: Helps identify and handle edge cases that might occur in production
- **Design Feedback**: Test-driven development improves overall system design

## Running the Tests

Tests can be executed with the provided `run_tests.py` script:

```bash
python3 run_tests.py
```

To run specific test modules:

```bash
python3 run_tests.py testcases/test_customers.py
```


# Quick Command Reference

This document provides quick commands to run all parts of the assignment.

## Q1: Food Delivery System Commands

```bash
# Navigate to Q1 directory
cd /home/shreyasmehta/Desktop/4th\ sem/DASS/Projects/Ass-2/2023101059/q1

# Run the application
python3 src/cli.py

# Run tests
python3 -m unittest testcases.test_food_delivery_system

# Default login credentials:
# Customer: username="customer", password="password"
# Delivery Agent: username="agent", password="password" 
# Admin: username="admin", password="admin123"
```

## Q2: Gobblet of Fire Game Commands

```bash
# Navigate to Q2 directory
cd /home/shreyasmehta/Desktop/4th\ sem/DASS/Projects/Ass-2/2023101059/q2

# Run the final version of the game
python3 AllLint/gobbletfinal.py

# Run the original version (before linting)
python3 OriginalGame/gobblet.py

# Check lint results
cat AllLint/lintScore.txt

# View detailed lint report
cat AllLint/lintfinal.txt
```

## Q3: Dollmart E-Commerce System Commands

```bash
# Navigate to Q3 directory
cd /home/shreyasmehta/Desktop/4th\ sem/DASS/Projects/Ass-2/2023101059/q3

# Run the main application
python3 src/main.py

# Run all tests
python3 run_tests.py

# Run specific test module
python3 run_tests.py testcases/test_customers.py

# View UML class diagram
# Open q3/uml/uml.png to see the class diagram
```

## General Commands

```bash
# Return to project root
cd /home/shreyasmehta/Desktop/4th\ sem/DASS/Projects/Ass-2/2023101059

# View README with full documentation
less Readme.md
# Press 'q' to exit less viewer
```
