# Food Delivery System Test Documentation

This document provides details about the test cases in the Food Delivery System test suite.

## Overview

The test suite contains 50 test cases that cover all major functionality of the food delivery system including:
- User registration and authentication
- Menu item management
- Order creation and tracking
- Order status updates
- Delivery agent operations
- System persistence and data integrity

## Test Case Descriptions

### User-Related Tests

| Test ID | Name | Description |
|---------|------|-------------|
| 01 | Register User | Tests successful registration of a new user with valid credentials |
| 02 | Duplicate User Registration | Verifies system prevents duplicate usernames |
| 03 | Valid User Login | Tests user login with correct credentials |
| 04 | Invalid User Login | Verifies system rejects incorrect passwords |
| 05 | Get User Details | Tests retrieval of user information |
| 22 | Get Nonexistent User | Tests behavior when requesting details of a nonexistent user |
| 42 | Multiple Users Registration | Tests registering multiple users in the system |
| 49 | Get User Orders (Empty) | Tests retrieving orders for a user with no order history |
| 50 | Update User Details | Tests updating user's order history after placing an order |

### Menu-Related Tests

| Test ID | Name | Description |
|---------|------|-------------|
| 06 | Add Menu Item | Tests adding a new item to the menu |
| 07 | Get All Menu Items | Verifies retrieval of all menu items |
| 08 | Get Specific Menu Item | Tests retrieval of a menu item by ID |
| 09 | Update Menu Item | Tests updating an existing menu item's details |
| 10 | Delete Menu Item | Tests removal of a menu item |
| 24 | Get Nonexistent Menu Item | Tests behavior when requesting a nonexistent menu item |
| 34 | Update Nonexistent Menu Item | Verifies system handles updates to nonexistent items |
| 35 | Delete Nonexistent Menu Item | Tests deleting a nonexistent menu item |
| 40 | Get Menu Item By ID | Tests retrieving a menu item using its ID |

### Order-Related Tests

| Test ID | Name | Description |
|---------|------|-------------|
| 11 | Create Takeaway Order | Tests creating a takeaway order |
| 12 | Create Home Delivery Order | Tests creating a home delivery order |
| 13 | Get Order Details | Tests retrieving order details |
| 14 | Order Initial Status | Verifies new orders start with "Placed" status |
| 25 | Get Nonexistent Order | Tests behavior when requesting a nonexistent order |
| 26 | Create Order Nonexistent User | Tests order creation with invalid user |
| 27 | Create Order Nonexistent Item | Tests order creation with nonexistent menu items |
| 28 | Create Order Empty Items | Verifies system prevents orders with no items |
| 29 | Order Total Price | Tests accurate calculation of order total price |
| 30 | Update Nonexistent Order | Tests updating status of a nonexistent order |
| 33 | Create Multiple Orders | Tests creating multiple orders in the system |
| 36 | Order With Default Address | Tests order creation using user's default address |
| 37 | Create Order Multiple Items | Tests creating orders with multiple menu items |
| 43 | Order Creation Time | Verifies creation timestamp is set for orders |
| 44 | Order Estimated Completion Time | Tests setting of estimated completion time |
| 46 | Get All Orders Empty | Tests retrieving orders when none exist in the system |
| 48 | Order Item Properties | Tests order item quantity and price calculations |

### Order Status Tests

| Test ID | Name | Description |
|---------|------|-------------|
| 15 | Update Order Status | Tests updating an order's status |
| 16 | Cancel Order | Tests cancellation of an order |
| 31 | Invalid Status Transition | Tests system prevents invalid status transitions |
| 38 | Order Status After Update | Tests order status is correctly updated after changes |

### Delivery Agent Tests

| Test ID | Name | Description |
|---------|------|-------------|
| 17 | Register Delivery Agent | Tests registering a new delivery agent |
| 18 | Duplicate Agent Registration | Verifies system prevents duplicate agent usernames |
| 19 | Valid Agent Login | Tests agent login with correct credentials |
| 20 | Invalid Agent Login | Verifies system rejects incorrect agent passwords |
| 21 | Get Agent Details | Tests retrieval of delivery agent information |
| 23 | Get Nonexistent Agent | Tests behavior when requesting a nonexistent agent |
| 32 | Get All Delivery Agents | Tests retrieval of all registered delivery agents |
| 41 | Multiple Agents Registration | Tests registering multiple agents in the system |
| 47 | Get Available Agents | Tests retrieving only available delivery agents |

### System Tests

| Test ID | Name | Description |
|---------|------|-------------|
| 39 | Database Save And Reload | Tests data persistence across service restarts |
| 45 | Time Remaining Calculation | Tests accurate calculation of time remaining for orders |

## Running the Tests

To run all tests in the suite:

```bash
cd /home/shreyasmehta/Desktop/4th\ sem/DASS/Projects/Ass-2/2023101059/q1
python3 -m unittest testcases.test_food_delivery_system
```

To run a specific test:

```bash
cd /home/shreyasmehta/Desktop/4th\ sem/DASS/Projects/Ass-2/2023101059/q1
python3 -m unittest testcases.test_food_delivery_system.TestFoodDeliveryBasics.test_01_register_user
```

