import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.transaction import Transaction
from src.models.purchase import Purchase
from src.models.customer import PersonalClient
from src.models.item import Item

class TestTransactionCreation:
    """Tests for transaction creation functionality"""
    
    def test_basic_transaction_creation(self):
        """Test creating a transaction with basic parameters"""
        purchase = None  # Could be a Purchase object but not required
        transaction = Transaction(purchase, "Card", 100.00)
        
        assert 100000 <= transaction.transaction_id <= 999999  # ID in expected range
        assert transaction.method == "Card"
        assert transaction.amount == 100.00
        assert transaction.status == "Pending"
    
    def test_zero_amount_transaction(self):
        """Test creating a transaction with zero amount"""
        transaction = Transaction(None, "Digital", 0.00)
        
        assert transaction.amount == 0.00
        assert transaction.status == "Pending"
    
    def test_negative_amount_transaction(self):
        """Test creating a transaction with negative amount (refund scenario)"""
        transaction = Transaction(None, "Refund", -50.00)
        
        assert transaction.amount == -50.00
        assert transaction.status == "Pending"
    
    def test_different_payment_methods(self):
        """Test creating transactions with different payment methods"""
        transaction1 = Transaction(None, "Card", 100.00)
        transaction2 = Transaction(None, "Digital", 100.00)
        transaction3 = Transaction(None, "Gift Card", 100.00)
        
        assert transaction1.method == "Card"
        assert transaction2.method == "Digital"
        assert transaction3.method == "Gift Card"
    
    def test_transaction_unique_ids(self):
        """Test that transactions receive unique IDs"""
        transactions = [Transaction(None, "Card", 100.00) for _ in range(100)]
        ids = [t.transaction_id for t in transactions]
        
        # Check for uniqueness
        assert len(set(ids)) == len(ids)


class TestTransactionProcessing:
    """Tests for transaction processing functionality"""
    
    def test_receipt_creation(self):
        """Test generating a receipt for a transaction"""
        transaction = Transaction(None, "Card", 123.45)
        
        receipt = transaction.create_receipt()
        
        # Receipt should contain transaction ID and amount
        assert str(transaction.transaction_id) in receipt
        assert "123.45" in receipt
    
    def test_payment_processing_success(self):
        """Test successful payment processing"""
        transaction = Transaction(None, "Card", 100.00)
        
        # Process payment with card details
        result = transaction.process_payment({
            "card_number": "1234567890123456",
            "expiry": "12/25",
            "cvv": "123"
        })
        
        assert result == True
        assert transaction.status == "Completed"
    
    def test_different_payment_details(self):
        """Test processing payments with different payment detail formats"""
        # Card payment
        transaction1 = Transaction(None, "Card", 100.00)
        result1 = transaction1.process_payment({
            "card_number": "1234567890123456",
            "expiry": "12/25",
            "cvv": "123"
        })
        
        # Digital wallet payment
        transaction2 = Transaction(None, "Digital", 100.00)
        result2 = transaction2.process_payment({
            "wallet_id": "user@wallet.com"
        })
        
        # Bank transfer payment
        transaction3 = Transaction(None, "Bank Transfer", 100.00)
        result3 = transaction3.process_payment({
            "account": "123456789",
            "routing": "987654321"
        })
        
        assert result1 == True
        assert result2 == True
        assert result3 == True
    
    def test_transaction_with_purchase(self):
        """Test transaction linked to a purchase"""
        # Create a purchase
        customer = PersonalClient("testuser", "password", "123 Test St")
        item = Item("Test Item", "Description", 10.00, "Test", 10)
        purchase = Purchase(customer, [{"item": item, "quantity": 1}], 10.00)
        
        # Create transaction for this purchase
        transaction = Transaction(purchase, "Card", purchase.final_cost)
        
        # Process payment
        transaction.process_payment({"card_number": "1234567890123456"})
        
        assert transaction.status == "Completed"
