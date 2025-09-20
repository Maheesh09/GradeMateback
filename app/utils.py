"""
Utility functions for the GradeMate application
"""

def roman_to_int(roman: str) -> int:
    """
    Convert Roman numeral to integer
    
    Args:
        roman: Roman numeral string (e.g., 'i', 'ii', 'iii', etc.)
        
    Returns:
        Integer representation of the Roman numeral
        
    Raises:
        ValueError: If the Roman numeral is not valid
    """
    roman = roman.lower().strip()
    
    # Roman numeral mapping
    roman_map = {
        'i': 1, 'ii': 2, 'iii': 3, 'iv': 4, 'v': 5,
        'vi': 6, 'vii': 7, 'viii': 8, 'ix': 9, 'x': 10,
        'xi': 11, 'xii': 12, 'xiii': 13, 'xiv': 14, 'xv': 15,
        'xvi': 16, 'xvii': 17, 'xviii': 18, 'xix': 19, 'xx': 20
    }
    
    if roman not in roman_map:
        raise ValueError(f"Invalid Roman numeral: {roman}")
    
    return roman_map[roman]

def int_to_roman(num: int) -> str:
    """
    Convert integer to Roman numeral
    
    Args:
        num: Integer to convert (1-20)
        
    Returns:
        Roman numeral string
        
    Raises:
        ValueError: If the number is out of range
    """
    if not 1 <= num <= 20:
        raise ValueError(f"Number {num} is out of range (1-20)")
    
    # Integer to Roman mapping
    int_map = {
        1: 'i', 2: 'ii', 3: 'iii', 4: 'iv', 5: 'v',
        6: 'vi', 7: 'vii', 8: 'viii', 9: 'ix', 10: 'x',
        11: 'xi', 12: 'xii', 13: 'xiii', 14: 'xiv', 15: 'xv',
        16: 'xvi', 17: 'xvii', 18: 'xviii', 19: 'xix', 20: 'xx'
    }
    
    return int_map[num]

def validate_roman_numeral(roman: str) -> bool:
    """
    Validate if a string is a valid Roman numeral (i-xx)
    
    Args:
        roman: String to validate
        
    Returns:
        True if valid, False otherwise
    """
    try:
        roman_to_int(roman)
        return True
    except ValueError:
        return False
