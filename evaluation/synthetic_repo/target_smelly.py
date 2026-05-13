def calculate_shipping(distance, weight, is_member):
    """
    Calculates shipping cost based on distance, weight, and membership.
    WARNING: Highly nested spaghetti code!
    """
    cost = 0
    if is_member:
        if distance < 50:
            if weight < 10:
                cost = 5
            else:
                cost = 10
        else:
            if weight < 10:
                cost = 15
            else:
                cost = 20
    else:
        if distance < 50:
            if weight < 10:
                cost = 10
            else:
                cost = 15
        else:
            if weight < 10:
                cost = 20
            else:
                cost = 25
                
    return cost