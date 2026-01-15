"""
This file demonstrates how TODO references work across different files.
"""

from example import process_payment

def checkout_shopping_cart(cart):
    total = sum(item.price for item in cart)
    
    # TODO(REF: Implement Payment Gateway Integration): We need to call the payment processor here once it's ready
    # Note how this TODO links back to the Issue created by the canonical TODO in example.py
    process_payment(total, 'USD')

def admin_dashboard():
    # TODO(REF: Refactor legacy authentication module): Dashboard still uses the old auth system
    pass
