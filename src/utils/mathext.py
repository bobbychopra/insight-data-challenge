"""Useful Math Extensions Module."""


def floor(value, number_of_decimals):
    """get the floor of a float upto number of decimals."""
    numerator = int(value * pow(10, number_of_decimals))
    denominator = pow(10, number_of_decimals) * 1.0
    return numerator / denominator
