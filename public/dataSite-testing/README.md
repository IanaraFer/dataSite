# DataSight AI - Company Data Analyzer Testing Environment

## Overview
This repository contains the testing environment for the DataSight AI - Company Data Analyzer platform. It includes unit tests, integration tests, performance tests, and security tests to ensure the application functions correctly and securely.

## Directory Structure
- **tests/**: Contains all test files organized into unit, integration, and fixtures.
  - **unit/**: Unit tests for individual components and methods.
  - **integration/**: Tests that validate the interaction between components.
  - **fixtures/**: Sample data and mock data for testing purposes.
- **test_data/**: Contains valid, invalid, and edge case sample data files for testing.
- **performance/**: Performance tests to evaluate the application's behavior under load.
- **selenium_tests/**: Selenium-based tests for UI interactions.
- **security_tests/**: Tests focused on the security aspects of the application.
- **utils/**: Utility functions and helpers for testing.
- **requirements-test.txt**: Lists dependencies required for running tests.
- **pytest.ini**: Configuration settings for pytest.
- **tox.ini**: Configuration for Tox to automate testing in multiple environments.
- **coverage.ini**: Configuration for measuring code coverage.
- **test_runner.py**: Script to run the tests.

## Setup Instructions
1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd dataSite-testing
   ```

2. **Install Dependencies**
   Use the provided `requirements-test.txt` to install the necessary packages.
   ```bash
   pip install -r requirements-test.txt
   ```

3. **Run Tests**
   You can run all tests using pytest:
   ```bash
   pytest
   ```

4. **Run Specific Tests**
   To run a specific test file, use:
   ```bash
   pytest tests/test_data_analyzer.py
   ```

5. **Check Code Coverage**
   To check the code coverage after running tests, use:
   ```bash
   coverage run -m pytest
   coverage report
   ```

## Contribution Guidelines
- Ensure all tests are passing before submitting a pull request.
- Follow the coding style guidelines outlined in the main project repository.
- Add new tests for any new features or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.