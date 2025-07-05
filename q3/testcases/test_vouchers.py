import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.voucher import Voucher
from datetime import datetime, timedelta

class TestVoucherCreation:
    """Tests for voucher creation functionality"""
    
    def test_basic_voucher_creation(self):
        """Test creating a voucher with default validity period"""
        voucher = Voucher("TEST10", 10)
        
        assert voucher.code == "TEST10"
        assert voucher.discount_percent == 10
        
        # Check expiry date is set correctly (default 30 days)
        expected_date = datetime.now() + timedelta(days=30)
        # Compare only the date part to avoid tiny timing differences
        assert voucher.expiry_date.date() == expected_date.date()
    
    def test_voucher_with_custom_validity(self):
        """Test creating a voucher with custom validity period"""
        voucher = Voucher("TEST20", 20, 60)
        
        assert voucher.code == "TEST20"
        assert voucher.discount_percent == 20
        
        # Check expiry date is set correctly
        expected_date = datetime.now() + timedelta(days=60)
        assert voucher.expiry_date.date() == expected_date.date()
    
    def test_expired_voucher_creation(self):
        """Test creating an already expired voucher"""
        voucher = Voucher("EXPIRED", 15, -10)  # Expired 10 days ago
        
        assert voucher.code == "EXPIRED"
        assert voucher.discount_percent == 15
        
        # Check expiry date is set correctly
        expected_date = datetime.now() + timedelta(days=-10)
        assert voucher.expiry_date.date() == expected_date.date()
    
    def test_zero_validity_voucher(self):
        """Test creating a voucher that expires today"""
        voucher = Voucher("TODAY", 25, 0)
        
        assert voucher.code == "TODAY"
        assert voucher.discount_percent == 25
        
        # Check expiry date is today
        today = datetime.now().date()
        assert voucher.expiry_date.date() == today

class TestVoucherValidity:
    """Tests for voucher validity checking"""
    
    def test_valid_voucher(self):
        """Test that a voucher with future expiry date is valid"""
        voucher = Voucher("FUTURE", 10, 30)
        assert voucher.is_valid() == True
    
    def test_expired_voucher(self):
        """Test that an expired voucher is invalid"""
        voucher = Voucher("PAST", 10, -1)
        assert voucher.is_valid() == False
    
    def test_expiring_today_voucher(self):
        """Test a voucher that expires today"""
        # Create voucher with 0 days validity
        voucher = Voucher("TODAY", 10, 0)
        
        # Expiring today is still valid
        assert voucher.is_valid() == True
    
    def test_about_to_expire_voucher(self):
        """Test a voucher that is about to expire"""
        voucher = Voucher("SOON", 10, 1)  # Expires tomorrow
        assert voucher.is_valid() == True

class TestDiscountCalculation:
    """Tests for discount calculation functionality"""
    
    def test_basic_discount_calculation(self):
        """Test basic percentage discount calculation"""
        voucher = Voucher("PERCENT10", 10)
        
        # 10% of 100 is 10
        assert voucher.calculate_discount(100) == 10.0
        
        # 10% of 50 is 5
        assert voucher.calculate_discount(50) == 5.0
    
    def test_zero_discount_calculation(self):
        """Test calculation with zero discount percentage"""
        voucher = Voucher("ZERO", 0)
        
        # 0% of any amount is 0
        assert voucher.calculate_discount(100) == 0.0
        assert voucher.calculate_discount(50) == 0.0
    
    def test_high_discount_calculation(self):
        """Test calculation with high discount percentage"""
        voucher = Voucher("HALF", 50)
        
        # 50% of 100 is 50
        assert voucher.calculate_discount(100) == 50.0
        
        voucher = Voucher("FULL", 100)
        
        # 100% of 100 is 100
        assert voucher.calculate_discount(100) == 100.0
    
    def test_discount_with_decimal_price(self):
        """Test discount calculation with decimal prices"""
        voucher = Voucher("PERCENT25", 25)
        
        # 25% of 19.99 is 4.9975
        assert voucher.calculate_discount(19.99) == 4.9975
    
    def test_discount_with_zero_price(self):
        """Test discount calculation with zero price"""
        voucher = Voucher("PERCENT25", 25)
        
        # 25% of 0 is 0
        assert voucher.calculate_discount(0) == 0.0
    
    def test_discount_with_negative_price(self):
        """Test discount calculation with negative price"""
        # Edge case that might happen with refunds
        voucher = Voucher("PERCENT10", 10)
        
        # 10% of -100 is -10
        assert voucher.calculate_discount(-100) == -10.0
