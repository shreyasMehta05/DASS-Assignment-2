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
