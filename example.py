"""
This file demonstrates the advanced features of the TODO-to-Issues workflow.
"""

def process_payment(amount, currency):
    # TODO(TITLE: Implement Payment Gateway Integration, PRIORITY: critical, TYPE: feature, EPIC: monetization): Need to support Stripe and PayPal
    if amount <= 0:
        raise ValueError("Amount must be positive")
    
    # TODO(REF: Implement Payment Gateway Integration): Add validation for supported currencies
    if currency not in ['USD', 'EUR']:
        raise ValueError("Unsupported currency")

    return True

def optimization_task():
    # TODO(TITLE: Reduce memory footprint of data processing, EFFORT: large, TYPE: performance, ASSIGNEE: octocat)
    # This is a complex task that might take a few days
    data = [i for i in range(1000000)]
    return sum(data)

def legacy_code():
    # TODO(TITLE: Refactor legacy authentication module, PRIORITY: medium, TYPE: refactor)
    # This code is old and needs to be updated to use modern standards
    pass

class DataSanitizer:
    def sanitize(self, input_str):
        # TODO(TITLE: Fix XSS vulnerability in sanitizer, PRIORITY: critical, TYPE: security)
        # We need to escape HTML characters here
        return input_str.strip()
