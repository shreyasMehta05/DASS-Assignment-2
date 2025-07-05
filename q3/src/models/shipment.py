import random
import threading
import time
from datetime import datetime, timedelta

class Shipment:
    """
    Manages the delivery process for a purchase.
    
    Includes status tracking, estimated delivery dates, and
    automated status updates to simulate real delivery progression.
    """
    
    def __init__(self, purchase_id, purchase=None):
        """
        Initialize shipment tracking for a purchase.
        
        Args:
            purchase_id: The purchase this shipment is associated with
            purchase: Reference to the Purchase object
        """
        self.shipment_id = random.randint(10000, 99999)
        self.purchase_id = purchase_id
        self.purchase = purchase  # Store reference to the purchase
        self.status = "Processing"
        # Set estimated delivery 3 days from now
        self.arrival_date = datetime.now() + timedelta(days=3)
        # Generate tracking number for customer reference
        self.tracking_code = f"SHIP{random.randint(1000000, 9999999)}"
        
        # Start background thread to automatically update shipment status
        self.status_thread = threading.Thread(target=self._auto_update_status)
        self.status_thread.daemon = True
        self.status_thread.start()
    
    def get_status(self):
        """
        Get current shipment status information.
        
        Returns:
            Dictionary with status, delivery date, and tracking info
        """
        return {
            "status": self.status,
            "estimated_arrival": self.arrival_date.strftime("%Y-%m-%d"),
            "tracking_code": self.tracking_code,
        }
    
    def update_status(self, new_status):
        """
        Manually update the shipment status.
        
        Args:
            new_status: New shipment status
            
        Returns:
            Boolean indicating update success
        """
        self.status = new_status
        
        # When manually updated to "Delivered", also update the purchase status
        if new_status == "Delivered" and self.purchase is not None:
            self.purchase.status = "Completed"
            
        return True
    
    def _auto_update_status(self):
        """
        Automatically progress shipment through status stages.
        
        This is a background thread that simulates the natural progression
        of a shipment through various logistics stages.
        """
        statuses = ["Processing", "Packed", "Shipped", "Out for delivery", "Delivered"]
        current_index = 0
        
        # Progress through each status with a delay
        while current_index < len(statuses):
            self.status = statuses[current_index]
            
            # Update purchase status when delivery is complete
            if self.status == "Delivered" and self.purchase is not None:
                self.purchase.status = "Completed"
                
            time.sleep(5)  # Simulate time passing between status changes
            current_index += 1
