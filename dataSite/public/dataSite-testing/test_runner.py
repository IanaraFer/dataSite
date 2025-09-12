"""
Test Runner for DataSight AI - Company Data Analyzer

This script orchestrates the execution of all tests in the DataSight AI testing suite.
It utilizes pytest to discover and run tests across various directories, including unit, integration, and performance tests.
"""

import pytest

if __name__ == "__main__":
    # Run all tests in the tests directory
    pytest.main(["-q", "--tb=short", "tests"])