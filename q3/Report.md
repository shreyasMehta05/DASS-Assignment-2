# Dollmart E-Commerce System: Design & Implementation Report

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
