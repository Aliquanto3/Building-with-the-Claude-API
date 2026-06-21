def greeting():
    print("Hi there!")


def calculate_pi_5_digits():
    """
    Calculates pi to 5 decimal places using the Machin formula.
    Machin's formula: pi/4 = 4*arctan(1/5) - arctan(1/239)
    Returns pi as a float rounded to 5 decimal places (3.14159)
    """
    from decimal import Decimal, getcontext
    
    # Set precision high enough to calculate accurately
    getcontext().prec = 50
    
    def arctan(x, num_terms=100):
        """Calculate arctan(x) using Taylor series"""
        x = Decimal(x)
        power = x
        result = power
        for n in range(1, num_terms):
            power *= -x * x
            result += power / (2 * n + 1)
        return result
    
    # Machin formula: pi = 16*arctan(1/5) - 4*arctan(1/239)
    pi = 4 * (4 * arctan(Decimal(1) / Decimal(5)) - arctan(Decimal(1) / Decimal(239)))
    
    # Return pi rounded to 5 decimal places
    return round(float(pi), 5)