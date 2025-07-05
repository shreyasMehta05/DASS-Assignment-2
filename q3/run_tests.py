#!/usr/bin/env python3

"""
Helper script to run the Dollmart tests with the correct Python path setup.
This ensures the imports work correctly without needing to modify PYTHONPATH.
"""

import os
import sys
import pytest

if __name__ == "__main__":
    # Add project root to Python path
    sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
    
    # Run pytest with command line arguments
    args = sys.argv[1:] or ["testcases/"]
    sys.exit(pytest.main(args))
