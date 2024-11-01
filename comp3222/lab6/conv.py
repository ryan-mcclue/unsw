def octal_to_binary(octal_str):
    """
    Convert octal number to 9-bit binary representation.
    
    Args:
        octal_str: String or integer representing octal number
        
    Returns:
        String containing 9-bit binary representation
        
    Raises:
        ValueError: If input is not a valid octal number
    """
    # Validate input
    try:
        # Convert input to integer using base 8
        decimal_num = int(str(octal_str), 8)
        
        # Check if number can fit in 9 bits
        if decimal_num > 511:  # 511 is max value for 9 bits (0o777)
            raise ValueError("Octal number too large for 9-bit representation")
            
        # Convert to binary and remove '0b' prefix
        binary = bin(decimal_num)[2:]
        
        # Pad with leading zeros to ensure 9 bits
        binary = binary.zfill(9)
        
        return binary
        
    except ValueError:
        raise ValueError("Invalid octal number")

# Example usage
if __name__ == "__main__":
    test_cases = ["100", "005", "010", "201", "300"]
    
    for test in test_cases:
        try:
            result = octal_to_binary(test)
            print(f"Octal {test} = Binary {result}")
        except ValueError as e:
            print(f"Error with {test}: {e}")
