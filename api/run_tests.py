"""
Integration test runner for the Promethios Compliance Demo Phase 2.

This script runs all the unit tests for the Phase 2 implementation.
"""

import unittest
import sys
import os

# Add the parent directory to the path so we can import the modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import all test modules
from tests.test_trust_factors import *
from tests.test_regulatory_frameworks import *
from tests.test_openai_explainer import *
from tests.test_pdf_report_generator import *
from tests.test_lending_club_api import *
from tests.test_compliance_timeline import *

if __name__ == "__main__":
    # Run all tests
    unittest.main()
