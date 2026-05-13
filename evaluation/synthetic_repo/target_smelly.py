def calculate_discounted_prices(cart_items, customer_tier):
    """
    Calculates the final price of items based on customer tier and item type.
    """
    final_prices = []
    
    if cart_items is not None and len(cart_items) > 0:
        discount_rates = {
            'GOLD': {'electronics': 0.80, 'clothing': 0.85, 'default': 0.90},
            'SILVER': {'electronics': 0.90, 'clothing': 0.95, 'default': 0.98},
            'default': {'electronics': 1.00, 'clothing': 1.00, 'default': 1.00}
        }
        
        for item in cart_items:
            tier_rate = discount_rates.get(customer_tier, discount_rates['default'])
            item_rate = tier_rate.get(item['type'], tier_rate['default'])
            final_prices.append(item['price'] * item_rate)
    
    return final_prices