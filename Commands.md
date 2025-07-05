# Quick Command Reference

This document provides quick commands to run all parts of the assignment.

## Project Overview

### Complete Directory Structure
```
/home/shreyasmehta/Desktop/4th sem/DASS/Projects/Ass-2/2023101059/
├── Commands.md         # This quick reference guide
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

## Q1: Food Delivery System

### Directory Structure
```
q1/
├── data/               # Data storage directory
├── src/                # Source code
│   ├── __init__.py
│   ├── models.py       # Data models
│   ├── services.py     # Business logic
│   ├── database.py     # Data persistence
│   └── cli.py          # Command-line interface
└── testcases/          # Unit tests
    ├── __init__.py
    └── test_food_delivery_system.py
```

### Commands
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

## Q2: Gobblet of Fire Game

### Directory Structure
```
q2/
├── AllLint/
│   ├── gobbletfinal.py       # Final version with best lint score
│   ├── gobblet_v2.py         # Progressive improvements
│   ├── gobblet_v3.py
│   ├── gobblet_v4.py
│   ├── gobblet_v5.py
│   ├── lintfinal.txt         # Final lint report
│   └── lintScore.txt         # Lint scores summary
├── InitialLint/
│   └── initialLint.txt       # Initial lint report
├── OriginalGame/
│   └── gobblet.py            # Original implementation
└── pic/
    └── game-background.jpg   # Game asset
```

### Commands
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

## Q3: Dollmart E-Commerce System

### Directory Structure
```
q3/
├── src/                # Source code
│   ├── app.py          # Application logic
│   ├── __init__.py
│   ├── main.py         # Main application entry point
│   ├── models/         # Domain models
│   │   ├── customer.py
│   │   ├── item.py
│   │   ├── purchase.py
│   │   ├── shipment.py
│   │   ├── shopping_basket.py
│   │   ├── transaction.py
│   │   └── voucher.py
│   └── utils/          # Utility functions
├── testcases/          # Test suites
│   ├── test_customers.py
│   ├── test_integration.py
│   ├── test_items.py
│   ├── test_purchases.py
│   ├── test_shipments.py
│   ├── test_shopping_basket.py
│   ├── test_transactions.py
│   └── test_vouchers.py
├── uml/                # UML diagrams
│   ├── mermaid.txt     # UML class diagram in Mermaid format
│   └── uml.png         # UML diagram image
├── Report.md           # Design documentation
├── Test.md             # Test documentation
└── run_tests.py        # Test runner script
```

### Commands
```bash
# Navigate to Q3 directory
cd /home/shreyasmehta/Desktop/4th\ sem/DASS/Projects/Ass-2/2023101059/q3

# Run the main application
python3 src/main.py

# Alternative way to run the application
python3 src/app.py

# Run all tests
python3 run_tests.py

# Run specific test module
python3 run_tests.py testcases/test_customers.py

# View UML class diagram
# Open q3/uml/mermaid.txt in a Mermaid viewer (e.g., https://mermaid.live)
# Or view the pre-rendered diagram at q3/uml/uml.png
```

## General Commands

```bash
# Return to project root
cd /home/shreyasmehta/Desktop/4th\ sem/DASS/Projects/Ass-2/2023101059

# View README with full documentation
less Readme.md
# Press 'q' to exit less viewer
```
